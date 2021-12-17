import enum

class LogMessageType(enum.Enum):
    Debug = 1
    Info = 2
    Critical = 3
    Warning = 4
    Error = 5
    Exception = 6