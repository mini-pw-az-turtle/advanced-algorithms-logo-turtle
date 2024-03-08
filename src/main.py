import sys
from input_parser import InputParser
from commands_processor import CommandsProcessor

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        return
    
    print(f"Processing file {sys.argv[1]}.")
    commands = InputParser.parse_file(sys.argv[1])
    
    commandProcessor = CommandsProcessor()
    edges = commandProcessor.processCommands(commands)
    print(edges)
    print(len(edges))
    
main()