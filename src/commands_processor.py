import math
from segment import *
from command import *

class CommandsProcessor:
    
    def processCommands(self, commands: list[Command]) -> list[Segment]:
        edges : list[Segment] = []
        currentPosition = Node(0,0)
        relativeAngle = 0 
        penDown = True
        for command in commands:
            start = currentPosition
            if(command.command_type in [CommandType.MOVE_FORWARD, CommandType.MOVE_BACKWARDS]):
                currentPosition = self._processMove(command, start, relativeAngle)
                if(penDown): 
                    edges.append(Segment(start, currentPosition))
            elif(command.command_type is CommandType.RIGHT_TURN):
                relativeAngle = (relativeAngle + command.value) % 360
            elif(command.command_type is CommandType.LEFT_TURN):
                relativeAngle = (relativeAngle - command.value) % 360
            elif(command.command_type is CommandType.PEN_DOWN):
                penDown = True
            elif(command.command_type is CommandType.PEN_UP):
                penDown = False
        return edges

    def _processMove(self, command: Command, currentPosition : Node, relativeAngle: int):
        radians = math.radians(relativeAngle)
        return self._processMoveForward(command, currentPosition, radians) \
            if command.command_type is CommandType.MOVE_FORWARD \
            else self._processMoveBackwards(command, currentPosition, radians)      
        
    def _processMoveForward(self, command : Command, currentPosition : Node, radians: float) -> Node:
        x = round(currentPosition.x + command.value * math.sin(radians), 4)
        y = round(currentPosition.y + command.value * math.cos(radians), 4)
        return Node(x,y)

    def _processMoveBackwards(self, command : Command, currentPosition : Node, radians: float) -> Node:
        x = round(currentPosition.x - command.value * math.sin(radians), 4)
        y = round(currentPosition.y - command.value * math.cos(radians), 4)
        return Node(x,y)