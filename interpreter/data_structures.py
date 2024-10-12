from typing import Any
from tools import adapt_expression, adapt_output, divide_by_commas
from limits import Limits

class Array:

    def __init__(self, default: Any = []) -> None:
        if hasattr(default, "body"):
            self.body: list[Any] = list(default.body)
        elif isinstance(default, list):
            self.body: list[Any] = default
        else:
            self.body: list[Any] = [default]

    def size(self) -> int:
        return len(self.body)

    def length(self) -> int:
        return len(self.body)

    def __str__(self) -> str:
        string: str = '[' + ", ".join([(('"' + value + '"') if isinstance(value, str) else str(value)) for value in self.body]) + ']'
        return adapt_output(string)

class LazyArray(Array):

    def __getitem__(self, index: int) -> Any:
        if index >= len(self.body):
            return None
        return self.body[index]

    def __setitem__(self, index: int, value: Any) -> None:
        while index >= len(self.body):
            self.body.append(None)
        self.body[index] = value

class LazyArrayInternal(LazyArray):

    def __init__(self, body: str = "") -> None:
        self.body: list[Any] = []
        if body != "":
            for value in divide_by_commas(body):
                self.body.append(eval(adapt_expression(value.strip())))

class StaticArray(Array):

    def __init__(self, size: int = 0, default: Any = []) -> None:
        self.body = [None for _ in range(0, size)]
        values: list[Any] = []
        if hasattr(default, "body"):
            values = list(default.body)
        elif isinstance(default, list):
            values = default
        else:
            values = [default]
        if len(values) > size:
            raise Exception("More defaults that the size")
        for i in range(0, len(values)):
            self.body[i] = values[i]

    def resize(self, size: int) -> None:
        self.body = [None for _ in range(0, size)]

    def __getitem__(self, index: int) -> Any:
        if index < 0 or index >= len(self.body):
            raise Exception("Index out of range")
        return self.body[index]

    def __setitem__(self, index: int, value: Any) -> None:
        if index < 0 or index >= len(self.body):
            raise Exception("Index out of range")
        self.body[index] = value

class DynamicArray(Array):

    def __getitem__(self, index: int) -> Any:
        if index < 0 or index >= len(self.body):
            raise Exception("Index out of range")
        return self.body[index]

    def __setitem__(self, index: int, value: Any) -> None:
        if index < 0 or index >= len(self.body):
            raise Exception("Index out of range")
        self.body[index] = value

    def push(self, value: Any) -> None:
        self.body.append(value)

    def insert(self, index: int, value: Any) -> None:
        self.body.insert(index, value)

    def pop(self) -> Any:
        return self.body.pop()

    def remove(self, index: Any) -> Any:
        return self.body.pop(index)

