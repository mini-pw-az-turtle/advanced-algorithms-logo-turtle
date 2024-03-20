from enum import Enum
from timeit import timeit
from avlTree import AVLTree
from segment import Node, Segment

def is_left(point: Node, segment: Segment) -> float:
    return (segment.end.x - segment.start.x) * (point.y - segment.start.y) - (point.x - segment.start.x) * (segment.end.y - segment.start.y)

def intersect(segment1: Segment, segment2: Segment) -> bool:
    p1, p2 = segment1.start, segment1.end
    p3, p4 = segment2.start, segment2.end

    d1 = is_left(p3, segment1)
    d2 = is_left(p4, segment1)
    d3 = is_left(p1, segment2)
    d4 = is_left(p2, segment2)

    if (d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0) and (d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0):
        return True
    elif d1 == 0 and on_segment(p3, segment1):
        return True
    elif d2 == 0 and on_segment(p4, segment1):
        return True
    elif d3 == 0 and on_segment(p1, segment2):
        return True
    elif d4 == 0 and on_segment(p2, segment2):
        return True
    else:
        return False

def on_segment(point: Node, segment: Segment) -> bool:
    if min(segment.start.x, segment.end.x) <= point.x <= max(segment.start.x, segment.end.x) and min(segment.start.y, segment.end.y) <= point.y <= max(segment.start.y, segment.end.y):
        return True
    else:
        return False
    
def heapify(arr: list, n: int, i: int) -> None:
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[l] > arr[largest]:
            largest = l

        if r < n and arr[r] > arr[largest]:
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

def heapSort(arr: list) -> list:
        n = len(arr)
        for i in range(n, -1, -1):
            heapify(arr, n, i)
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            heapify(arr, i, 0)
        return arr

def any_intersections_avl(segments: list[Segment]) -> bool:
    events = AVLTree()  # Using AVL tree instead of list
    for i, segment in enumerate(segments):
        events.insert((segment.start.x, i, True))
        events.insert((segment.end.x, i, False))

    active_segments = set()
    for event in events.inorder_traversal():
        label_index = event[1]
        is_left_endpoint = event[2]
        segment = segments[label_index]

        if is_left_endpoint:
            active_segments.add(label_index)
            predecessor = None
            successor = None
            for active_segment in active_segments:
                if active_segment < label_index:
                    predecessor = active_segment
                elif active_segment > label_index and successor is None:
                    successor = active_segment
                    break
            if predecessor is not None and intersect(segments[predecessor], segment):
                return True
            if successor is not None and intersect(segments[label_index], segments[successor]):
                return True
        else:
            if label_index in active_segments:  # Dodaj sprawdzenie przed usunięciem
                active_segments.remove(label_index)
            predecessor = None
            successor = None
            for active_segment in active_segments:
                if active_segment < label_index:
                    predecessor = active_segment
                elif active_segment > label_index and successor is None:
                    successor = active_segment
                    break
            if predecessor is not None and successor is not None and intersect(segments[predecessor], segments[successor]):
                return True

    return False

def any_intersections_heap(segments: list[Segment]) -> bool:
    events = [] # TODO: Needs to be changed to balanced binary tree (AVL/black-red) to assure O(log(n)) complexity for adding and removing elements.
    for i, segment in enumerate(segments):
        events.append((segment.start.x, i, True))
        events.append((segment.end.x, i, False))

    heapSort(events)

    active_segments = set()
    for event in events:
        label_index = event[1]
        is_left_endpoint = event[2]
        segment = segments[label_index]

        if is_left_endpoint:
            active_segments.add(label_index)
            predecessor = None
            successor = None
            for active_segment in active_segments:
                if active_segment < label_index:
                    predecessor = active_segment
                elif active_segment > label_index and successor is None:
                    successor = active_segment
                    break
            if predecessor is not None and intersect(segments[predecessor], segment):
                return True
            if successor is not None and intersect(segments[label_index], segments[successor]):
                return True
        else:
            if label_index in active_segments:  # Dodaj sprawdzenie przed usunięciem
                active_segments.remove(label_index)
            predecessor = None
            successor = None
            for active_segment in active_segments:
                if active_segment < label_index:
                    predecessor = active_segment
                elif active_segment > label_index and successor is None:
                    successor = active_segment
                    break
            if predecessor is not None and successor is not None and intersect(segments[predecessor], segments[successor]):
                return True

    return False

class AlgorithmBase(Enum):
    AVL = 0
    HEAP = 1

class AnyIntersections:
    @staticmethod
    def check_all(segments: list[Segment]) -> None:
        for base in AlgorithmBase:
            print(f"For type {base.name} is in progress", end="\r")
            value = AnyIntersections.do_for_base(segments, base)
            execution_time = timeit(lambda: AnyIntersections.do_for_base(segments, base), number=1) * 1000
            print(f"\033[KFor type {base.name}:\tresoult: {value}\ttime: {execution_time:.4f}ms")

    
    @staticmethod
    def do_for_base(segments: list[Segment], base: AlgorithmBase) -> bool:
        if base == AlgorithmBase.AVL:
            return any_intersections_avl(segments)
        if base == AlgorithmBase.HEAP:
            return any_intersections_heap(segments)