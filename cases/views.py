import requests
import openai
from .models import LegalArticle, LegalLearnResource, LegalDocTemplate
import json

import io
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Client, Case, Lawyer, LegalArticle, QuizQuestion, QuizAttempt, QuizResult
from django.utils import timezone
from django.conf import settings
from .utils import google_web_search
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import QuizQuestion, QuizAttempt, QuizResult, Case, Document, UserSearchLog, Question, LegalChatMessage
from .forms import ClientForm, LawyerForm, CaseForm, CustomUserCreationForm, CustomAuthenticationForm, ContactForm, QuizAttemptForm, QuestionForm, AnswerForm
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients_count'] = Client.objects.count()
        context['lawyers_count'] = Lawyer.objects.count()
        context['cases_count'] = Case.objects.count()
        return context


# Client views

class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("cases:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("cases:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("cases:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Client"
        return context


# Lawyer Views

class LawyerListView(ListView):
    model = Lawyer
    template_name = "lawyers/lawyer_list.html"


class LawyerCreateView(CreateView):
    model = Lawyer
    form_class = LawyerForm
    template_name = "lawyers/lawyer_form.html"
    success_url = "/lawyers/"


class LawyerUpdateView(UpdateView):
    model = Lawyer
    form_class = LawyerForm
    template_name = "lawyers/lawyer_form.html"
    success_url = "/lawyers/"


class LawyerDeleteView(DeleteView):
    model = Lawyer
    template_name = "lawyers/lawyer_confirm_delete.html"
    success_url = reverse_lazy("cases:lawyer_list")


class CaseListView(ListView):
    model = Case
    template_name = "cases/case_list.html"


class CaseCreateView(CreateView):
    model = Case
    form_class = CaseForm
    template_name = "cases/case_form.html"
    success_url = "/cases/"


class CaseUpdateView(UpdateView):
    model = Case
    form_class = CaseForm
    template_name = "cases/case_form.html"
    success_url = "/cases/"


class CaseDeleteView(DeleteView):
    model = Case
    template_name = "cases/case_confirm_delete.html"
    success_url = reverse_lazy("cases:case_list")


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']       # Explicitly set role
            user.save()
            messages.success(request, 'Registration successful. Please login!')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Fix errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Login successful. Welcome!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Try again.')
    else:
        # Always initialize form, so 'form' is defined for GET and error cases
        form = CustomAuthenticationForm()
        if 'next' in request.GET:
            messages.warning(request, "You must login first to access this page.")
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('cases:home')


#about_us page 
def about_view(request):
    return render(request, 'about.html')


#Contact_Us Page

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for reaching out! We will get back to you soon.")
            return redirect('cases:contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})





#Module no.10 Quiz 
@login_required
def quiz_start(request, category='lawbasics'):
    if category not in ['lawbasics', 'beginner', 'subjectwise', 'examprep', 'challenge']:
        category = 'lawbasics'
    question_ids = list(QuizQuestion.objects.filter(category=category).values_list('id', flat=True))
    request.session['quiz_score'] = 0
    request.session['quiz_pk_list'] = question_ids
    request.session['quiz_index'] = 0
    request.session['quiz_time_start'] = str(timezone.now())
    request.session['quiz_category'] = category
    return redirect('cases:quiz_next')


@login_required
def quiz_next(request):
    pk_list = request.session.get('quiz_pk_list', [])
    index = request.session.get('quiz_index', 0)
    score = request.session.get('quiz_score', 0)
    category = request.session.get('quiz_category', 'lawbasics')
    options = ['A', 'B', 'C', 'D']
    timer_secs = 15

    if index >= len(pk_list):
        QuizResult.objects.create(user=request.user, score=score)
        return redirect('cases:quiz_result')

    question_pk = pk_list[index]
    question = get_object_or_404(QuizQuestion, pk=question_pk)

    if request.method == "POST":
        # Timeout check (add this priority)
        if 'timeout' in request.POST:
            messages.warning(request, "You're out of time!")
            return redirect('cases:quiz_select')

        selected = request.POST.get('selected')
        # Validation: user must select an option
        if not selected:
            messages.warning(request, "Please select an answer!")
            # Re-display current question without incrementing index or saving attempt
            form = QuizAttemptForm()
            return render(request, "quiz/quiz_question.html", {
                "question": question,
                "form": form,
                "timer": timer_secs,
                "index": index + 1,
                "total": len(pk_list),
                "options": options,
                "category": category,
            })

        # Process answer if valid
        correct = selected == question.correct
        if correct:
            score += 1
        QuizAttempt.objects.create(
            user=request.user, question=question, selected=selected, correct=correct
        )
        request.session['quiz_score'] = score
        request.session['quiz_index'] = index + 1
        return redirect('cases:quiz_next')

    # If GET request, just show question
    form = QuizAttemptForm()
    return render(request, "quiz/quiz_question.html", {
        "question": question,
        "form": form,
        "timer": timer_secs,
        "index": index + 1,
        "total": len(pk_list),
        "options": options,
        "category": category,
    })



@login_required
def quiz_result(request):
    score = request.session.get('quiz_score', 0)
    total = len(request.session.get('quiz_pk_list', []))
    return render(request, "quiz/quiz_result.html", {"score": score, "total": total})




@login_required
def quiz_select(request):
    # Just return a template with all tab/category choices
    return render(request, "quiz/quiz_select.html")





#Module no. 9 Search & Filter
@login_required
def advanced_search(request):
    query = request.GET.get("q", "")
    filter_type = request.GET.get("type", "all")
    results = []
    count = 0

    if query:
        if filter_type in ["all", "case"]:
            results += list(Case.objects.filter(title__icontains=query))
        if hasattr(Document, "objects") and filter_type in ["all", "document"]:
            results += list(Document.objects.filter(name__icontains=query))
        # Add "LegalResource" if you have this model too

        count = len(results)
        UserSearchLog.objects.create(
            user=request.user, query=query, results_count=count, category=filter_type
        )

    return render(request, "search/advanced_search.html", {
        "query": query,
        "results": results,
        "filter_type": filter_type
    })





#Module no . 9 
#Google Custom Search API for Web Searches

@login_required
def advanced_search(request):
    query = request.GET.get("q", "")
    filter_type = request.GET.get("type", "all")
    results = []
    count = 0

    if query:
        if filter_type in ["all", "case"]:
            results += list(Case.objects.filter(title__icontains=query))
        if filter_type in ["all", "document"]:
            results += list(Document.objects.filter(name__icontains=query))
        # Add more local DB filters here

        # Call Google Search for external results if type=web or all
        if filter_type in ["all", "case","document","resource","web"]:
            api_key = settings.GOOGLE_API_KEY
            cse_id = settings.GOOGLE_SEARCH_ENGINE_ID
            web_results = google_web_search(query, api_key, cse_id)
            results += web_results

        count = len(results)
        UserSearchLog.objects.create(
            user=request.user, query=query, results_count=count, category=filter_type
        )

    return render(request, "search/advanced_search.html", {
        "query": query,
        "results": results,
        "filter_type": filter_type
    })



#Module no . 8 PDF & CSV Export
@login_required
def export_report(request, report_type='pdf'):
    # Fetch data - example: all cases for logged in user
    data_queryset = Case.objects.all()


    if report_type == 'pdf':
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("NyayaSetu Legal Report", styles['Title']))
        elements.append(Paragraph("Generated for: " + str(request.user), styles['Normal']))
        elements.append(Spacer(1, 12))

        # Prepare table data: headers + case info
        table_data = [['Case ID', 'Title', 'Status', 'Date Filed']]
        for case in data_queryset:
            table_data.append([str(case.id), case.title, case.status, case.date_filed.strftime("%d-%m-%Y")])

        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.darkblue),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        elements.append(t)

        doc.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="nyayasetu_report.pdf"'
        return response

    elif report_type == 'csv':
        data = []
        for case in data_queryset:
            data.append({
                "Case ID": case.id,
                "Title": case.title,
                "Status": case.status,
                "Date Filed": case.date_filed.strftime("%d-%m-%Y"),
            })
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="nyayasetu_report.csv"'
        df.to_csv(path_or_buf=response, index=False)
        return response

    else:
        return HttpResponse("Unsupported report type", status=400)
    

# file: cases/views.py
@login_required
def export_options(request):
    return render(request, 'export/export_options.html')




#Module no . 7 Q&A Forum 
def is_student_or_public(user):
    return user.is_authenticated and user.role in ('student', 'public')

def is_advocate(user):
    return user.is_authenticated and user.role == 'advocate'

@login_required
@user_passes_test(is_student_or_public)
def qna_ask_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.status = 'pending'
            question.save()
            # redirect or render success
    else:
        form = QuestionForm()
    return render(request, 'cases/qna_ask_question.html', {'form': form})
    messages.success(request, "Your question has been submitted!")

@login_required
@user_passes_test(is_advocate)
def qna_list_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'cases/qna_list_questions.html', {'questions': questions})

