import sys
import matplotlib.pyplot as plt
from input_parser import InputParser
from commands_processor import CommandsProcessor
from intersection_checker import AnyIntersections
from commandGenerator import generate_commands

def main():
    if len(sys.argv) != 2:
        print("Incorrect input. Example input:\n$ python src/main.py data/simple.txt\t - Solve case from file\n$")
        return
    else:
        print(f"Processing file {sys.argv[1]}.")
        commands = InputParser.parse_file(sys.argv[1])
    
        commandProcessor = CommandsProcessor()
        segments = commandProcessor.processCommands(commands)

        ret = AnyIntersections.check(segments)
        print(f"\033[KResult: {ret[0]}\ttime: {ret[1]:.4f}ms")
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