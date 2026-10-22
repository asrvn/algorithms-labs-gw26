class AVLNode:

    def __init__(self, key, value = None):

        self.key = key
        self.value = value
        self.left, self.right = None, None  # A new leaf has no children
        self.height, self.size = 1, 1  # A leaf has height 1 and subtree size 1

class AVLOrderStatisticTree:

    def __init__(self):

        self.root = None

    def height(self, node):

        return 0 if not node else node.height

    def update_properties(self, node):

        # Maintain the cached height and subtree size after changes are made
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        node.size = 1

        if node.left:

            node.size += node.left.size

        if node.right:

            node.size += node.right.size

    def left_rotation(self, node):

        root = node.right
        node.right = root.left
        root.left = node

        self.update_properties(node)
        self.update_properties(root)

        return root

    def right_rotation(self, node):

        root = node.left
        node.left = root.right
        root.right = node

        self.update_properties(node)
        self.update_properties(root)

        return root

    def rebalance(self, route):

        # Update the balances from the changed subtree back to the root
        for i in reversed(range(len(route))):

            node = route[i]
            self.update_properties(node)
            balance = self.height(node.left) - self.height(node.right)

            if balance > 1:

                # Left-Right imbalance requiring rotating the left child first
                if self.height(node.left.left) < self.height(node.left.right):

                    node.left = self.left_rotation(node.left)

                root = self.right_rotation(node)

            elif balance < -1:

                # Right-Left imbalance requiring rotating the right child first
                if self.height(node.right.right) < self.height(node.right.left):

                    node.right = self.right_rotation(node.right)

                root = self.left_rotation(node)

            else:

                root = node

            # Grafting the subtree to its parent if rotated
            if i == 0:

                self.root = root

            elif route[i - 1].left == node:

                route[i - 1].left = root

            else:

                route[i - 1].right = root

    def insert(self, key, value = None):

        if not self.root:

            self.root = AVLNode(key, value)
            return

        route = []
        node = self.root

        while node:

            if key == node.key:

                node.value = value
                return

            route.append(node)

            if key < node.key:

                if not node.left:

                    node.left = AVLNode(key, value)
                    break

                node = node.left

            elif key > node.key:

                if not node.right:

                    node.right = AVLNode(key, value)
                    break

                node = node.right

        self.rebalance(route)

    def delete(self, key):

        route = []
        parent, node = None, self.root

        while node and node.key != key:

            route.append(node)
            parent = node
            node = node.left if key < node.key else node.right

        if not node:

            return False

        if node.left and node.right:

            route.append(node)
            parent = node
            replacement = node.right

            while replacement.left:

                route.append(replacement)
                parent = replacement
                replacement = replacement.left

            node.key, node.value = replacement.key, replacement.value

            if parent.left == replacement:

                parent.left = replacement.right

            else:

                parent.right = replacement.right

        else:

            child = node.left if node.left else node.right

            if not parent:

                self.root = child
                return True

            if parent.left == node:

                parent.left = child

            else:

                parent.right = child

        self.rebalance(route)
        return True

    def find(self, key):

        node = self.root

        while node:

            if key == node.key:

                return node.value

            node = node.left if key < node.key else node.right

        return None

    def select(self, k):

        if not 1 <= k <= self.size():

            raise IndexError("The desired k is not within the range of the AVL tree")

        node = self.root

        while node:

            lsize = 0 if not node.left else node.left.size
            position = lsize + 1

            if k == position:

                return node.key

            elif k < position:

                node = node.left

            else:

                k -= position
                node = node.right

        return None

    def rank(self, key):

        total_elements, node = 0, self.root

        while node:

            if key < node.key:

                node = node.left

            else:

                lsize = 0 if not node.left else node.left.size
                total_elements += lsize + 1
                node = node.right

        return total_elements

    def size(self):

        return 0 if not self.root else self.root.size

    def is_valid_avl(self):

        node_stack = [[self.root, None, None]]

        while node_stack:

            node, low, high = node_stack.pop()

            if not node:

                continue

            if ((low is not None and node.key <= low) or
                (high is not None and node.key >= high)):

                return False

            lheight, rheight = self.height(node.left), self.height(node.right)
            lsize = 0 if not node.left else node.left.size
            rsize = 0 if not node.right else node.right.size

            if ((abs(lheight - rheight) > 1) or
                (node.height != 1 + max(lheight, rheight)) or
                (node.size != 1 + lsize + rsize)):

                return False

            node_stack.append([node.left, low, node.key])
            node_stack.append([node.right, node.key, high])

        return True

if __name__ == "__main__":

    # Single and double rotation triggers
    rotation_examples = [[3, 2, 1],  # LL
                         [1, 2, 3],  # RR
                         [3, 1, 2],  # LR
                         [1, 3, 2]]  # RL
    for example in rotation_examples:

        avl_tree = AVLOrderStatisticTree()
        for key in example:
            avl_tree.insert(key)

        assert avl_tree.is_valid_avl()
        assert avl_tree.root.key == 2

    basic_example = [2, 4, 1, 3, 5]
    avl_tree = AVLOrderStatisticTree()
    for key in basic_example:
        avl_tree.insert(key)

    assert avl_tree.select(1) == 1
    assert avl_tree.select(avl_tree.size()) == 5

    assert avl_tree.rank(0) == 0  # Below the minimum key
    assert avl_tree.rank(3) == 3  # Existing key
    assert avl_tree.rank(6) == 5  # Above the maximum key

    try:
        avl_tree.select(0)
    except IndexError:
        pass
    else:
        assert False

    try:
        avl_tree.select(6)
    except IndexError:
        pass
    else:
        assert False

    # Example of a deletion causing a cascading rebalance from my written Problem 1
    cascading_rebalance_example = [24, 12, 36, 6, 18, 30, 42, 4, 9, 15, 27, 2]
    avl_tree = AVLOrderStatisticTree()
    for key in cascading_rebalance_example:
        avl_tree.insert(key)

    assert avl_tree.delete(42)
    assert avl_tree.root.key == 12
    assert avl_tree.root.right.right.key == 30
    assert avl_tree.is_valid_avl()
