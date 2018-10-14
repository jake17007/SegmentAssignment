class DllistNode:

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.child = None


class Dllist:

    def __init__(self):
        self.top = None
        self.bottom = None

    def append_to_head(self, node):
        if not self.top and not self.bottom:  # List is empty
            self.top = node
            self.bottom = node
        else:                                 # List contains at least one node
            self.top.parent = node
            node.child = self.top
            self.top = node

    def trim_bottom(self):
        if self.bottom and self.bottom.parent:  # List contains multiple nodes
            self.bottom.parent.child = None
            self.bottom = self.bottom.parent
        elif self.bottom:                       # List contains one node
            self.bottom = None
            self.top = None

    def delete(self, node):
        if node.parent and node.child:  # Node is somewhere in middle of list
            node.parent.child = node.child
            node.child.parent = node.parent
        elif node.child:                # Node is at top of list
            node.child.parent = None
            self.top = node.child
        elif node.parent:               # Node is at bottom of list
            node.parent.child = None
            self.bottom = node.parent
        else:                           # Node is only one in list
            self.top = None
            self.bottom = None

    def move_to_top(self, node):
        if self.top == node:
            return
        self.delete(node)
        self.append_to_head(node)
