class Line:
    def __init__(self):
        self.f: str = ''
        self.t: str = ''
        self.departure: str = ''
        self.arrival: str = ''
        self.vehicle: str = ''
        self.vehicle_id: str = ''
        self.walk_duration: str = ''
        self.delay: str = ''
        self.platform: str = ''
        self.date: str = ''
        self.is_walk: bool = False

    def __repr__(self):
        if self.is_walk:
            return u'[Walk] {0}'.format(self.walk_duration)

        delay = ' ({0} delay)'.format(self.delay) if self.delay else ''
        platform = f' {self.platform}' if self.platform else ''

        return u'[{0} {1}]{2} {3} {4} -> {5} {6}{7}'.format(
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
