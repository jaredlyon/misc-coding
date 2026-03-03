from __future__ import annotations

class FibNode:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val

class FibHeap:
    # init the empty heap
    def __init__(self):
        self.roots = []
        self.min = None
        self.node_count = 0

    # returns a list of all roots in the heap
    def get_roots(self) -> list:
        return self.roots
    
    # returns the node with the minimum value
    def find_min(self) -> FibNode:
        return self.min

    # inserts a new node into the heap
    def insert(self, val: int) -> FibNode:
        new = FibNode(val)
        self.roots.append(new)
        self.node_count += 1
        if self.min is None or val < self.min.val : self.min = new
        return new
        
    # deletes the minimum node from the heap and consolidates remaining values
    def delete_min(self) -> None:
        if self.min is None:
            return # empty
        
        to_delete = self.min
        for node in to_delete.children:
            node.parent = None
            node.flag = False
            self.roots.append(node)

        self.roots.remove(to_delete)
        self.node_count -= 1
        
        if len(self.roots) == 0:
            self.min = None
        else:
            degree_table = {}
            
            for root in self.roots:
                root.parent = None
                degree = len(root.children)
                
                while degree in degree_table:
                    other = degree_table[degree]

                    if root.val > other.val:
                        root, other = other, root
                    
                    self.__link(other, root)
                    del degree_table[degree]
                    degree += 1
                
                degree_table[degree] = root
            
            self.roots = []
            self.min = None
            
            for node in degree_table.values():
                self.roots.append(node)
                if self.min is None or node.val < self.min.val:
                    self.min = node

    # connects a child node to a parent node
    def __link(self, child, parent):
        child.parent = parent
        parent.children.append(child)
        child.flag = False

    # decrease the priority of a node and cut of children if necessary
    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        node.val = new_val
        parent = node.parent
        
        if parent is not None and node.val < parent.val:
            self.__cut(node, parent)
            self.__cut_recursive(parent)
        
        if node.val < self.min.val:
            self.min = node

    # cut a child node and send it to the root
    def __cut(self, child, parent):
        parent.children.remove(child)
        child.parent = None
        self.roots.append(child)
        child.flag = False

    # recursively cut parent nodes if they have already lost a child
    def __cut_recursive(self, node):
        parent = node.parent
        
        if parent is not None:
            if not node.flag:
                node.flag = True
            else:
                self.__cut(node, parent)
                self.__cut_recursive(parent)