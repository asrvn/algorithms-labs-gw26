class SplayNode:

    def __init__(self, key, value = None):

        self.key = key
        self.value = value
        self.left, self.right, self.parent = None, None, None

class SplayTree:

    def __init__(self):

        self.root = None

    def left_rotation(self, node):

        root = node.right
        node.right = root.left

        if root.left:

            root.left.parent = node

        root.parent = node.parent

        if not node.parent:

            self.root = root

        elif node == node.parent.left:

            node.parent.left = root

        elif node == node.parent.right:

            node.parent.right = root

        root.left = node
        node.parent = root

    def right_rotation(self, node):

        root = node.left
        node.left = root.right

        if root.right:

            root.right.parent = node

        root.parent = node.parent

        if not node.parent:

            self.root = root

        elif node == node.parent.left:

            node.parent.left = root

        elif node == node.parent.right:

            node.parent.right = root

        root.right = node
        node.parent = root

    def splay(self, node):

        while node.parent:

            parent = node.parent
            grandparent = parent.parent

            if not grandparent:  # Case: Zig, L and R

                if node == parent.left:

                    self.right_rotation(parent)

                elif node == parent.right:

                    self.left_rotation(parent)

            elif node == parent.left and parent == grandparent.left:  # Case: Zig-Zig (LL)

                self.right_rotation(grandparent)
                self.right_rotation(parent)

            elif node == parent.right and parent == grandparent.right:  # Case: Zig-Zig (RR)

                self.left_rotation(grandparent)
                self.left_rotation(parent)

            elif node == parent.right and parent == grandparent.left:  # Case: Zig-Zig (LR)

                self.left_rotation(parent)
                self.right_rotation(grandparent)

            elif node == parent.left and parent == grandparent.right:  # Case: Zig-Zig (RL)

                self.right_rotation(parent)
                self.left_rotation(grandparent)

    def insert(self, key, value = None):

        parent, node = None, self.root

        while node:

            if key == node.key:

                node.value = value
                self.splay(node)
                return

            parent = node
            node = node.left if key < node.key else node.right

        node = SplayNode(key, value)
        node.parent = parent

        if not parent:

            self.root = node

        elif key < parent.key:

            parent.left = node

        else:

            parent.right = node

        self.splay(node)

    def search(self, key):

        node, current = self.root, None

        while node:

            current = node

            if key == node.key:

                self.splay(node)
                return node.value

            node = node.left if key < node.key else node.right

        if current:

            self.splay(current)

        return None

    def delete(self, key):

        self.search(key)

        if not self.root or self.root.key != key:

            return False

        left, right = self.root.left, self.root.right
        self.root.left, self.root.right = None, None

        if left:

            left.parent = None

        if right:

            right.parent = None

        self.root = left if left else right

        if left and right:

            node = left

            while node.right:

                node = node.right

            self.splay(node)
            self.root.right = right
            right.parent = self.root

        return True

    def to_inorder_keys(self):

        node_stack, ordered_keys = [], []
        node = self.root

        while node_stack or node:

            if node:

                node_stack.append(node)
                node = node.left

            else:

                node = node_stack.pop()
                ordered_keys.append(node.key)
                node = node.right

        return ordered_keys

    def root_key(self):

        return None if not self.root else self.root.key

    def size(self):

        return len(self.to_inorder_keys())

if __name__ == "__main__":

    zig_example = [[10, "A"], [20, "B"]]
    splay_tree = SplayTree()
    for key, value in zig_example:
        splay_tree.insert(key, value)

    assert splay_tree.search(10) == "A"
    assert splay_tree.root_key() == 10

    zig_zig_example = [[30, "C"], [20, "B"], [10, "A"]]
    splay_tree = SplayTree()
    for key, value in zig_zig_example:
        splay_tree.insert(key, value)

    assert splay_tree.search(30) == "C"
    assert splay_tree.root_key() == 30

    zig_zag_example = [[30, "C"], [10, "A"], [20, "B"]]
    splay_tree = SplayTree()
    for key, value in zig_zag_example:
        splay_tree.insert(key, value)

    assert splay_tree.root_key() == 20
    assert splay_tree.search(99) is None
    assert splay_tree.root_key() == 30
    splay_tree.insert(10, "D")
    assert splay_tree.search(10) == "D"
    assert splay_tree.size() == 3

    split_join_delete_example = [[6, "F"], [3, "C"], [8, "H"], [1, "A"], [5, "E"], [7, "G"], [9, "I"]]
    splay_tree = SplayTree()
    for key, value in split_join_delete_example:
        splay_tree.insert(key, value)

    assert splay_tree.search(6) == "F"
    assert splay_tree.root.left is not None and splay_tree.root.right is not None
    assert splay_tree.delete(6)
    assert splay_tree.to_inorder_keys() == [1, 3, 5, 7, 8, 9]
    assert not splay_tree.delete(0)
    for key, value in split_join_delete_example[1:]:
        assert splay_tree.delete(key)
    assert splay_tree.size() == 0
    assert splay_tree.root_key() is None
