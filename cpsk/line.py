from .enums import UsualDeparture, Vehicle


class Line:
    def __init__(self):
        self.f: str = ''
        self.t: str = ''
        self.departure: str = ''
        self.arrival: str = ''
        self.vehicle: Vehicle = None
        self.vehicle_id: str = ''
        self.walk_duration: str = ''
        self.delay: str = ''
        self.platform: str = ''
        self.date: str = ''
        self.usual_departure: UsualDeparture = None

    def __repr__(self):
        if self.vehicle == Vehicle.WALK:
            return '[WALK] {0}'.format(self.walk_duration)

        delay = ' ({0} delay)'.format(self.delay) if self.delay else ''
        platform = f' {self.platform}' if self.platform else ''

        return '[{0} {1}]{2} {3} {4} -> {5} {6}{7}'.format(
            self.vehicle,
            self.vehicle_id,
            platform,
            self.f,
            self.departure,
            self.t,
            self.arrival,
            delay,
        )

    def __str__(self):
        return self.__repr__()
