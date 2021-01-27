import requests
from datetime import datetime
from bs4 import BeautifulSoup

global APP_ID
APP_ID = '8931f8efdec8d4f859031d9cf5666826'


#Checking leap year
def is_year_leap(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

#Parse
def get_json(name_city):
    global APP_ID
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(name_city,APP_ID)
    r = requests.get(url)
    return r.json()

def get_info(json):
    data = {'Temperature':json['main']['feels_like'],'Humidity':json['main']['humidity'],'Wind_speed':json['wind']['speed'], 'Clouds':json['clouds']['all'], 'Sunrise':json['sys']['sunrise'], 'Sunset':json['sys']['sunset']}
    return data

#Return temperature in Celsius
def convertate_to_Celsius(temperature):
    CelsiusTemperature = round(temperature - 273,1)
    return CelsiusTemperature

def month_day(days, year,date):
    if days < 32:
        date['dd'] = days
        date['mm'] = 1
        return date
    else:
        days -= 31
        date['mm']+=1

    if is_year_leap(year):
        days -= 29
    else:
        days -= 28

    date['mm']+= 1


    while days > 31 and date['mm'] != 8:
        if date['mm'] % 2 ==0:
            days -= 30
        else:
            days -= 31

        date['mm']+= 1


    while days > 31:
        if date['mm'] % 2 ==0:
            days -= 31
        else:
            days -= 30

        date['mm']+= 1

    date['dd'] = days+1
    date['mm']+=1

    return date



#Return date with time
def converate_unixTime(time):
    date = {'yy': 0, 'mm': 0, 'dd': 0, 'hh': 0, 'min': 0}
    year = 31536000
    leap_year = year + 86400
    current_year = 1970

    while time > leap_year:
        if(is_year_leap(current_year)):
            time-=leap_year
            current_year+=1
        else:
            time-=year
            current_year+=1

    date['yy'] = current_year
    days = time // 86400

    time = time - days * 86400
    date = month_day(days, current_year,date)

    date['hh'] = time // 3600
    time = time - date['hh']*3600

    date['min'] = time // 60
    date['dd'] = datetime.now().day
    utc = datetime.now() - datetime.utcnow()

    DateTime = datetime(date['yy'],date['mm'],date['dd'],date['hh'],date['mm'])
    DateTime += utc
    date['yy'] = DateTime.year
    date['mm'] = DateTime.month
    date['dd'] = DateTime.day
    date['hh'] = DateTime.hour
    date['mm'] = DateTime.minute
    return date



class Prediction(object):
    """docstring for Prediction"""

    def __init__(self,city):
        json_object = get_json(city)
        data = get_info(json_object)
        self.city = city
        self.temperature = data['Temperature']
        self.humidity = data['Humidity']
        self.wind_speed = data['Wind_speed']
        self.clouds = data['Clouds']
        self.sunrise = converate_unixTime(data['Sunrise'])
        self.sunset = converate_unixTime(data['Sunset'])
        self.data = data


    def get_humidity(self):
        return str(self.humidity) + '%'

    def get_temperature(self):
        return str(convertate_to_Celsius(self.temperature)) + ' C'

    def get_wind_speed(self):
        return str(self.wind_speed) + 'm/s'

    def get_clouds(self):
        return str(self.clouds) + '%'

    def get_sunrise(self):
        return """{}-{}-{}
{}:{}""".format(self.sunrise['yy'],self.sunrise['mm'],self.sunrise['dd'],self.sunrise['hh'],self.sunrise['min'])

    def get_sunset(self):
        return """{}-{}-{}
{}:{}""".format(self.sunset['yy'],self.sunset['mm'],self.sunset['dd'],self.sunset['hh'],self.sunset['min'])



def make_prediction(obj):
        print()
        print(obj.city)
        print("Temperature "+ obj.get_temperature())
        print("Humidity "+ obj.get_humidity())
        print("Wind speed "+ obj.get_wind_speed())
        print("Clouds "+ obj.get_clouds())
        print("Sunrise(UTC):")
        print(obj.get_sunrise())
        print("Sunset(UTC):")
        print(obj.get_sunset())
        print()


def make_prediction_db(obj):
    res = []
    res.append(obj.city)
    res.append(obj.get_temperature())
    res.append(obj.get_humidity())
    res.append(obj.get_clouds())
    res.append(str(datetime.now()).split('.')[0])
    return res

def make_prediction2(obj):
    res = {}
    res['Name'] = obj.city
    res['Temperature'] = obj.get_temperature()
    res['Humidity'] = obj.get_humidity()
    res['Wind_speed'] = obj.get_wind_speed()
    res['Clouds'] = obj.get_clouds()
    res['Sunrise'] = obj.get_sunrise()
    res['Sunset'] = obj.get_sunset()
    return res

#Main function
def main():
    city = input("Enter city name: ")

    predict = Prediction(city)


    make_prediction(predict)




if __name__ == '__main__':
    main()
