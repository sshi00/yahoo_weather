import lxml.html
import requests
import datetime
import yaml
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

with open('config.yml') as f:
    config = yaml.load(f,Loader=yaml.SafeLoader)['server']

def connect() -> '':
    #connect()引数 config
    return psycopg2.connect(f'host={config["database"]["host"]} port={config["database"]["port"]} dbname={config["database"]["dbname"]} password={config["database"]["password"]}')

def get_weather(weather_url:'URL') -> 'list':
    r = requests.get(weather_url)
    html = lxml.html.fromstring(r.text)

    place = []
    weather_forecast = []
    pro_pre = []
    high_tem = []
    low_tem = []

    for i in html.cssselect('div.mapJp ul li'):
        place.append(i.cssselect('dt.name')[0].text)
        high_tem.append(int(i.cssselect('em.high')[0].text))
        low_tem.append(int(i.cssselect('em.low')[0].text))
        pro_pre.append(int(i.cssselect('p.precip')[0].text.replace('%','')))
        weather_forecast.append(i.cssselect('img')[0].get('alt'))

    yahoo_weather = {'place':place,'weather':weather_forecast,'pro_pre':pro_pre,'high_tem':high_tem,'low_tem':low_tem}

    return yahoo_weather

if __name__ == '__main__':
    yahoo_weather = get_weather(config['yahoo_weather_url'])
    weather_df = pd.DataFrame({'date':pd.to_datetime(datetime.date.today()),'place':yahoo_weather['place'],'weather':yahoo_weather['weather'],'pro_pre':yahoo_weather['pro_pre'],'high_tem':yahoo_weather['high_tem'],'low_tem':yahoo_weather['low_tem']})
    engine = create_engine(f'{config["database"]["sql"]}://', creator=connect)
    df.to_sql('yahoo_weather', con=engine, if_exists='append', index=False)
