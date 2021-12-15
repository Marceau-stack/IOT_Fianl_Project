from django.shortcuts import render, redirect
from .models import Preference
from .forms import PreferenceForm

# Create your views here.


def get_preference(request):
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
        preference = Preference.objects(username=username)[0]
        context = {
            "close_when_rainy": "Yes" if preference.close_when_rainy else "No",
            "close_when_dry": "Yes" if preference.close_when_dry else "No",
            "max_temp": str(preference.temp_max) + chr(176) + "C",
            "min_temp": str(preference.temp_min) + chr(176) + "C",
            "close_when_windy": "Yes" if preference.close_when_windy else "No",
            "diff_temp": str(preference.diff_temp) + chr(176) + "C",
            "diff_hum": str(preference.diff_hum) + "%"
        }
    return render(request, "preference/preference.html", context)


def update_preference(request):
    username = request.user.username
    preference = Preference.objects(username=username)[0]
    if request.method == "POST":
        preference_form = PreferenceForm(request.POST)
        if preference_form.is_valid():
            close_when_rainy = preference_form.cleaned_data["close_when_rainy"]
            close_when_dry = preference_form.cleaned_data["close_when_dry"]
            close_when_windy = preference_form.cleaned_data["close_when_windy"]
            temp_max = preference_form.cleaned_data["temp_max"]
            temp_min = preference_form.cleaned_data["temp_min"]
            diff_temp = preference_form.cleaned_data["diff_temp"]
            diff_hum = preference_form.cleaned_data["diff_hum"]
            preference.update(
                close_when_rainy=close_when_rainy,
                close_when_dry=close_when_dry,
                close_when_windy=close_when_windy,
                temp_max=temp_max,
                temp_min=temp_min,
                diff_temp=diff_temp,
                diff_hum=diff_hum
            )
            return redirect("preference")
    else:
        preference_form = PreferenceForm(
            initial={
                "close_when_rainy": preference.close_when_rainy,
                "close_when_dry": preference.close_when_dry,
                "close_when_windy": preference.close_when_windy,
                "temp_max": preference.temp_max,
                "temp_min": preference.temp_min,
                "diff_temp": preference.diff_temp,
                "diff_hum": preference.diff_hum
            }
        )
    context = {
        "preference_form": preference_form,
    }
    return render(request, "preference/preference_update.html", context)