@login_required
@user_passes_test(is_advocate)
def qna_reply_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        answer = question.answer
    except Question.answer.RelatedObjectDoesNotExist:
        answer = None
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.question = question
            ans.responder = request.user
            ans.save()
            question.status = 'replied'
            question.save()
            messages.success(request, 'Your reply has been submitted.')
            return redirect('cases:qna_list_questions')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'cases/qna_reply_question.html', {'question': question, 'form': form})

@login_required
@user_passes_test(is_student_or_public)
def qna_view_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'cases/qna_view_question.html', {'question': question})


@login_required
def qna_my_questions(request):
    questions = Question.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'cases/qna_my_questions.html', {'questions': questions})




#Module no . 6 LegalAwareness
def is_public_user(user):
    return user.is_authenticated and user.role == 'public'

@login_required
@user_passes_test(is_public_user)
def legal_awareness_list(request):
    articles = LegalArticle.objects.order_by('-created_at')
    return render(request, 'cases/legal_awareness_list.html', {'articles': articles})

@login_required
@user_passes_test(is_public_user)
def legal_awareness_detail(request, pk):
    article = LegalArticle.objects.get(pk=pk)
    return render(request, 'cases/legal_awareness_detail.html', {'article': article})






#Module No . 5 Legal Learning (Students)
def is_student_user(user):
    return user.is_authenticated and user.role == 'student'

