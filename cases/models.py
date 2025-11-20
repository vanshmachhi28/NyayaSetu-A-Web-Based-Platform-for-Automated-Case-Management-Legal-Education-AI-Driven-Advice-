from django.utils import timezone   

from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    # other fields...

    def __str__(self):
        # Always return a string; never None!
        return f"{self.first_name} {self.last_name or ''}".strip()

class Lawyer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    # other fields...

    def __str__(self):
        # Always return a string; never None!
        return f"{self.first_name} {self.last_name or ''}".strip()
    

class Case(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed')
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date_filed = models.DateTimeField(default=timezone.now)  # <-- USE THIS
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('advocate', 'Advocate'),
        ('public', 'Public User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='public')

    def __str__(self):
        return self.username


#Contact_Us page 

class ContactQuery(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"



#Module_10 Quiz Module
class QuizQuestion(models.Model):
    CATEGORY_CHOICES = [
        ('lawbasics', 'Law Basics Quiz'),
        ('beginner', '📘 Beginner Quizzes'),
        ('subjectwise', '⚖️ Subject-wise Quizzes'),
        ('examprep', '🎓 Exam Prep Quizzes'),
        ('challenge', '🧠 Challenge Quizzes'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lawbasics')
    question_text = models.CharField(max_length=300)
    opt_a = models.CharField(max_length=100)
    opt_b = models.CharField(max_length=100)
    opt_c = models.CharField(max_length=100)
    opt_d = models.CharField(max_length=100)
    correct = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    added_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.get_category_display()} | {self.question_text}"

class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1)
    correct = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)






#Module no. 9 Search & Filter 
class UserSearchLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    search_time = models.DateTimeField(auto_now_add=True)
    results_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=32, default="all")  # e.g., case, document, resource
    def __str__(self):
        return f"{self.user} searched '{self.query}' ({self.category}) at {self.search_time}"
    


class Document(models.Model):
    name = models.CharField(max_length=255)
    file_url = models.URLField(blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Modify if you have a detail view for documents, else return file_url
        return self.file_url or "#"



#Module no . 8 PDF & CSV Export
class ExportedReport(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('csv', 'CSV')])
    generated_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.file_name} ({self.file_type})"




#Module no. 7 Q&A Forum
User = get_user_model()

class Question(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'General'),
        ('criminal_law', 'Criminal Law'),
        ('civil_law', 'Civil Law'),
        ('family_law', 'Family Law'),
        ('constitutional_law', 'Constitutional Law'),
        # add more as needed
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending/replied/moderated

    def __str__(self):
        return f"{self.subject} - {self.author.username}"

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.responder.username} to Q[{self.question.id}]"



#Module no . 6 LegalAwareness
class LegalArticle(models.Model):
    CATEGORY_CHOICES = [
        ('ipc', 'Indian Penal Code'),
        ('crpc', 'Code of Criminal Procedure'),
        ('rights', 'Legal Rights'),
        ('process', 'Legal Processes'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



#Module no . 5 Legal Learning (Students)
class LegalLearnResource(models.Model):
    TOPIC_CHOICES = [
        ('constitution', 'Indian Constitution'),
        ('evidence', 'Evidence Act'),
        ('contract', 'Contract Law'),
        ('tort', 'Tort Law'),
        ('casebrief', 'Case Briefing'),
        ('research', 'Legal Research'),
        # add more as needed
    ]
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=30, choices=TOPIC_CHOICES)
    description = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





#Module no . 4 Legal Document Generator 
class LegalGeneratedDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('rent_agreement', 'Rent Agreement'),
        ('affidavit', 'Affidavit'),
        # Extend with more document types if needed
    ]
    doc_type = models.CharField(max_length=30, choices=DOC_TYPE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    generated_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.get_doc_type_display()} by {self.user}"


# Module no . 4 Legal Document Generator Model
class LegalDocTemplate(models.Model):
    DOC_TYPE_CHOICES = [
        ('rent_agreement', 'Rent Agreement'),
        ('affidavit', 'Affidavit'),
        ('nda', 'Non-Disclosure Agreement'),
        # Add more as needed
    ]
    doc_type = models.CharField(max_length=32, choices=DOC_TYPE_CHOICES, unique=True)
    title = models.CharField(max_length=128)
    short_description = models.TextField()
    fields_json = models.TextField(help_text="JSON describing form fields and labels")
    template_text = models.TextField(help_text="Use {{field_name}} for placeholders")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Example: If you have a document generation instance model that stores user relation,
# make sure to use settings.AUTH_USER_MODEL for ForeignKey 

class LegalGeneratedDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doc_template = models.ForeignKey(LegalDocTemplate, on_delete=models.CASCADE)
    filled_data = models.JSONField(null=True, blank=True)
    generated_pdf = models.FileField(upload_to='generated_docs/', null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_template.title} by {self.user.username} at {self.generated_at}"



#Module no . 3 Chat with a legal bot
class LegalChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_query = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.timestamp.strftime('%d-%b-%Y %H:%M')}"




