from django.contrib import admin
from .models import Label, BackgroundImage

class BackgroundImageInline(admin.TabularInline):
    model = BackgroundImage
    extra = 1  # Number of empty forms to display initially

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [BackgroundImageInline]
