from __future__ import annotations

class Segment:
    def __init__(self, start : Node, end : Node):
        self.start = start
        self.end = end
    
    def __repr__(self) -> str:
        return f"E: {self.start} -> {self.end}"
        
class Node:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"({self.x},{self.y})"
        