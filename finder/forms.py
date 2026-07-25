from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Interest, ProjectIdea


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email address",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "name@example.test",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Enter your password",
            }
        ),
    )
    error_messages = {
        "invalid_login": (
            "The email address or password is incorrect. Check the demonstration "
            "credentials and try again."
        ),
        "inactive": "This account is inactive.",
    }


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ("name",)
        labels = {"name": "Area of interest"}
        help_texts = {
            "name": "Use a concise subject name, for example Data analysis."
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter an area of interest",
                    "autocomplete": "off",
                }
            )
        }

    def __init__(self, *args, staff_profile, **kwargs):
        super().__init__(*args, **kwargs)
        self.staff_profile = staff_profile
        self.instance.staff_profile = staff_profile

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Use at least two characters.")
        duplicate = Interest.objects.filter(
            staff_profile=self.staff_profile,
            name__iexact=name,
        ).exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError(
                "This area of interest is already on your profile."
            )
        return name


class ProjectIdeaForm(forms.ModelForm):
    class Meta:
        model = ProjectIdea
        fields = ("title", "description")
        labels = {
            "title": "Project title",
            "description": "Project description",
        }
        help_texts = {
            "title": "Use a clear title between 4 and 120 characters.",
            "description": (
                "Explain the proposed work and expected outcome in at least "
                "20 characters."
            ),
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter a descriptive project title",
                    "autocomplete": "off",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Describe the problem, proposed work and intended outcome..."
                    ),
                    "rows": 8,
                }
            ),
        }

    def __init__(self, *args, staff_profile, **kwargs):
        super().__init__(*args, **kwargs)
        self.staff_profile = staff_profile
        self.instance.staff_profile = staff_profile

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 4:
            raise forms.ValidationError("Use at least four characters.")
        return title

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if len(description) < 20:
            raise forms.ValidationError(
                "Provide at least 20 characters so students can understand the idea."
            )
        return description
