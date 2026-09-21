"""Part 2: implement BST pointer insertion and deletion.

Node structure, search, minimum, and subtree transplant helpers are provided.
"""


class Node:
  """Binary Search Tree node with parent pointer and height."""

  def __init__(self, key, parent=None):
    self.key = key
    self.parent = parent
    self.left = None
    self.right = None
    self.height = 0

  def __repr__(self):
    return "Node(" + str(self.key) + ")"


class BinarySearchTree:
  """Container holding the root pointer of a Binary Search Tree."""

  def __init__(self):
    self.root = None


def bst_search(node, key):
  """Provided: search for node containing key; return Node or None."""
  while node is not None and key != node.key:
    if key < node.key:
      node = node.left
    else:
      node = node.right
  return node


def tree_minimum(node):
  """Provided: return node with minimum key in subtree rooted at node."""
  while node.left is not None:
    node = node.left
  return node


def transplant(tree, u, v):
  """Provided: replace subtree rooted at node u with subtree rooted at node v.

  Updates parent's child pointer and v.parent. Does not update u.left or u.right.
  """
  if u.parent is None:
    tree.root = v
  elif u == u.parent.left:
    u.parent.left = v
  else:
    u.parent.right = v
  if v is not None:
    v.parent = u.parent


def bst_insert(tree, key):
  """Insert key into tree with parent pointers; return the new Node.

  Preconditions: key is comparable and distinct from existing keys in tree.
  Postconditions: tree satisfies BST search invariant; new node has correct parent.
  """
  # TODO 2.3A: Traverse downward to find parent slot, attach Node(key, parent=...), and update tree.root if empty.

  to_insert = Node(key)

  if (tree.root is None):

    tree.root = to_insert

  else:

    current = tree.root
    parent = None

    while current is not None:

      parent = current

      if key < current.key:

        current = current.left

      else:

        current = current.right

    to_insert.parent = parent

    if key < parent.key:

      parent.left = to_insert

    else:

      parent.right = to_insert

  return to_insert

def bst_delete(tree, key):

  """Delete key from tree, splicing/replacing nodes; return deleted Node (or None).

  Handles 0-child, 1-child, and 2-child cases using the in-order successor.
  Preserves BST search invariant and all parent pointers.
  """

  to_insert = Node(key)

  if (tree.root is None):

    return None

  current = tree.root

  while current is not None:

    if key < current.key:

      current = current.left

    elif key > current.key:

      current = current.right

    else:

      break
        
  if current is None or key != current.key:

    return None

  if current.left is None:

    transplant(tree, current, current.right)

  elif current.right is None:

    transplant(tree, current, current.left)
  
  else:

    minimum = tree_minimum(current.right)

    if minimum.parent != current:

      transplant(tree, minimum, minimum.right)
      minimum.right = current.right
      minimum.right.parent = minimum

    transplant(tree, current, minimum)
    minimum.left = current.left
    minimum.left.parent = minimum

  return current



if __name__ == "__main__":
  from lab_checks import check_bst
  raise SystemExit(check_bst(bst_insert, bst_delete))
