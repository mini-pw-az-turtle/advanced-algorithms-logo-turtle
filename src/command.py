from enum import Enum


        
class CommandType(Enum):
    MOVE_FORWARD = 'fd'
    MOVE_BACKWARDS = 'bk'
    RIGHT_TURN = 'rt'
    LEFT_TURN = 'lt'
    PEN_DOWN = 'pendown'
    PEN_UP = 'penup'

class Command:
    command_type: CommandType
    value: int
    
    def __init__(self, command_type_value: CommandType, value: int = None):
        self.command_type = CommandType(command_type_value)
        self.value = value
        
    def __repr__(self) -> str:
        return f"{self.command_type.name}, value: {self.value}"