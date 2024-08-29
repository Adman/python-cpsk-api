from enum import StrEnum


class Vehicle(StrEnum):
    BUS = "BUS"
    TRAIN = "TRAIN"
    TRAM = "TRAM"
    UNKNOWN = "UNKNOWN"
    WALK = "WALK"


class UsualDeparture(StrEnum):
    ON_TIME = "ON TIME"
    DELAYED = "DELAYED"
