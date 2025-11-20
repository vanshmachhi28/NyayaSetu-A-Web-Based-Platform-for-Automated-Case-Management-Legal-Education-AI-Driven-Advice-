from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from cases.models import *
# Register your models here.

admin.site.register(Case)
admin.site.register(Lawyer)
admin.site.register(Client)

# change in the dashboard


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('role',)}),)

admin.site.register(CustomUser, CustomUserAdmin)




#Contact_Us fetched from the client side and shown here
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','message',   'submitted_at']
    readonly_fields = ['name', 'email', 'message', 'submitted_at']

admin.site.register(ContactQuery, ContactQueryAdmin)



#Module_10 Quiz Module
@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "correct", "added_at")
    search_fields = ("question_text",)
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "selected", "correct", "attempted_at")
@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "completed_at")




#Module no . 9 Search & Filter 
@admin.register(UserSearchLog)
class UserSearchLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'category', 'results_count', 'search_time')
    search_fields = ('user__username', 'query', 'category')
    list_filter = ('category',)



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'author', 'status', 'created_at')
    search_fields = ('question_text', 'author__username', 'subject')
    list_filter = ('subject', 'status', 'created_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'responder', 'created_at')
    search_fields = ('answer_text', 'responder__username')
    list_filter = ('created_at',)



#Module no . 6 LegalAwareness
@admin.register(LegalArticle)
class LegalArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']



#Module no . 5 Legal Learning (Students):
@admin.register(LegalLearnResource)
class LegalLearnResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_at')
    list_filter = ('topic',)
    search_fields = ('title', 'content', 'description')

    


#Module no . 4 legal Document Generator
@admin.register(LegalDocTemplate)
class LegalDocTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'created_at')
    search_fields = ('title', 'doc_type', 'short_description')

@admin.register(LegalGeneratedDocument)
class LegalGeneratedDocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_template', 'user', 'generated_at')
    list_filter = ('generated_at',)
    search_fields = ('doc_template__title', 'user__username')

    




#Module no . 3 Chat with a Legal Bot
@admin.register(LegalChatMessage)
class LegalChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'user_query')
    search_fields = ('user__username', 'user_query', 'bot_response')
    list_filter = ('timestamp',)




