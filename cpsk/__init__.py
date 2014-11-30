import requests
import datetime
from lxml import html

CPSK_URL = 'http://cp.atlas.sk/{0}/spojenie/'

class Drive(object):
    def __init__(self):
        self.departure = None
        self.line_change = None
        self.dest = None

        self.departure_time = None
        # lc means line change
        self.lc_arr_time = None
        self.lc_dep_time = None
        self.arrival_time = None

        self.duration = None
        self.distance = None

        self.vehicles = []

    def __repr__(self):
        if self.line_change is not None:
            return "[{0}] {1} {2} >> {3} {4} > {5} >> {6} {7} ({8}, {9})" \
                                    .format(self.vehicles[0],
                                            self.departure.encode("utf-8"),
                                            self.departure_time,
                                            self.line_change.encode("utf-8"),
                                            self.lc_arr_time,
                                            self.lc_dep_time,
                                            self.dest.encode("utf-8"),
                                            self.arrival_time,
                                            self.duration,
                                            self.distance)
        else:
            return "[{0}] {1} {2} >> {3} {4} ({5}, {6})" \
                                    .format(self.vehicles[0],
                                            self.departure.encode("utf-8"),
                                            self.departure_time,
                                            self.dest.encode("utf-8"),
                                            self.arrival_time,
                                            self.duration,
                                            self.distance)


def get_routes(departure, dest, vehicle='vlakbus', time='', date=''):
    if time == '':
        time = datetime.datetime.now().strftime("%H:%M")

    if date == '':
        date = datetime.datetime.now().strftime("%d.%m.%Y")

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
        if datalen == 4:
            drive.line_change = table.xpath('./tr[2]/td[3]/text()')[0]
            drive.lc_arr_time = table.xpath('./tr[2]/td[4]/text()')[0]
            drive.lc_dep_time = table.xpath('./tr[2]/td[5]/text()')[0]

        drive.departure = table.xpath('./tr[1]/td[3]/text()')[0]
        drive.dest = table.xpath('./tr[' + str(datalen-1) + ']/td[3]/text()')[0]
        drive.departure_time = table.xpath('./tr[1]/td[5]/text()')[0]
        drive.arrival_time = table.xpath('./tr[' + str(datalen-1) + \
                                            ']/td[4]/text()')[0]

        drive.vehicles.append(table.xpath('./tr[1]/td[7]/img[1]')[0] \
                                .get('title').replace('Autobus', 'Bus'))

        drive.duration = table.xpath('./tr[' + str(datalen) + \
                                        ']/td[3]/p/strong[1]/text()')[0]
        drive.distance = table.xpath('./tr[' + str(datalen) + \
                                        ']/td[3]/p/strong[2]/text()')[0]

        routes.append(drive)

    return routes
