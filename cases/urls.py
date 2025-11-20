from django.urls import path

from cases import views

from .views import quiz_next, quiz_result, quiz_start, register_view, login_view, logout_view, HomeView, about_view, contact_view, quiz_select, advanced_search

app_name = 'cases'  # the prefix before any url

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    #     URLS PATTERN FOR THE CLIENTS
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    #     URLS PATTERN FOR THE LAWYERS
    path('lawyers/', views.LawyerListView.as_view(), name='lawyer_list'),
    path('lawyers/create/', views.LawyerCreateView.as_view(), name='lawyer_create'),
    path('lawyers/<int:pk>/update/', views.LawyerUpdateView.as_view(), name='lawyer_update'),
    path('lawyers/<int:pk>/delete/', views.LawyerDeleteView.as_view(), name='lawyer_delete'),
    #     URLS PATTERNS FOR THE CASES
    path('cases/', views.CaseListView.as_view(), name='case_list'),
    path('cases/create/', views.CaseCreateView.as_view(), name='case_create'),
    path('cases/<int:pk>/update/', views.CaseUpdateView.as_view(), name='case_update'),
    path('cases/<int:pk>/delete/', views.CaseDeleteView.as_view(), name='case_delete'),

    path('', HomeView.as_view(), name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    

    #about_us page
    path('about/', about_view, name='about'),


    #contact_us page
    path('contact/', contact_view, name='contact'),



    #module no . 10 Quiz
    path('quiz/', quiz_select, name='quiz_select'),  # the tabbed selection page
    path('quiz/start/<str:category>/', quiz_start, name='quiz_start'),
    path('quiz/next/', quiz_next, name='quiz_next'),
    path('quiz/result/', quiz_result, name='quiz_result'),



    #Module no . 9 Search & Filter 
    path('search/', advanced_search, name='advanced_search'),



    #Module no . 8 PDF & CSV Export
    path('export/', views.export_options, name='export_options'),                  # Page with buttons
    path('export/<str:report_type>/', views.export_report, name='export_report'),  # The action url!

    #Module no . 7 Q&A Forum
    path('qna/ask/', views.qna_ask_question, name='qna_ask_question'),
    path('qna/list/', views.qna_list_questions, name='qna_list_questions'),
    path('qna/reply/<int:pk>/', views.qna_reply_question, name='qna_reply_question'),
    path('qna/view/<int:pk>/', views.qna_view_question, name='qna_view_question'),

    path('qna/my/', views.qna_my_questions, name='qna_my_questions'),


    #Module no . 6 LegalAwareness
    path('legal-awareness/', views.legal_awareness_list, name='legal_awareness_list'),
    path('legal-awareness/<int:pk>/', views.legal_awareness_detail, name='legal_awareness_detail'),


    #Module No . 5 Legal Learning (Students)
    path('legal-learning/', views.legal_learn_list, name='legal_learn_list'),
    path('legal-learning/<int:pk>/', views.legal_learn_detail, name='legal_learn_detail'),



    #Module no . 4 Legal Document Generator
    path('docgen/', views.legal_docgen_main, name='legal_docgen_main'),
    path('docgen/form/<str:doc_type>/', views.legal_docgen_form, name='legal_docgen_form'),
    path('docgen/result/', views.legal_docgen_result, name='legal_docgen_result'),
    
    #Module no . 3 Chat with a Legal 
    path('legalbot-chat/', views.legalbot_chat_view, name='legalbot_chat'),





]
