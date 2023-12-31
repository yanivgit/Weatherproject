import flask
import requests
import tools
import datetime
import db

app = flask.Flask(__name__)

#saves the date
current_datetime = datetime.datetime.now()
current_date =(str(current_datetime.day)+"." + str(current_datetime.month)+"."+str(current_datetime.year)) 

@app.route("/")
def root():
    return flask.render_template('product.html')


@app.route("/weather", methods=['POST'])
def weather():
    #  location inputted by user in html file.
    location = flask.request.form['location']
    print("loction is" + location)

    #  Making url for api use.
    first_api = f'https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json'

    #  Analysing api for next api use(lang,long)
    try:
        data = requests.get(first_api).json()['results']
    except Exception:
        return flask.render_template('product.html', not_found="Couldn't find location, try again")

    else:
        
        latitude = "{:.2f}".format(data[0]['latitude']) 
        longitude = "{:.2f}".format(data[0]['longitude']) 
        country = data[0]['country']
        print("contry is " + country)

    #  using 2nd api for weather detail
    second_api = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,&current_weather=true'
    buffer = requests.get(second_api).json()
    print("the buffer is " + str(buffer))
    #  getting temps from buffer into new list(9am,9pm) and append list with temp now at the end
    temp = buffer['hourly']['temperature_2m'][9::12]
    print("temp is" + str(temp))
    current_temp = buffer['current_weather']['temperature']
    print("current_temp is" + str(current_temp))
    temp.append(current_temp)
    #  list for humidity and avg which is a list with avg humidity for a day(7 elements for each day)
    humidity = buffer['hourly']['relativehumidity_2m']
    print("humidity is " + str(humidity))
    avg_humidity = ["{:.2f}".format(sum(humidity[i * 24: (i + 1) * 24]) / 24) for i in range(7)]
    print("the avg_humidity is" + str(avg_humidity))
    #  sky state info(rain, clear, thunderstorm, etc...)
    weathercode = buffer['current_weather']['weathercode']
    print("this is wther code" + str(weathercode))

    #  day or night, which is used to change image according to the output of it
    is_day = buffer['current_weather']['is_day']
    print ("the is_day is " + str(is_day))


    # create a dictionary to entre the db
     
    data_for_db = {"country":country,"current_temp": current_temp,"date":current_date}
    push_to_db= db.connect_to_db().insert_one(data_for_db)

    #  if location is country put nothing on html page
    if location.lower() == country.lower():
        country = ""



    #  returning rendered template of rusult.html- the weather page
    return flask.render_template('rusult.html', location=location, country=country, date=tools.datetime.date.today(), weather=temp, days=tools.list_of_days(), humidity=avg_humidity, weather_state=tools.get_weather_state(weathercode), is_day=tools.get_image(is_day))
     



@app.route("/graphic", methods=['GET'])
def result():
    return flask.render_template('app.html')

@app.route("/about", methods=['GET'])
def about():
    return flask.render_template('user.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')



