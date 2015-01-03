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

    def __repr__(self):
        if self.vehicle == 'Presun':
            return self.f + '-> ' + self.t  + self.walk_duration
        return '[' + self.vehicle + '] ' + self.f + ' ' + self.departure \
                + ' -> ' + self.t + ' ' + self.arrival


class Drive(object):
    def __init__(self):
        self.duration = None
        self.distance = None

        self.lines = []

    def __repr__(self):
        return ' >> '.join(map(str,self.lines)) + \
               ' ({0}, {1})'.format(self.duration, self.distance)


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
            drive.lines.append(line)

        drive.duration = table.xpath('./tr[' + str(datalen) + \
                                        ']/td[3]/p/strong[1]/text()')[0]
        drive.distance = table.xpath('./tr[' + str(datalen) + \
                                        ']/td[3]/p/strong[2]/text()')[0]

        routes.append(drive)

    return routes
