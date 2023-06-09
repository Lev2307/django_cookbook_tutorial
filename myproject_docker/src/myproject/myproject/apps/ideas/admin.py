from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from myproject.apps.core.admin import get_multilingual_field_names
from .models import Idea, IdeaTranslations
from myproject.apps.core.admin import LanguageChoicesForm
from myproject.apps.categories1.models import Category

class IdeaTranslationsForm(LanguageChoicesForm):
    class Meta:
        model = IdeaTranslations
        fields = "__all__"

class IdeaTranslationsInline(admin.StackedInline):
    form = IdeaTranslationsForm
    model = IdeaTranslations
    extra = 0

class IdeaForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        label=_("Categories"),
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )
    class Meta:
        model = Idea
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["picture"].widget.template_name = "core/widgets/image.html"

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    form = IdeaForm
    inlines = [IdeaTranslationsInline]
    fieldsets = [
        (_("Author and Category"), {"fields": ["author", "categories"]}),
        (_("Title and Content"), {"fields": ["title", "content", "picture"]}),
        (_("Ratings"), {"fields": ["rating"]}),
    ]