import logging
from command import *

class InputParser:
    
    @staticmethod
    def parse_file(filename) -> list[Command]:
        commands = []
        try:
            with open(filename, 'r') as file:
                for line_num, line in enumerate(file, start=1):
                    parts = line.strip().split()
                    if len(parts) == 2:
                        command_type, value = parts
                        if command_type in [CommandType.MOVE_FORWARD.value, CommandType.MOVE_BACKWARDS.value, CommandType.LEFT_TURN.value, CommandType.RIGHT_TURN.value]:
                            value = int(value)
                        commands.append(Command(command_type, value))
                    elif len(parts) == 1:
                        command_type = parts[0]
                        if command_type in [CommandType.PEN_DOWN.value, CommandType.PEN_UP.value]:
                            commands.append(Command(command_type))
                        else:
                            logging.warning(f"Value missing at line {line_num}: {line}")
                    else:
                        logging.warning(f"Invalid command at line {line_num}: {line}")
        except FileNotFoundError:
            logging.error(f"File '{filename}' not found.")
        except ValueError as e:
            logging.error(f"Error parsing value at line {line_num}: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        return commands