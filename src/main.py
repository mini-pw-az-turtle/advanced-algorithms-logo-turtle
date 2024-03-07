import sys
from input_parser import InputParser

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        return
    
    print(sys.argv[1])
    commands = InputParser.parse_file(sys.argv[1])
    print(commands)
    
main()