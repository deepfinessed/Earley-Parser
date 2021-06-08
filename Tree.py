from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')

class Node(Generic[T]):

    value: T
    parent: Optional['Node[T]']
    children: List['Node[T]']

    def __init__(self, value: T, parent: 'Optional[Node[T]]'=None, children: 'Optional[List[Node[T]]]'=None):
        self.value = value
        self.parent = parent
        self.children = children if children else []

    def add_child(self, value: T) -> None:
        self.children.append(Node(value, parent=self))

    def append_node(self, node: 'Node[T]') -> None:
        node.parent = self
        self.children.append(node)

    def __str__(self) -> str:
        return str(self.value)


