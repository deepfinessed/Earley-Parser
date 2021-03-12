from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')

class Node(Generic[T]):

    value: T
    parent: Optional['Node[T]']
    children: List['Node[T]']

    def __init__(self, value: T, parent=None, children=None):
        self.value = value
        self.parent = parent
        self.children = children if children else []

    def add_child(self, value: T):
        self.children.append(Node(value, parent=self))

    def append_node(self, node: 'Node'):
        node.parent = self
        self.children.append(node)

    def __str__(self):
        return str(self.value)


