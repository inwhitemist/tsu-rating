from django.contrib import admin
from .models import Teacher, Review, Action

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'rating', 'created_at')
    fields = ('name', 'department', 'rating', 'image', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Review)
admin.site.register(Action)
