from enum import Enum


class StateEnumn(Enum):
    IDEL = "IDEL"
    LOADING = "LOADING"
    LOADED = "LOADED"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    RETURNING = "RETURNING"
