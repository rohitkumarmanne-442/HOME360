from django.contrib import admin
from .models import Feedback
from .models import *

# Register your models here.
admin.site.register(Status)
admin.site.register(Contact)
admin.site.register(ID_Card)
admin.site.register(Order)
admin.site.register(Service_Category)
admin.site.register(Service)
admin.site.register(Customer)
admin.site.register(Service_Man)
admin.site.register(Total_Man)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'submitted_at', 'is_addressed')
    list_filter = ('rating', 'is_addressed', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('submitted_at',)
    actions = ['mark_as_addressed']

    def mark_as_addressed(self, request, queryset):
        queryset.update(is_addressed=True)
    mark_as_addressed.short_description = "Mark selected feedback as addressed"

