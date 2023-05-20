import datetime


def list_of_days():
    """
    Returning a list containing shortcut week names(sun,mon,tue,etc...)
    last Item of the list will be full current day name
    """
    today = datetime.date.today()
    #  today + datetime.timedelta(days=x) generate datetime object x days from today
    list_short = [day.strftime('%a') for day in (today + datetime.timedelta(days=x) for x in range(7))]
    list_full = [day.strftime('%A') for day in (today + datetime.timedelta(days=x) for x in range(7))]
    return list_short + list_full


def get_weather_state(code):
    """
    Function getting code from program and returns weather state
    """
    dict_weather = {0: "Clear", (1, 2, 3): "Cloudy", (45, 48): "Fogy", (61, 63, 66): "Rainy",
                         (65, 67): "Heavy Rain", (71, 73, 75): "Snowy", (80, 81, 82): "Rain Showers",
                         (85, 86): "Snow Showers", (95, 96, 99): "Thunderstorm"}
    new_dict = {}

    #  create new dictionary with each element in those tuples, get own key with the value.
    for key, value in dict_weather.items():
        if isinstance(key, tuple):
            for k in key:
                new_dict[k] = value
        else:
            new_dict[key] = value
    return new_dict[code]


def get_image(is_day):
    """
    Function return right image
    day or night accordingly
    """
    if is_day == 0:
        return "/static/images/day.jpg"
    else:
        return "/static/images/night.jpeg"


