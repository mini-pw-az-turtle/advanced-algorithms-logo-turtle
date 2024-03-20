import random

from command import Command, CommandType

def generate_commands(length: int, pen_pairs: int, pen_up_segments: int = 5) -> list[CommandType]:
    commands = []
    for _ in range(pen_pairs):
        commands.append(Command(CommandType.PEN_UP))
        commands.extend(generate_segment(pen_up_segments))
        commands.append(Command(CommandType.PEN_DOWN))
        commands.extend(generate_segment(length // pen_pairs))
    return commands

def generate_segment(length) -> list[CommandType]:
    segment = []
    while length > 0:
        turn = random.choice([CommandType.LEFT_TURN, CommandType.RIGHT_TURN])
        distance = random.randint(5, 25)
        segment.append(Command(CommandType.MOVE_FORWARD, distance))
        segment.append(Command(turn, random.randint(30, 60)))
        length -= distance
    return segment