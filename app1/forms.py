# forms.py

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']  # Exclude the 'user' field from the form

class ExpenseForm(forms.Form):
    expense = forms.DecimalField(label='Expense')