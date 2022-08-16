import datetime
from typing import List, Optional

import requests
from lxml import html

from .drive import Drive
from .line import Line
from .settings import CPSK_URL


def _get_vehicle_type(vehicle: str) -> str:
    if 'vlak' in vehicle:
        return 'Train'
    elif 'rýchlik' in vehicle:
        return 'Fast Train'
    elif 'autobus' in vehicle:
        return 'Bus'
    else:
        return vehicle


def get_routes(
    departure: str,
    destination: str,
    vehicle: str ='vlakbus',
    time: Optional[str] = None,
    date: Optional[str] = None,
    direct: bool = False,
) -> List[Drive]:
    """
    Query cp.sk with given parameters and parse the results.

    Args:
        departure: Place to depart from
        destination: Place to arrive to
        vehicle: One of "bus", "vlak" (train), "vlakbus" (train or bus),
        time (optional): Time of departure in format "HH:MM" (defaults to now)
        date (optional): Date of departure in format "dd.mm.YYYY" (defaults to today)
        direct (optional): Whether to search just direct routes

    Returns:
        list of available drives from departure city to destination
    """

    if time is not None:
        time = datetime.datetime.now().strftime('%H:%M')

    if date is not None:
        date = datetime.datetime.now().strftime('%d.%m.%Y')

    req = requests.get(
        CPSK_URL.format(vehicle),
        params={
            'date': date, 'time': time, 'f': departure,
            't': destination, 'submit': 'true',
            'direct': 'true' if direct else 'false',
        }
    )

    tree = html.fromstring(req.text)

    connections = tree.xpath('//div[@class="connection-list"]')[0]
    connection_list = connections.xpath('div[contains(@class, "connection")]')

    drives: List[Drive] = []
    for conn in connection_list:
        drive = Drive()

        drive_head = conn.xpath('div[@class="connection-head"]')[0]
        drive_info = drive_head.xpath(
            'div[@class="date-total"]/label/p[contains(@class, "total")]/strong'
        )
        drive.duration = drive_info[0].text
        try:
            drive.distance = drive_info[1].text
        except IndexError:
            drive.distance = 'Distance unknown'

        conn_details = conn.xpath('div[@class="connection-details "]')[0]
        html_lines = conn_details.xpath('div/div')

        for html_line in html_lines:
            line = Line()
            walk_info = html_line.xpath('div[contains(@class, "walk")]')
            if walk_info:
                walk_text = walk_info[0].text_content().strip()
                walk_line = Line()
                walk_line.is_walk = True
                walk_line.walk_duration = walk_text.replace('Presun asi ', '')
                drive.lines.append(walk_line)

            from_html, to_html = html_line.xpath('ul/li')

            departure_info = from_html.xpath('p')
            line.departure = departure_info[0].text
            line.f = departure_info[1].xpath('strong[contains(@class, "name")]')[0].text
            platform = departure_info[1].xpath('span/span')
            if platform:
                line.platform = platform[0].text

            arrival_info = to_html.xpath('p')
            line.arrival = arrival_info[0].text
            line.t = arrival_info[1].xpath('strong[contains(@class, "name")]')[0].text

            vehicle_info = html_line.xpath('a[@class="title"]/div/div')[0]
            line.vehicle_id = vehicle_info.xpath('h3/span')[0].text
            line.vehicle = _get_vehicle_type(vehicle_info.xpath('img')[0].attrib['alt'])

            delay_info = html_line.xpath('span/a[contains(@class, "delay-bubble")]')
            if delay_info:
                delay = delay_info[0].text
                if delay != 'Aktuálne bez meškania':
                    mins = delay.replace(
                        'Aktuálne meškanie ', ''
                    ).replace(
                        ' minúty', ''
                    ).replace(
                        ' minútu', ''
                    ).replace(
                        ' minút', ''
                    )
                    minstr = 'mins' if mins != '1' else 'min'
                    line.delay = '{0} {1}'.format(mins, minstr)

            drive.lines.append(line)

        drives.append(drive)

    return drives
