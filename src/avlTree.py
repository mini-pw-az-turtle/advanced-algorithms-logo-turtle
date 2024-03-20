from __future__ import annotations

from typing import Generator
from segment import Node

class AVLNode:
    key: Node
    left: AVLNode
    right: AVLNode
    height: int

    def __init__(self, key: Node):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    root: AVLNode

    def __init__(self):
        self.root = None

    def insert(self, key: Node):
        self.root = self._insert(self.root, key)

    def _insert(self, root: AVLNode, key: Node) -> AVLNode:
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self._insert(root.left, key)
        else:
            root.right = self._insert(root.right, key)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        balance = self._get_balance(root)

        if balance > 1:
            if key < root.left.key:
                return self._right_rotate(root)
            else:
                root.left = self._left_rotate(root.left)
                return self._right_rotate(root)
        if balance < -1:
            if key > root.right.key:
                return self._left_rotate(root)
            else:
                root.right = self._right_rotate(root.right)
                return self._left_rotate(root)

        return root

    def _left_rotate(self, z: AVLNode) -> AVLNode:
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, z: AVLNode) -> AVLNode:
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _get_height(self, node: AVLNode) -> int:
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: AVLNode) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def inorder_traversal(self) -> Generator[Node, None, None]:
        yield from self._inorder_traversal(self.root)

    def _inorder_traversal(self, root: AVLNode) -> Generator[Node, None, None]:
        if root:
            yield from self._inorder_traversal(root.left)
            yield root.key
            yield from self._inorder_traversal(root.right)