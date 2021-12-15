from django import forms
from datetime import datetime


class DateForm(forms.Form):
    date = forms.DateField(
        label="Date",
        initial=datetime.now().date,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "onchange": "this.form.submit()",
                "id": "date_input",
                "class": "form-control-plaintext col-2",
            }
        )
    )
