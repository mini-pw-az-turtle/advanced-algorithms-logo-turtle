import argparse
import random

from command import Command, CommandType
from input_parser import InputParser
from intersection_checker import AnyIntersections
from commands_processor import CommandsProcessor

def generate(length: int, pen_pairs: int, pen_up_segments: int = 5, force_intersections : bool = False) -> list[CommandType]:
    commandProcessor = CommandsProcessor()
    commands = generate_commands(length, pen_pairs, pen_up_segments)
    segments = commandProcessor.processCommands(commands)
    if(force_intersections):
        while not AnyIntersections.check(segments):
            commands = generate_commands(length+1 // 2, pen_pairs, pen_up_segments)
            segments = commandProcessor.processCommands(commands)
        tmp = commands.copy()
        random.shuffle(tmp)
        commands.extend(tmp)
    return commands

def generate_commands(length: int, pen_pairs: int, pen_up_segments: int = 5) -> list[CommandType]:
    commands = []
    for _ in range(pen_pairs):
        commands.append(Command(CommandType.PEN_UP))
        commands.extend(generate_segments(pen_up_segments))
        commands.append(Command(CommandType.PEN_DOWN))
        commands.extend(generate_segments((length - pen_up_segments) // pen_pairs))
    return commands[:length]

def generate_segments(length) -> list[CommandType]:
    segments = []
    for _ in range(length // 2):
        turn = random.choice([CommandType.LEFT_TURN, CommandType.RIGHT_TURN])
        distance = random.randint(5, 25)
        segments.append(Command(CommandType.MOVE_FORWARD, distance))
        segments.append(Command(turn, random.randint(30, 60)))
    return segments

def check_length(value):
    ivalue = int(value)
    if ivalue < 50 or ivalue > 1000:
        raise argparse.ArgumentTypeError("%s is not a valid length (must be between 30 and 1000)" % value)
    return ivalue

def main():
    parser = argparse.ArgumentParser(description="Generate drawing commands.")
    parser.add_argument("--filename", type=str, default="generated.txt", help="Output file to save the commands (default is 'generated.txt').")
    parser.add_argument("length", type=check_length, help="Total number of commands generated (between 50 and 1000).")
    parser.add_argument("pen_pairs", type=int, help="Number of pen up/down pairs.")
    parser.add_argument("--pen_up_segments", type=int, default=5, help="Number of pen up segments per pair (default is 5).")
    parser.add_argument("--force_intersections", action="store_true", help="Generate intersections in the path (default is False).")
    args = parser.parse_args()

    commands = generate(args.length, args.pen_pairs, args.pen_up_segments, args.force_intersections)
    InputParser.write_commands_to_file(commands, args.filename)
    
if __name__ == "__main__":  
    main()