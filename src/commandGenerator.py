import argparse
import random

from command import Command, CommandType
from input_parser import InputParser

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

def main():
    parser = argparse.ArgumentParser(description="Generate drawing commands.")
    parser.add_argument("--filename", type=str, default="generated.txt", help="Output file to save the commands (default is 'generated.txt').")
    parser.add_argument("length", type=int, help="Total length for the segments.")
    parser.add_argument("pen_pairs", type=int, help="Number of pen up/down pairs.")
    parser.add_argument("--pen_up_segments", type=int, default=5, help="Number of pen up segments per pair (default is 5).")

    args = parser.parse_args()

    commands = generate_commands(args.length, args.pen_pairs, args.pen_up_segments)
    InputParser.write_commands_to_file(commands, args.filename)
        
main()