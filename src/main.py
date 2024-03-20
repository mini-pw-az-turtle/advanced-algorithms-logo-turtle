import sys
import matplotlib.pyplot as plt
from input_parser import InputParser
from commands_processor import CommandsProcessor
from intersection_checker import AnyIntersections

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        return
    
    print(f"Processing file {sys.argv[1]}.")
    commands = InputParser.parse_file(sys.argv[1])
    
    commandProcessor = CommandsProcessor()
    segments = commandProcessor.processCommands(commands)
    print(segments)
    print(len(segments))
    AnyIntersections.check_all(segments)
    draw_edges(segments)
    
def draw_edges(segments):
    for idx, segment in enumerate(segments):
        x_values = [segment.start.x, segment.end.x]
        y_values = [segment.start.y, segment.end.y]
        plt.plot(x_values, y_values, 'b-')  # Blue line connecting start and end points
        plt.text((segment.start.x + segment.end.x) / 2, (segment.start.y + segment.end.y) / 2, str(idx), fontsize=10, color='red')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graphical representation of turtle path')
    plt.grid(True)
    plt.show()


    
main()