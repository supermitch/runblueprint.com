from django import forms

class PlanForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    weeks = forms.IntegerField(label='Weeks until your race')
