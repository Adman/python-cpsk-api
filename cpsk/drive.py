class Drive(object):
    def __init__(self):
        self.duration: str = ''
        self.distance: str = ''

        self.lines = []

    def __repr__(self):
        return '{0} ({1}, {2})'.format(
            ' >> '.join(map(str, self.lines)),
            self.duration,
            self.distance,
        )

    def __str__(self):
        return self.__repr__()
