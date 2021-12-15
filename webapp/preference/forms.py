from django import forms


class PreferenceForm(forms.Form):
    close_when_rainy = forms.ChoiceField(
        label="Close window when rainy?",
        choices=[(True, "Yes"), (False, "No")],
        widget=forms.RadioSelect()
    )
    close_when_dry = forms.ChoiceField(
        label="Close window when dry?",
        choices=[(True, "Yes"), (False, "No")],
        widget=forms.RadioSelect()
    )
    temp_max = forms.FloatField(
        label="Max temperature",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    temp_min = forms.FloatField(
        label="Min temperature",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    close_when_windy = forms.ChoiceField(
        label="Close window when windy?",
        choices=[(True, "Yes"), (False, "No")],
        widget=forms.RadioSelect()
    )
    diff_temp = forms.IntegerField(
        label="Temperature difference",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    diff_hum = forms.IntegerField(
        label="Humidity difference",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    def clean_close_when_rainy(self):
        if self.cleaned_data["close_when_rainy"] == "True":
            return True
        else:
            return False

    def clean_close_when_windy(self):
        if self.cleaned_data["close_when_windy"] == "True":
            return True
        else:
            return False

    def clean_close_when_dry(self):
        if self.cleaned_data["close_when_dry"] == "True":
            return True
        else:
            return False
