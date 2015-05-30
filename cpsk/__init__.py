# -*- coding: utf-8 -*-

import requests
import datetime
from lxml import html

CPSK_URL = 'http://cp.atlas.sk/{0}/spojenie/'


class Line(object):
    def __init__(self):
        self.f = ''
        self.t = ''
        self.departure = ''
        self.arrival = ''
        self.vehicle = ''
        self.walk_duration = ''
        self.delay = ''

    def __repr__(self):
        if self.vehicle == 'Presun':
            return '{0}-> {1}{2}'.format(self.f, self.t, self.walk_duration)
        return '[{0}] {1} {2} -> {3} {4}{5}'.format(self.vehicle,
                                                    self.f,
                                                    self.departure,
                                                    self.t,
                                                    self.arrival,
                                                    self.delay)


class Drive(object):
    def __init__(self):
        self.duration = None
        self.distance = None

        self.lines = []

    def __repr__(self):
        return ('{0} ({1}, {2})'.format(' >> '.join(map(str, self.lines)),
                                        self.duration,
                                        self.distance)).encode('utf-8')


def get_routes(departure, dest, vehicle='vlakbus', time='', date=''):
    if time == '':
        time = datetime.datetime.now().strftime('%H:%M')

    if date == '':
        date = datetime.datetime.now().strftime('%d.%m.%Y')

    try:
        req = requests.get(CPSK_URL.format(vehicle),
                           params={'date': date, 'time': time, 'f': departure,
                                   't': dest, 'fc': 1, 'tc': 1,
                                   'submit': 'true'})
    except:
        return False

    tree = html.fromstring(req.text)
    html_tables = tree.xpath('//div[@id="main-res-inner"]/table/tbody')
    routes = []

    for table in html_tables:
        drive = Drive()
        datalen = len(table.xpath('./tr'))

        for i in range(1, datalen-1):
            line = Line()
            trf = './tr[' + str(i) + ']'
            trt = './tr[' + str(i+1) + ']'
            line.f = table.xpath(trf + '/td[3]/text()')[0]
            line.t = table.xpath(trt + '/td[3]/text()')[0]
            line.departure = table.xpath(trf + '/td[5]/text()')[0]
            line.arrival = table.xpath(trt + '/td[4]/text()')[0]
            line.vehicle = table.xpath(trf + '/td[7]/img[1]')[0] \
                                .get('title').replace('Autobus', 'Bus')
            if line.vehicle == 'Presun':
                line.walk_duration = table.xpath(trf + '/td[7]/text()')[0] \
                                        .replace('Presun asi ', '')

            delay = table.xpath(trf + '/td[7]/div[1]/' +
                                'span[@class!="nodelay"]/text()')
            if delay and delay[0] is not u'Aktuálne bez meškania':
                mins = delay[0].replace(u'Aktuálne meškanie ', '') \
                               .replace(u' minúty', '') \
                               .replace(u' minúta', '') \
                               .replace(u' minút', '')

                minstr = 'minutes' if mins is not '1' else 'minute'

                line.delay = ' ({0} {1} delay)'.format(mins, minstr)

            drive.lines.append(line)

        drive.duration = table.xpath('./tr[' + str(datalen) +
                                     ']/td[3]/p/strong[1]/text()')[0]
        drive.distance = table.xpath('./tr[' + str(datalen) +
                                     ']/td[3]/p/strong[2]/text()')[0]

        routes.append(drive)

    return routes
