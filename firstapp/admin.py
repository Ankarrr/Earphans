from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Earphone

# class QuestionAdmin(admin.ModelAdmin):
#    fields = ['pub_date', 'question_text']

# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # define the order of fields in admin page
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    # This tells Django "Choice objects are edited on the Question admin page. By default, provide enough fields for 3 choices."
    inlines = [ChoiceInline]
    # change the displays for all the questions in the system.
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

class EarphoneAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['earphone_name']}),
        (None,               {'fields': ['brand_name']}),
        (None,               {'fields': ['earphone_description']}),
        (None,               {'fields': ['price']}),
        (None,               {'fields': ['earphone_image']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    list_display = ('earphone_name', 'brand_name', 'price', 'pub_date')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Earphone, EarphoneAdmin)
