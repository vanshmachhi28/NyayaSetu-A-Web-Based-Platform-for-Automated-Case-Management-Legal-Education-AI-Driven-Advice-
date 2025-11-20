from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Case, Client, Lawyer, CustomUser, ContactQuery, Question, Answer


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'status', 'client', 'lawyer']
        # template_name = 'cases/case_form.html'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone']
        # template_name = 'clients/client_form.html'


class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = ['first_name', 'last_name', 'email', 'phone']
        # template_name = 'lawyers/lawyer_form.html'


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    pass




#Contact_US page

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactQuery
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': True, 'placeholder': 'Your Message'}),
        }








#Module 10 quiz 
class QuizAttemptForm(forms.Form):
    selected = forms.ChoiceField(
        choices=[('A','A'),('B','B'),('C','C'),('D','D')],
        widget=forms.RadioSelect
    )




#Module no . 7 Q&A Forum
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'question_text']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control qasubject-select'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control qamessage-text', 'rows': 4})
        }
        labels = {
            'subject': 'Select Subject',
            'question_text': 'Your Question'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']
        widgets = {
            'answer_text': forms.Textarea(attrs={'class': 'form-control qareply-text', 'rows': 4})
        }
        labels = {
            'answer_text': 'Your Reply'
        }


