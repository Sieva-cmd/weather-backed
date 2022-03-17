
from flask import render_template,request

from flask_login import login_required

from app.models import Cities
from ..main import main
import requests 
from app import db



@main.route('/',methods =['GET','POST'])
@login_required
def index():

    if request.method =='POST':
        new_city= request.form.get('city')
        new_city_obj =Cities(city=new_city)
        if new_city:
            db.session.add(new_city_obj)
            db.session.commit()

    cities = Cities.query.all()
 
    api_key ='https://api.openweathermap.org/data/2.5/weather?q={}&appid=e1c34a11142d22d0e932a9f6978a4105&units=metric'

    weather_data =[]


    for city in cities:
            r =requests.get(api_key.format(city.city)).json()
            
           
            climate ={
                'name':city.city ,
                'temperature':r['main']['temp'],
                'description':r['weather'][0]['description'],
                'minimum_temp':r['main']['temp_min'],
                'temp_max':r['main']['temp_max'],
                'feel_like':r['main']['feels_like'],
                'humidity':r['main']['humidity'],
                'pressure':r['main']['pressure'],
                'visibility':r['visibility'],
                'wind':r['wind']['speed'],
                'icon':r['weather'][0]['icon'],
               
                

            }

            weather_data.append(climate)
            lon=r['coord']['lon']
            lat=r['coord']['lat']
            
            # re.sub("[\(\[].*?[\)\]]","",lat)
            # re.sub("[\(\[].*?[\)\]]","",lon)
        
            
            
            
            exclude ="minute,hourly"
            daily_api =f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid=e1c34a11142d22d0e932a9f6978a4105"
            print(daily_api)
            r2 =requests.get(daily_api.format(city=city)).json()
            print(r2)
            days =[]
            nights =[]
            descr =[]

            for i in r2['daily']:
                days.append(round(i['temp']['day'] - 273.15,2))
                nights.append(round(i['temp']['night'] - 273.15,2))
                # print(days)
                # print(nights)

                descr.append(i['weather'][0]['description']+" :" +"\n" +i['weather'][0]['main'])
                print(descr)

                string =f'{city.city} -8 days forecast'
                for i in range(len(days)):
                    if i ==0:
                        string +=f'\n Day {i+1} \n (Today) \n'
                    elif i==1:
                        string+= f'\n Day {i+1} \n (Tomorrow) \n'
                    else:
                        string += f'\n Day {i+1} \n' 
              

                    string += 'Morning: ' +str(days[i]) +"\n" 
                    string += 'Night: ' + str(nights[i]) + "\n"
                    string += '' + str(descr[i]) + "\n" 

                               

   
    return render_template('index.html',weather_data=weather_data,string=string)



