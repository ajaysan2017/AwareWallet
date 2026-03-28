from django import forms
from django.core.exceptions import ValidationError
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError('Category name is required.')
        if len(name) < 2:
            raise ValidationError('Category name must be at least 2 characters.')
        if len(name) > 100:
            raise ValidationError('Category name cannot exceed 100 characters.')
        return name

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        type_ = cleaned_data.get('type')

        if name and type_ and self.user:
            qs = Category.objects.filter(
                user=self.user,
                name__iexact=name,
                type=type_
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    f'A {type_} category named "{name}" already exists.'
                )
        return cleaned_data
