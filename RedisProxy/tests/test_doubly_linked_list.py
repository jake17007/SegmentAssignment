from unittest import TestCase

from RedisProxy.doubly_linked_list import (
    Dllist,
    DllistNode
)


class DllistNodeTest(TestCase):

    def setUp(self):
        self.node = DllistNode(1)

    def test_init(self):
        self.assertEqual(1, self.node.value)
        self.assertEqual(None, self.node.parent)
        self.assertEqual(None, self.node.child)


class DllistTest(TestCase):

    def setUp(self):
        self.dllist = Dllist()
        self.node1 = DllistNode(1)
        self.node2 = DllistNode(2)
        self.node3 = DllistNode(3)
        self.node4 = DllistNode(4)

    def test_append_to_head(self):

        # Append to empty dllist
        self.dllist.append_to_head(self.node1)
        self.assertEqual(self.node1, self.dllist.top)
        self.assertEqual(self.node1, self.dllist.bottom)

        # Append to dllist with one node (1)
        self.dllist.append_to_head(self.node2)
        self.assertEqual(self.node2, self.dllist.top)
        self.assertEqual(self.node1, self.dllist.bottom)

        # Append to dllist with two nodes (1, 2)
        self.dllist.append_to_head(self.node3)
        self.assertEqual(self.node3, self.dllist.top)
        self.assertEqual(self.node1, self.dllist.bottom)

    def test_trim_tail(self):

        self.dllist.append_to_head(self.node1)
        self.dllist.append_to_head(self.node2)
        self.dllist.append_to_head(self.node3)

        # Trim tail with three nodes (1, 2, 3)
        self.dllist.trim_tail()
        self.assertEqual(self.node3, self.dllist.top)
        self.assertEqual(self.node2, self.dllist.bottom)

        # Trim tail with two nodes (2, 3)
        self.dllist.trim_tail()
        self.assertEqual(self.node3, self.dllist.top)
        self.assertEqual(self.node3, self.dllist.bottom)

        # Trim tail with one node (3)
        self.dllist.trim_tail()
        self.assertEqual(None, self.dllist.top)
        self.assertEqual(None, self.dllist.bottom)

        # Trim empty dllist
        self.dllist.trim_tail()
        self.assertEqual(None, self.dllist.top)
        self.assertEqual(None, self.dllist.bottom)

    def test_delete(self):

        self.dllist.append_to_head(self.node1)
        self.dllist.append_to_head(self.node2)
        self.dllist.append_to_head(self.node3)
        self.dllist.append_to_head(self.node4)

        # Delete a middle node (1, [2], 3, 4)
        self.dllist.delete(self.node2)
        self.assertEqual(self.node4, self.dllist.top)
        self.assertEqual(self.node1, self.dllist.bottom)

        # Delete tail node ([1], 3, 4)
        self.dllist.delete(self.node1)
        self.assertEqual(self.node4, self.dllist.top)
        self.assertEqual(self.node3, self.dllist.bottom)

        # Delete top node (3, [4])
        self.dllist.delete(self.node4)
        self.assertEqual(self.node3, self.dllist.top)
        self.assertEqual(self.node3, self.dllist.bottom)

        # Delete last remaining node ([3])
        self.dllist.delete(self.node3)
        self.assertEqual(None, self.dllist.top)
        self.assertEqual(None, self.dllist.bottom)

def test_tester():
    import sys
    print('hello')
    print(sys.path)
