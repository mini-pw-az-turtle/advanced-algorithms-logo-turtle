from __future__ import annotations

class Segment:
    start: Node
    end: Node

    def __init__(self, start : Node, end : Node):
        self.start = start
        self.end = end
    
    def __repr__(self) -> str:
        return f"E: {self.start} -> {self.end}"
        
class Node:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __lt__(self, other: 'Node') -> bool:
        return self.x < other.x
        