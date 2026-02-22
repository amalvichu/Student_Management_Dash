from django import forms
from .models import Student, Achievement

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'

class StudentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'register_number', 'course', 'batch', 'department', 'status']

class AchievementForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['student', 'category', 'title', 'description', 'proof', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }