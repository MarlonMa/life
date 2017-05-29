#!/usr/bin/env python
"""Program to get weather of in the future week, send the result to mailbox.
"""

import requests
from bs4 import BeautifulSoup
from string import Template
from datetime import date
from toolbox import get_url, send_mail


def get_weather(weather_res):
    soup = BeautifulSoup(weather_res.text, 'html.parser')
    for weather in soup.select('.sky'):
        weather_dict = {}
        weather_dict['date'] = weather.select('h1')[0].text
        weather_dict['wea'] = weather.select('.wea')[0].text
        weather_dict['tem'] = weather.select('.tem')[0].text.strip()
        win = weather.select('.win')[0]
        weather_dict['win'] = win.text.strip()
        weather_dict['win_direction'] = ','.join(
            [direction['title'] for direction in win.select('span')])
        yield weather_dict


def generate_weather_report(res):
    subject = 'WeatherReport (%s)' % date.today().strftime('%Y-%m-%d')
    tcaption = '<caption>Weather</caption>'
    thead = '<thead><th>Date</th><th>Weather</th><th>Temperature</th><th>Wind(Direction)</th></thead>'
    tr_template = Template(
        '<tr><td>$date</td><td>$wea</td><td>$tem</td><td>$win($win_direction)</td></tr>')
    tbody = '<tbody>'
    for weather in get_weather(res):
        tbody += tr_template.substitute(weather)
    tbody += '</tbody>'
    table = '<table border="1" cellspacing="0">' + \
        tcaption + thead + tbody + '</table>'
    content = '<html><body>%s</body><html>' % table
    return subject, content


if __name__ == '__main__':
    weather_url = 'http://www.weather.com.cn/weather/101010100.shtml'
    res = get_url(weather_url)
    subject, content = generate_weather_report(res)
    # password is the mail account password
    send_mail(subject, content, password='******')
