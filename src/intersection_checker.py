from enum import Enum
from timeit import timeit
from typing import Tuple
from newAvlTree import AVL_Tree, TreeNode, findPreSuc
from segment import Node, Segment

def is_left(point: Node, segment: Segment) -> float:
    """
    Determines whether a point is to the left, on, or to the right of a line segment.

    Args:
        point (Node): The point to be checked.
        segment (Segment): The line segment.

    Returns:
        float: The determinant value indicating the point's position relative to the segment.
               Positive if the point is to the left.
               Negative if the point is to the right.
               Zero     if the point is on the segment.
    """
    return (segment.start.x - point.x) * (segment.end.y - point.y) - (segment.start.y - point.y) * (segment.end.x - point.x)

def on_segment(point: Node, segment: Segment) -> bool:
    """
    Checks if a point lies on a given line segment.

    Args:
        point (Node): The point to be checked.
        segment (Segment): The line segment.

    Returns:
        bool: True if the point lies on the segment, False otherwise or if point is exactly on either of end points of segment.
    """
    return min(segment.start.x, segment.end.x) < point.x < max(segment.start.x, segment.end.x) and min(segment.start.y, segment.end.y) < point.y < max(segment.start.y, segment.end.y)

def intersect(segment1: Segment, segment2: Segment) -> bool:
    """
    Checks whether two line segments intersect.

    Args:
        segment1 (Segment): The first line segment.
        segment2 (Segment): The second line segment.

    Returns:
        bool: True if the line segments intersect, False otherwise.
    """
    p1, p2 = segment1.start, segment1.end
    p3, p4 = segment2.start, segment2.end

    d1 = is_left(p1, segment2)
    d2 = is_left(p2, segment2)
    d3 = is_left(p3, segment1)
    d4 = is_left(p4, segment1)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    elif d1 == 0 and on_segment(p1, segment2):
        return True
    elif d2 == 0 and on_segment(p2, segment2):
        return True
    elif d3 == 0 and on_segment(p3, segment1):
        return True
    elif d4 == 0 and on_segment(p4, segment1):
        return True
    else:
        return False


def any_intersections(segments: list[Segment]) -> bool:
    class Endpoint:
        node: Node
        label: int # Segment index
        isLeft: bool # Is endpoint left in segment (has lesser x)

        def __init__(self, node: Node, label: int, isLeft: bool):
            self.node = node
            self.label = label
            self.isLeft = isLeft

        def __lt__(self, other: 'Endpoint') -> bool:
            if self.node.x == other.node.x:
                if self.isLeft == other.isLeft:
                    return self.node.y < other.node.y
                else:
                    return self.isLeft
            else:
                return self.node.x < other.node.x

        def __gt__(self, other: 'Endpoint') -> bool:
            if self.node.x == other.node.x:
                if self.isLeft == other.isLeft:
                    return self.node.y > other.node.y
                else:
                    return other.isLeft
            else:
                return self.node.x > other.node.x



        def __ne__(self, other: 'Endpoint') -> bool:
            return not self.__eq__(other)
    class Edge:
        label: int  # Segment index

        def __init__(self, label: int):
            self.label = label

        def _getNodesSorted(self) -> Tuple[Node, Node]:
            segment = segments[self.label]
            if segment.start.x == segment.end.x:
                isStartLeft = segment.start.y < segment.end.y
            else:
                isStartLeft = segment.start.x < segment.end.x

            if isStartLeft:
                return segment.start, segment.end
            else:
                return segment.end, segment.start

        def _getLeft(self) -> Node:
            return self._getNodesSorted()[0]

        def _getRight(self) -> Node:
            return self._getNodesSorted()[1]

        def compare_y(self, other: 'Edge') -> bool:
            # Calculate cross product to determine which edge is above the other
            self_left, _ = self._getNodesSorted()
            other_left, _ = other._getNodesSorted()

            if self_left.y==other_left.y:
                return self_left.x < other_left.x
            else:
                return self_left.y < other_left.y

        def __lt__(self, other: 'Edge') -> bool:
            return self.compare_y(other)

        def __gt__(self, other: 'Edge') -> bool:
            return not self.compare_y(other)

        def __eq__(self, other: 'Edge') -> bool:
            if isinstance(other, Edge):
                return self.label == other.label
            else:
                return False

        def __ne__(self, other: 'Edge') -> bool:
            return not self.__eq__(other)

    endpoints = list[Endpoint]()

    activeEdges: AVL_Tree[Edge]  = AVL_Tree[Edge]()
    activeEdgesRoot: TreeNode[Edge] = None
    for i, segment in enumerate(segments):
        if segment.start.x == segment.end.x:
            isStartLeft = segment.start.y <= segment.end.y
        else:
            isStartLeft = segment.start.x < segment.end.x
        endpoints.append(Endpoint(segment.start, i, isStartLeft))
        endpoints.append(Endpoint(segment.end, i, not isStartLeft))
    endpoints.sort()
    

    for endpoint in endpoints:
        segmentIndex = endpoint.label
        isLeft = endpoint.isLeft
        segment = segments[segmentIndex]

        for edge in activeEdges.inOrder(activeEdgesRoot):
            print(f"edge {edge.label}", end=" ")
        print("\n")

        pre = suc = None

        if isLeft:
            # Edge is starting
            newEdge = Edge(endpoint.label)
            
            activeEdgesRoot = activeEdges.insert(activeEdgesRoot, newEdge)

            findPreSuc.pre = None
            findPreSuc.suc = None
            
            findPreSuc(activeEdgesRoot, newEdge)

            pre: TreeNode[Edge] = findPreSuc.pre
            suc: TreeNode[Edge] = findPreSuc.suc

            if pre is not None and intersect(segments[segmentIndex], segments[pre.val.label]):
                print(f"Intersection in {segmentIndex} and {pre.val.label}")
                return True
            if suc is not None and intersect(segments[segmentIndex], segments[suc.val.label]):
                print(f"Intersection in {segmentIndex} and {suc.val.label}")
                return True
        else:

            endingEdge = Edge(endpoint.label)

            findPreSuc.pre = None
            findPreSuc.suc = None
            
            findPreSuc(activeEdgesRoot, newEdge)

            pre: TreeNode[Edge] = findPreSuc.pre
            suc: TreeNode[Edge] = findPreSuc.suc

            if suc is not None and pre is not None and intersect(segments[suc.val.label], segments[pre.val.label]):
                print(f"Intersection in {suc.val.label} and {pre.val.label}")
                return True

            print(f"Pre delete of {endingEdge.label}")
            for edge in activeEdges.inOrder(activeEdgesRoot):
                print(f"edge {edge.label}", end=" ")
            print("\n")
            activeEdgesRoot = activeEdges.delete(activeEdgesRoot, endingEdge)
            print(f"Post delete of {endingEdge.label}")
            for edge in activeEdges.inOrder(activeEdgesRoot):
                print(f"edge {edge.label}", end=" ")
            print("\n")

    return False


class AnyIntersections:
    @staticmethod
    def check(segments: list[Segment]) -> bool:
        value = any_intersections(segments)
        execution_time = timeit(lambda: any_intersections(segments), number=1) * 1000
        print(f"\033[KResult: {value}\ttime: {execution_time:.4f}ms")
        return value
