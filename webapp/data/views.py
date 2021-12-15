from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from pyecharts.charts import Line
from pyecharts import options as opts
from .models import Weather, History
from .forms import DateForm
import json
from datetime import datetime, timedelta

# Create your views here.

WEATHER = 0
HISTORY = 1


def draw_line(weather_today_list, field_list, series_list):
    timestamp = []
    field_data = {}
    for field in field_list:
        field_data[field] = []
    for weather in weather_today_list:
        timestamp.append(weather.timestamp.strftime("%Y/%m/%d %H:%M:%S"))
        for field in field_list:
            field_data[field].append(weather[field])

    chart = Line().add_xaxis(xaxis_data=timestamp)
    for i in range(len(field_list)):
        chart.add_yaxis(
            series_name=series_list[i],
            y_axis=field_data[field_list[i]],
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=4)
        )
    chart.set_global_opts(
        xaxis_opts=opts.AxisOpts(type_="time", min_interval=0, max_interval=3600 * 24 * 1000)
    )
    return chart


def get_data_list(today, type):
    tomorrow = today + timedelta(days=1)
    if type == WEATHER:
        return Weather.objects(timestamp__gte=today, timestamp__lt=tomorrow).order_by("-timestamp")
    elif type == HISTORY:
        return History.objects(timestamp__gte=today, timestamp__lt=tomorrow).order_by("-timestamp")
    else:
        return "Type Incorrect"


def get_date_form(request):
    today = date_keeper.date

    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            today = form.cleaned_data["date"]
            date_keeper.date = today
    else:
        form = DateForm(initial={"date": today})
    return today, form


def generate_page(request, rows, n_per_page):
    paginator = Paginator(rows, n_per_page)
    if request.method == "POST":
        page_num = 1
    else:
        page_num = request.GET.get('page', 1)
    page_of_rows = paginator.get_page(page_num)
    current_page_num = page_of_rows.number
    page_range = list(range(max(current_page_num - 2, 1), min(current_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    return page_of_rows, page_range


def temperature_list(request):
    today, date_form = get_date_form(request)
    weather_today_list = get_data_list(today, WEATHER)

    table_rows = []
    for weather in weather_today_list:
        table_rows.append([weather.timestamp.time, weather.temp_in, weather.temp_out])

    page_of_rows, page_range = generate_page(request, table_rows, 6)

    chart = draw_line(weather_today_list,
                      field_list=["temp_in", "temp_out"],
                      series_list=["Indoor Temperature", "Outdoor Temperature"])
    context = {
        "page_title": "Temperature",
        "temperature_active": "active",
        "title": "Temperature",
        "form": date_form,
        "chart_option": chart.dump_options_with_quotes(),
        "table_heads": ["Time", "Indoor Temperature", "Outdoor Temperature"],
        "page_of_rows": page_of_rows,
        "page_range": page_range
    }
    return render(request, "data/data_list.html", context)


def humidity_list(request):
    today, date_form = get_date_form(request)
    weather_today_list = get_data_list(today, WEATHER)

    table_rows = []
    for weather in weather_today_list:
        table_rows.append([weather.timestamp.time, weather.hum_in, weather.hum_out])

    page_of_rows, page_range = generate_page(request, table_rows, 6)

    chart = draw_line(weather_today_list,
                      field_list=["hum_in", "hum_out"],
                      series_list=["Indoor Humidity", "Outdoor Humidity"])
    context = {
        "page_title": "Humidity",
        "humidity_active": "active",
        "title": "Humidity",
        "form": date_form,
        "chart_option": chart.dump_options_with_quotes(),
        "table_heads": ["Time", "Indoor Humidity", "Outdoor Humidity"],
        "page_of_rows": page_of_rows,
        "page_range": page_range
    }
    return render(request, "data/data_list.html", context)


def wind_list(request):
    today, date_form = get_date_form(request)
    weather_today_list = get_data_list(today, WEATHER)

    table_rows = []
    for weather in weather_today_list:
        table_rows.append([weather.timestamp.time, weather.wind_speed])

    page_of_rows, page_range = generate_page(request, table_rows, 6)

    chart = draw_line(weather_today_list,
                      field_list=["wind_speed"],
                      series_list=["Wind Speed"])
    context = {
        "page_title": "Wind",
        "wind_active": "active",
        "title": "Wind Speed",
        "form": date_form,
        "chart_option": chart.dump_options_with_quotes(),
        "table_heads": ["Time", "Wind Speed"],
        "page_of_rows": page_of_rows,
        "page_range": page_range
    }
    return render(request, "data/data_list.html", context)


def history_list(request):
    today, date_form = get_date_form(request)
    history_today_list = get_data_list(today, HISTORY)

    table_rows = []
    for history in history_today_list:
        table_rows.append([history.timestamp.time, history.user, history.status, history.reason])

    page_of_rows, page_range = generate_page(request, table_rows, 20)

    context = {
        "user": request.user,
        "page_title": "History",
        "history_active": "active",
        "title": "Window History",
        "form": date_form,
        "no_chart": True,
        "table_heads": ["Time", "User", "Status", "Reason"],
        "page_of_rows": page_of_rows,
        "page_range": page_range
    }
    return render(request, "data/data_list.html", context)


@csrf_exempt
def post_weather(request):
    if request.method == "POST":
        data = json.loads(request.body)
        w = Weather()
        w.timestamp = datetime.now()
        w.wind_speed = data["wind_speed"]
        w.hum_in = data["hum_in"]
        w.hum_out = data["hum_out"]
        w.temp_in = data["temp_in"]
        w.temp_out = data["temp_out"]
        w.save()
        return HttpResponse('200')
    else:
        return HttpResponse('500')


@csrf_exempt
def post_history(request):
    if request.method == "POST":
        data = json.loads(request.body)
        h = History()
        h.timestamp = datetime.now()
        h.status = data["status"]
        h.user = data["user"]
        h.reason = data["reason"]
        h.save()
        return HttpResponse("200")


class DateKeeper:
    def __init__(self):
        self.date = datetime.now().date()


date_keeper = DateKeeper()