@login_required
@user_passes_test(is_student_user)
def legal_learn_list(request):
    resources = LegalLearnResource.objects.order_by('-created_at')
    return render(request, 'cases/legal_learn_list.html', {'resources': resources})

@login_required
@user_passes_test(is_student_user)
def legal_learn_detail(request, pk):
    resource = LegalLearnResource.objects.get(pk=pk)
    return render(request, 'cases/legal_learn_detail.html', {'resource': resource})





#Module no . 4 Legal Document Generator 
def is_allowed_user(user):
    return user.is_authenticated and user.role in ['student', 'public']

@login_required
@user_passes_test(is_allowed_user)
def legal_docgen_main(request):
    doc_templates = LegalDocTemplate.objects.all().order_by('title')
    return render(request, 'cases/legal_docgen_main.html', {'doc_templates': doc_templates})

@login_required
@user_passes_test(is_allowed_user)
def legal_docgen_form(request, doc_type):
    template = get_object_or_404(LegalDocTemplate, doc_type=doc_type)
    fields = json.loads(template.fields_json)
    if request.method == 'POST':
        data = {f['name']: request.POST.get(f['name'], '') for f in fields}
        rendered_doc = template.template_text
        for k, v in data.items():
            rendered_doc = rendered_doc.replace(f"{{{{{k}}}}}", v)
        request.session['generated_doc'] = rendered_doc
        request.session['generated_doc_title'] = template.title
        return redirect('cases:legal_docgen_result')
    return render(request, 'cases/legal_docgen_form.html', {'template': template, 'fields': fields})

@login_required
@user_passes_test(is_allowed_user)
def legal_docgen_result(request):
    doc = request.session.get('generated_doc', None)
    doc_title = request.session.get('generated_doc_title', 'Document')
    return render(request, 'cases/legal_docgen_result.html', {'doc': doc, 'doc_title': doc_title})



#Module no . 3 chat with a Legal Bot
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

def query_hf_model(question):
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": question,
        "parameters": {"max_new_tokens": 150},
    }
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=20)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, dict) and 'error' in result:
            return "Sorry, the AI service is temporarily unavailable."
        return result[0]['generated_text'] if isinstance(result, list) and 'generated_text' in result[0] else str(result)
    else:
        return "Sorry, an error occurred while contacting the AI service."

@login_required
def legalbot_chat_view(request):
    chat_history = LegalChatMessage.objects.filter(user=request.user).order_by('timestamp')
    bot_reply = ""
    if request.method == "POST":
        user_question = request.POST.get('question', '').strip()
        if user_question:
            prompt = (
                "Summarize the following user's legal situation in two sentences, "
                "then suggest plain next steps. Add: 'This is guidance, not a substitute for a lawyer.' "
                f"User question: {user_question}"
            )
            bot_reply = query_hf_model(prompt)
            LegalChatMessage.objects.create(
                user=request.user,
                user_query=user_question,
                bot_response=bot_reply,
            )
            return redirect('cases:legalbot_chat')
    return render(request, 'cases/legalbot_chat.html', {
        'legalbot_messages': [(msg.user_query, msg.bot_response, msg.timestamp) for msg in chat_history],
        'bot_reply': bot_reply,
    })