class Dictionary:

    def __init__(self) -> None:
        self.body: dict[Any, Any] = {}

    def __getitem__(self, key: Any) -> Any:
        if key not in self.body:
            return None
        else:
            return self.body[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self.body[key] = value

    def __str__(self) -> str:
        string: str = '{' + ", ".join([(('"'+ key + '"') if isinstance(key, str) else str(key)) + ': ' + (('"' + self.body[key] + '"') if isinstance(self.body[key], str) else str(self.body[key])) for key in self.body]) + '}'
        return adapt_output(string)

class DictionaryInternal(Dictionary):

    def __init__(self, body: str = "") -> None:
        self.body: dict[Any, Any] = {}
        if body != "":
            for elem in divide_by_commas(body):
                key_value = elem.strip().split(':')
                if len(key_value) != 2:
                    raise Exception("Invalid dictionary syntax")
                self.body[eval(adapt_expression(key_value[0].strip()))] = eval(adapt_expression(key_value[1].strip()))

class Stack:

    def __init__(self, default: Any = []) -> None:
        if hasattr(default, "body"):
            self.body: list[Any] = list(default.body)
        elif isinstance(default, list):
            self.body: list[Any] = default
        else:
            self.body: list[Any] = [default]
    
    def push(self, element: Any) -> None:
        self.body.append(element)

    def pop(self) -> Any:
        return self.body.pop()

    def is_empty(self) -> bool:
        return not len(self.body)

    def size(self) -> int:
        return len(self.body)

    def length(self) -> int:
        return len(self.body)

    def __str__(self) -> str:
        string: str = '[' + ", ".join([(('"' + value + '"') if isinstance(value, str) else str(value)) for value in self.body]) + ']'
        return adapt_output(string)
    
class Queue:

    def __init__(self, default: Any = []) -> None:
        if hasattr(default, "body"):
            self.body: list[Any] = list(default.body)
        elif isinstance(default, list):
            self.body: list[Any] = default
        else:
            self.body: list[Any] = [default]
        self.end_index: int = 0
    
    def enqueue(self, element: Any) -> None:
        self.body.append(element)

    def dequeue(self) -> Any:
        self.end_index += 1
        return self.body[self.end_index - 1]

    def is_empty(self) -> bool:
        return (len(self.body) - self.end_index) <= 0

    def size(self) -> int:
        return len(self.body) - self.end_index

    def length(self) -> int:
        return len(self.body) - self.end_index

    def __str__(self) -> str:
        string: str = '[' + ", ".join([(('"' + value + '"') if isinstance(value, str) else str(value)) for value in self.body[self.end_index:]]) + ']'
        return adapt_output(string)

class BinaryTreeNode:

    def __init__(self, value: Any = None, height: int = 1, left: Any = None, right: Any = None) -> None:
        self.value: Any = value
        self.height: int = height
        self.left: BinaryTreeNode | None = left
        self.right: BinaryTreeNode | None = right

class BinaryTree:

    def __init__(self, default: Any = []) -> None:
        self.__head: BinaryTreeNode | None = None
        values: list[Any] = []
        if hasattr(default, "body"):
            values = list(default.body)
        elif isinstance(default, list):
            values = default
        else:
            values = [default]
        for value in values:
            self.add(value)

    def is_empty(self) -> bool:
        return self.__head is None

    def __fix_height(self, node: BinaryTreeNode) -> None:
        height_left: int = node.left.height if node.left != None else 0
        height_right: int = node.right.height if node.right != None else 0 
        node.height: int = (height_left if height_left > height_right else height_right) + 1

    def __rotate_right(self, node: BinaryTreeNode) -> BinaryTreeNode:
        vertex: BinaryTreeNode = node.left
        node.left = vertex.right
        vertex.right = node
        self.__fix_height(node)
        self.__fix_height(vertex)
        return vertex

    def __rotate_left(self, node: BinaryTreeNode) -> BinaryTreeNode:
        vertex: BinaryTreeNode = node.right
        node.right = vertex.left
        vertex.left = node
        self.__fix_height(node)
        self.__fix_height(vertex)
        return vertex

    def __b_factor(self, node: BinaryTreeNode) -> int:
        return (node.right.height if node.right != None else 0) - (node.left.height if node.left != None else 0)

    def __balance(self, node: BinaryTreeNode) -> BinaryTreeNode:
        self.__fix_height(node)
        if self.__b_factor(node) == 2:
            if self.__b_factor(node.right) < 0:
                node.right = self.__rotate_right(node.right)
            return self.__rotate_left(node)
        elif self.__b_factor(node) == -2:
            if self.__b_factor(node.left) > 0:
                node.left = self.__rotate_left(node.left)
            return self.__rotate_right(node)
        return node

    def __get_min_node(self, node: BinaryTreeNode) -> BinaryTreeNode:
        if node.left != None:
            return self.__get_min_node(node.left)
        else:
            return node

    def get_min(self) -> int:
        if self.__head.left != None:
            return self.__get_min_node(self.__head.left)
        elif self.__head is not None:
            return self.__head.value
        else:
            return None

    def __get_max_node(self, node: BinaryTreeNode) -> BinaryTreeNode:
        if node.right != None:
            return self.__get_max_node(node.right)
        else:
            return node

    def get_max(self) -> int:
        if self.__head.right != None:
            return self.__get_max_node(self.__head.right)
        elif self.__head is not None:
            return self.__head.value
        else:
            return None

    def __add_node(self, value: Any, node: BinaryTreeNode | None) -> None:
        if node is None:
            return BinaryTreeNode(value)
        if value < node.value:
            node.left = self.__add_node(value, node.left)
        else:
            node.right = self.__add_node(value, node.right)
        return self.__balance(node)

    def add(self, value: Any) -> None:
        self.__head = self.__add_node(value, self.__head)

    def __includes(self, value: Any, node: BinaryTreeNode) -> BinaryTreeNode:
        if node.value == value:
            return True
        if value < node.value:
            if node.left is None:
                return False
            return self.__includes(value, node.left)
        else:
            if node.right is None:
                return False
            return self.__includes(value, node.right)

    def includes(self, value: Any) -> bool:
        return not self.is_empty() and self.__includes(value, self.__head)

    def __remove_min_node(self, node: BinaryTreeNode | None) -> BinaryTreeNode:
        if node is None:
            return None
        if node.left is None:
            return node.right
        node.left = self.__remove_min_node(node.left)
        return self.__balance(node)

    def remove_min(self) -> None:
        self.__head = self.__remove_min_node(self.__head)

    def __remove_max_node(self, node: BinaryTreeNode | None) -> BinaryTreeNode:
        if node is None:
            return None
        if node.right is None:
            return node.left
        node.right = self.__remove_max_node(node.right)
        return self.__balance(node)

    def remove_max(self) -> None:
        self.__head = self.__remove_max_node(self.__head)

    def __remove_node(self, value: Any, node: BinaryTreeNode | None) -> BinaryTreeNode:
        if node is None:
            return None
        if value < node.value:
            node.left = self.__remove_node(value, node.left)
        elif value > node.value:
            node.right = self.__remove_node(value, node.right)
        else:
            left: BinaryTreeNode | None = node.left
            right: BinaryTreeNode | None = node.right
            if right is None:
                return left
            min: BinaryTreeNode = self.__get_min_node(right)
            min.right = self.__remove_min_node(right)
            min.left = left
            return self.__balance(min)
        return self.__balance(node)

    def remove(self, value: Any) -> None:
        self.__head = self.__remove_node(value, self.__head)

    def __bfs(self) -> list[list[Any, int]]:
        queue: Queue = Queue([[self.__head, 0]])
        path: list[list[Any, int]] = []
        while not queue.is_empty():
            vertex: list[BinaryTreeNode, int] = queue.dequeue()
            path.append([vertex[0].value, vertex[1]])
            if vertex[0].right != None:
                queue.enqueue([vertex[0].right, vertex[1] + 1])
            if vertex[0].left != None:
                queue.enqueue([vertex[0].left, vertex[1] + 1])
        return path

    def get_tree_by_levels(self) -> LazyArray:
        if self.is_empty():
            return []
        path: list[list[Any, int]] = self.__bfs()
        max_p: int = -1
        for node in path:
            if max_p < node[1]:
                max_p = node[1]
        result: list[list[Any]] = [[] for _ in range(0, max_p + 1)]
        for node in path:
            result[node[1]].append(node[0])
        return LazyArray([LazyArray(level) for level in result])

    def get_tree_list(self) -> LazyArray:
        if self.is_empty():
            return []
        path: list[list[Any, int]] = self.__bfs()
        result: list[Any] = []
        for node in path:
            result.append(node[0])
        return LazyArray(result)

    def __dfs_plain(self, node: BinaryTreeNode, path: list[Any]) -> None:
        if node.left != None:
            self.__dfs_plain(node.left, path)
        path.append(node.value)
        if node.right != None:
            self.__dfs_plain(node.right, path)
    
    def __dfs_reverse(self, node: BinaryTreeNode, path: list[Any]) -> None:
        if node.right != None:
            self.__dfs_reverse(node.right, path)
        path.append(node.value)
        if node.left != None:
            self.__dfs_reverse(node.left, path)

    def get_tree_sorted(self, reverse: bool = False) -> LazyArray:
        if self.is_empty():
            return []
        path: list[Any] = []
        if reverse:
            self.__dfs_reverse(self.__head, path)
        else:
            self.__dfs_plain(self.__head, path)
        return LazyArray(path)

    def __str__(self) -> str:
        return self.get_tree_list().__str__()

class Set:

    def __init__(self, default: Any = []) -> None:
        self.tree: BinaryTree = BinaryTree()
        values: list[Any] = []
        if hasattr(default, "body"):
            values = list(default.body)
        elif isinstance(default, list):
            values = default
        else:
            values = [default]
        for value in values:
            if not self.tree.includes(value):
                self.tree.add(value)

    def __getitem__(self, index: int) -> Any:
        values: LazyArray = self.tree.get_tree_sorted()
        if index >= len(values.body):
            return None
        else:
            return values[index]

    def is_empty(self) -> bool:
        return self.tree.is_empty()

    def add(self, value: Any) -> None:
        if not self.tree.includes(value):
            self.tree.add(value)

    def includes(self, value: Any) -> bool:
        return self.tree.includes(value)
    
    def remove(self, value: Any) -> None:
        if self.tree.includes(value):
            self.tree.remove(value)

    def to_array(self) -> LazyArray:
        return self.tree.get_tree_sorted()

    def size(self) -> int:
        return len(self.tree.get_tree_sorted())

    def length(self) -> int:
        return len(self.tree.get_tree_sorted())

    def __str__(self) -> str:
        return self.tree.get_tree_sorted().__str__()

class Multiset(Set):

    def __init__(self, default: Any = []) -> None:
        self.tree: BinaryTree = BinaryTree()
        values: list[Any] = []
        if hasattr(default, "body"):
            values = list(default.body)
        elif isinstance(default, list):
            values = default
        else:
            values = [default]
        for value in values:
            self.tree.add(value)

    def add(self, value: Any) -> None:
        self.tree.add(value)

class CustomStructure:

    def __init__(self, limits: Limits, names: list[str], default_values: list[Any], *args_values: Any) -> None:
        self.limits = limits
        for i in range(0, len(names)):
            setattr(self, names[i], default_values[i])
            self.limits.change_limit_by_value(default_values[i], -1)
        for i in range(0, len(args_values)):
            setattr(self, names[i], args_values[i])

    def __str__(self) -> str:
        string: str = '{' + ", ".join([(('"'+ key + '"') if isinstance(key, str) else str(key)) + ': ' + (('"' + self.__dict__[key] + '"') if isinstance(self.__dict__[key], str) else str(self.__dict__[key])) for key in self.__dict__]) + '}'
        return adapt_output(string)

aliases = {
    "LazyArray": LazyArray,
    "Array": LazyArray,
    "LazyArrayInternal": LazyArrayInternal,
    "StaticArray": StaticArray,
    "DynamicArray": DynamicArray,
    "Dictionary": Dictionary,
    "DictionaryInternal": DictionaryInternal,
    "Map": Dictionary,
    "Stack": Stack,
    "Queue": Queue,
    "BinaryTree": BinaryTree,
    "BinarySearchTree": BinaryTree,
    "Set": Set,
    "Multiset": Multiset,
}