# explanations for member functions are provided in requirements.py
from __future__ import annotations

import math

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
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.min_node =  None
        self.num_nodes = 0

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        # create new node
        new_node = FibNode(val)
        # add new node to roots
        self.roots.append(new_node)
        # update counter for total nodes in fib heap
        self.num_nodes += 1
        # update the min pointer if needed
        self._update_min()
        return new_node
        
    def delete_min_lazy(self) -> None:
        # Lazy becomes O(1) because you just put in vacant node
        # Update node value from number to None
        if self.min_node:
            self.min_node.val = None

    def find_min_lazy(self):
        if not self.roots:
            return None
        
        # Only consolidate & update min if current min is None
        if self.min_node.val is None:
            vacant_roots = [r for r in self.roots if r.val is None]
            for v in vacant_roots:
                self._promote_nonvacant_nodes(v)

            self.roots = [r for r in self.roots if r.val is not None]

            if not self.roots:
                return None
            
            self._consolidate()
            self._update_min()

        return self.min_node

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        node.val = new_val
        self._promote(node)
        self._update_min()


    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define

    def _update_min(self):
        min_node = None 
        for root in self.roots:
            if root.val is not None:
                if min_node is None or root.val < min_node.val:
                    min_node = root 
        self.min_node = min_node


    def _promote(self, x: FibNode):
        
        if x.parent is None:
            return
        p = x.parent
        p.children = [c for c in p.children if c is not x]
        
        x.parent = None
        x.flag = False
        self.roots.append(x)

        # parent promote if it lost 2 children now, using flags for this
        if p.flag and p.val is not None:
            self._promote(p)
        elif p.parent is not None:
            p.flag = True


    def _merge_y_to_x(self, x: FibNode, y: FibNode):
        x.children.append(y)
        y.parent = x

    def _find_array_size(self, x):
        # array size = ceil(log(n)) + 1
        return math.ceil(math.log2(x)) + 1

    def _consolidate(self):
        # make the degree array
        # array size = ceil(log(n)) + 1
        size = self._find_array_size(self.num_nodes)
        arr = [None] * size
        while self.roots:
            # get first root in our list (start from left to right)
            # remove it from self.roots & make deg array point to it
            x = self.roots[0]
            deg = len(x.children)
            self.roots.remove(x)

            # possible chain merging
            while arr[deg] is not None:
                # y = the heap we already seen with degree deg
                y = arr[deg]
                # figure out who becomes the root of the merged tree
                # should be no case where there's any vacant node in roots during consolidation
                if x.val > y.val:
                    # we want to make sure x is the one with smaller value
                    x, y = y, x
                
                # merge them
                self._merge_y_to_x(x, y)

                # reset this index in degree array
                arr[deg] = None
                
                # update degree since we merged so children + 1
                deg += 1

            # set pointer
            arr[deg] = x

        # Put back in our self.roots list after all the merging
        for a in arr:
            if a is not None:
                self.roots.append(a)

    def _promote_nonvacant_nodes(self, x: FibNode):
        # Need to find non-vacant and promote to root
        if x.val is not None:
            self._promote(x)
        else:
            for child in list(x.children):
                self._promote_nonvacant_nodes(child)
        return