"""
File: linkedbst.py
Author: Ken Lambert
This module contains class LinkedBST, which implements Binary Search Tree.
There is comparison of different methods of searching the words.
"""

from random import shuffle
from time import time
from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_tree = ""
            if node is not None:
                str_tree += recurse(node.right, level + 1)
                str_tree += "| " * level
                str_tree += str(node.data) + "\n"
                str_tree += recurse(node.left, level + 1)
            return str_tree

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)


    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()
        stack = LinkedStack()
        node = self._root
        while node is not None or not stack.isEmpty():
            if node is not None:
                stack.push(node)
                node = node.left
            else:
                item = stack.pop()
                lyst.append(item.data)
                node = item.right
        return iter(lyst)


    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None


    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root
        while node is not None:
            if node.data == item:
                return node.data
            if item < node.data:
                node = node.left
            else:
                node = node.right
        return None


    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0


    def add(self, item):
        """Adds item to the tree."""
        self._size += 1
        curr = self._root
        parent = None
        if curr is None:
            self._root = BSTNode(item)
        else:
            while curr:
                parent = curr
                if item < curr.data:
                    curr = curr.left
                else:
                    curr = curr.right
            if item < parent.data:
                parent.left = BSTNode(item)
            else:
                parent.right = BSTNode(item)


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed


    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None


    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        size = self._size
        return height < (2 * log(size + 1, 2) - 1)


    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        root = self._root
        lst = []
        def recurse(root, low, high, lst):
            if root.data > low and root.left is not None:
                root1 = root.left
                recurse(root1, low, high, lst)
            if low <= root.data <= high:
                lst.append(root.data)
            if root.data < high and root.right is not None:
                root2 = root.right
                recurse(root2, low, high, lst)
            return lst
        recurse(root, low, high, lst)
        return lst


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        sorted_tree = list(self.inorder())
        self.clear()
        stack = LinkedStack()
        center_pos = int(len(sorted_tree) / 2)
        self.add(sorted_tree.pop(center_pos))
        left = sorted_tree[:center_pos]
        right = sorted_tree[center_pos:]
        stack.push(left)
        stack.push(right)
        while not stack.isEmpty():
            elems = stack.pop()
            if len(elems) > 0:
                center_pos = int(len(elems) / 2)
                self.add(elems.pop(center_pos))
                left = elems[:center_pos]
                right = elems[center_pos:]
                stack.push(left)
                stack.push(right)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        root = self._root
        succ = None
        while root:
            if root.data > item:
                succ = root.data
                root = root.left
            elif root.data <= item:
                root = root.right
        return succ


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        root = self._root
        pred = None
        while root:
            if root.data >= item:
                root = root.left
            elif root.data < item:
                pred = root.data
                root = root.right
        return pred


    @staticmethod
    def read_file(path: str) -> list:
        """Reads file with words and returns a list of them."""
        words = []
        with open(path, encoding='utf-8') as words_file:
            for word in words_file:
                words.append(word.strip())
        return words


    @staticmethod
    def random_words(words: list) -> list:
        """Returns 10,000 random words after reading them from file."""
        rand_words = list(set(words))
        return rand_words[:10000]


    @staticmethod
    def list_search(words: list, random_words: list) -> float:
        """Returns the time of search of 10,000 words in the list after reading them from file."""
        start = time()
        found = 0
        for word in random_words:
            try:
                words.index(word)
                found += 1
            except ValueError:
                continue
        print(f"List search found {found} words.")
        return time() - start


    def order_tree_search(self, words: list, random_words: list) -> float:
        """Returns time of search of 10,000 words in the binary search tree,
        the elements of which were added by order."""
        self.clear()
        for word in words:
            self.add(word)
        start = time()
        found = 0
        for word in random_words:
            if self.find(word):
                found += 1
        print(f"Ordered tree search found {found} words.")
        return time() - start


    def disorder_tree_search(self, words: list, random_words: list) -> float:
        """Returns time of search of 10,000 words in the binary search tree,
        the elements of which were added without order (randomly)."""
        self.clear()
        words_set = set(words)
        for word in words_set:
            self.add(word)
        start = time()
        found = 0
        for word in random_words:
            if self.find(word):
                found += 1
        print(f"Disordered tree search found {found} words.")
        return time() - start


    def balanced_tree_search(self, random_words: list) -> float:
        """Returns time of search of 10,000 words in the balanced binary search tree."""
        self.rebalance()
        start = time()
        found = 0
        for word in random_words:
            if self.find(word):
                found += 1
        print(f"Balanced tree search found {found} words.")
        return time() - start


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = self.read_file(path)
        random_words = self.random_words(words)
        lst_sec = round(self.list_search(words, random_words), 5)
        print(f'List search took {lst_sec} seconds.')
        order_tree_sec = round(self.order_tree_search(words, random_words), 5)
        print(f'Ordered tree search took {order_tree_sec} seconds.')
        disord_tree_sec = round(self.disorder_tree_search(words, random_words), 5)
        print(f'Disordered tree search took {disord_tree_sec} seconds.')
        bal_tree_sec = round(self.balanced_tree_search(random_words), 5)
        print(f'Balanced tree search took {bal_tree_sec} seconds.')


if __name__ == "__main__":
    tree = LinkedBST()
    tree.demo_bst('words.txt')
