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

class FibHeapLazy:
    # init the empty heap
    def __init__(self):
        self.roots = []
        self.min = None
        self.sorted_roots = []

    # resorts roots when needed
    def __update_sorted_roots(self):
        non_vacant = []
        for root in self.roots:
            if root.val is not None:
                non_vacant.append(root)
        
        self.sorted_roots = sorted(non_vacant, key=lambda node: node.val)
        
    # returns a list of all roots in the heap
    def get_roots(self) -> list:
        return self.roots
    
    # returns the node with the minimum value
    def find_min_lazy(self) -> FibNode:
        if self.min is None:
            return None # empty
        
        if self.min.val is None:
            self.__cleanup()
        
        return self.min
    
    # cleanup vacant nodes
    def __cleanup(self):
        new_roots = []
        
        for root in self.roots:
            if root.val is None:
                for child in root.children:
                    child.parent = None
                    child.flag = False
                    new_roots.append(child)
            else:
                self.__clean_subtree(root)
                new_roots.append(root)
        
        self.roots = new_roots
        if len(self.roots) == 0:
            self.min = None
            self.sorted_roots = []
        else:
            self.__consolidate()

    # recursively clean vacant nodes from a subtree
    def __clean_subtree(self, node):
        if node.val is None:
            return
        
        new_children = []
        for child in node.children:
            if child.val is None:
                for grandchild in child.children:
                    grandchild.parent = node
                    grandchild.flag = False
                    new_children.append(grandchild)
            else:
                self.__clean_subtree(child)
                new_children.append(child)
        
        node.children = new_children
    
    # consolidate trees so no two roots have the same degree
    def __consolidate(self):
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
        
        self.__update_sorted_roots()

    # inserts a new node into the heap
    def insert(self, val: int) -> FibNode:
        new = FibNode(val)
        self.roots.append(new)
        if self.min is None or val < self.min.val:
            self.min = new
        
        # Update sorted roots list
        self.__update_sorted_roots()
        return new
        
    # deletes the minimum node from the heap
    def delete_min_lazy(self) -> None:
        if self.min is None:
            return
        
        self.min.val = None
        
        self.min = None

        # this lookup is guaranteed to be O(1) since we maintain a sorted list of roots
        # and there can only be one vacant node at a time (the old min)
        for root in self.sorted_roots:
            if root.val is not None: # skip
                self.min = root
                break

    # connects a child node to a parent node
    def __link(self, child, parent):
        child.parent = parent
        parent.children.append(child)
        child.flag = False

    # decrease the priority of a node and cut of children if necessary
    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        node.val = new_val
        parent = node.parent
        
        if parent is not None and parent.val is not None and node.val < parent.val:
            self.__cut(node, parent)
            self.__cut_recursive(parent)
        
        if self.min.val is not None and node.val < self.min.val:
            self.min = node

    # cut a child node and send it to the root
    def __cut(self, child, parent):
        parent.children.remove(child)
        child.parent = None
        self.roots.append(child)
        child.flag = False
        # Update sorted roots after adding new root
        self.__update_sorted_roots()

    # recursively cut parent nodes if they have already lost a child
    def __cut_recursive(self, node):
        parent = node.parent
        
        if parent is not None:
            if not node.flag:
                node.flag = True
            else:
                self.__cut(node, parent)
                self.__cut_recursive(parent)