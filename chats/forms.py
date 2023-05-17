from django import forms


class ThreadForm(forms.Modelform):
    def clean(self):
        super(ThreadForm, self).clean
