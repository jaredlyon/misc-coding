from __future__ import annotations

"""
Fibonacci Heap Implementation - LAZY DELETION VERSION

This variant implements lazy deletion for delete_min:
- Instead of immediately removing the min node, we mark it as "vacant" (val = None)
- Actual cleanup/consolidation is deferred until the next find_min or until explicitly needed
- This can improve performance when doing many consecutive delete operations

Key difference from standard: delete_min is O(1) instead of O(log n) amortized,
but find_min may trigger O(log n) cleanup when encountering a vacant node.
"""

class FibNode:
    """
    Node in a Lazy Fibonacci Heap.
    
    Same as standard FibNode, but val can be None to mark "vacant" (logically deleted) nodes.
    """
    def __init__(self, val: int):
        self.val = val          # None means this node is vacant (deleted)
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
    """
    Fibonacci Heap with Lazy Deletion.
    
    Main optimization: delete_min just marks the min as vacant (val = None)
    instead of immediately removing it. Cleanup happens later.
    """
    
    def __init__(self):
        """Initialize an empty lazy Fibonacci heap."""
        self.roots = []         # List of root nodes (may include vacant nodes)
        self.min = None         # Pointer to minimum (may be vacant)
        self.sorted_roots = []  # Cached sorted list of non-vacant roots for fast min lookup

    def __update_sorted_roots(self):
        """
        Maintain a sorted list of non-vacant roots.
        
        This allows O(1) lookup of the next minimum after a lazy deletion,
        since we can just scan through sorted_roots to find the first non-vacant node.
        """
        non_vacant = []
        for root in self.roots:
            if root.val is not None:  # Skip vacant nodes
                non_vacant.append(root)
        
        # Sort by value for quick min lookup
        self.sorted_roots = sorted(non_vacant, key=lambda node: node.val)
        
    def get_roots(self) -> list:
        """Returns a list of all root nodes (may include vacant nodes)."""
        return self.roots
    
    def find_min_lazy(self) -> FibNode:
        """
        Find the minimum element (lazy version).
        
        Key difference: If min is vacant (deleted), trigger cleanup before returning.
        This is where the deferred work from lazy deletions gets done.
        
        Time Complexity: O(1) if min is valid, O(log n) amortized if cleanup needed
        
        Returns:
            The node with minimum value, or None if heap is empty
        """
        if self.min is None:
            return None  # Heap is empty
        
        # If the min is vacant, time to do the cleanup we deferred!
        if self.min.val is None:
            self.__cleanup()
        
        return self.min
    
    def __cleanup(self):
        """
        Clean up all vacant nodes from the heap.
        
        This is where lazy deletions are actually processed:
        1. Remove vacant roots and promote their children
        2. Recursively clean vacant nodes from subtrees
        3. Consolidate to maintain O(log n) roots
        4. Find new minimum
        
        Time Complexity: O(log n) amortized
        """
        new_roots = []
        
        # Process each root
        for root in self.roots:
            if root.val is None:
                # This root is vacant - promote all its children to roots
                for child in root.children:
                    child.parent = None
                    child.flag = False
                    new_roots.append(child)
            else:
                # This root is valid - but clean any vacant nodes in its subtree
                self.__clean_subtree(root)
                new_roots.append(root)
        
        self.roots = new_roots
        
        if len(self.roots) == 0:
            # Heap is now empty
            self.min = None
            self.sorted_roots = []
        else:
            # Consolidate like in standard Fibonacci heap
            self.__consolidate()

    def __clean_subtree(self, node):
        """
        Recursively remove vacant nodes from a subtree.
        
        If a child is vacant, promote its children (grandchildren of node).
        Recurse on all valid children.
        
        Args:
            node: The root of the subtree to clean (assumed non-vacant)
        """
        if node.val is None:
            return  # Shouldn't happen, but be safe
        
        new_children = []
        for child in node.children:
            if child.val is None:
                # Child is vacant - promote grandchildren
                for grandchild in child.children:
                    grandchild.parent = node   # Grandchild's new parent is node
                    grandchild.flag = False
                    new_children.append(grandchild)
            else:
                # Child is valid - recurse and keep it
                self.__clean_subtree(child)
                new_children.append(child)
        
        node.children = new_children
    
    def __consolidate(self):
        """
        Consolidate trees so no two roots have the same degree.
        
        Same algorithm as standard Fibonacci heap:
        - Use degree table to merge trees with same degree
        - Smaller value becomes parent
        - Rebuild roots list and find new minimum
        
        After consolidation, update sorted_roots for fast min lookup.
        """
        degree_table = {}  # Maps degree -> node
        
        # Process each root, merging trees with same degree
        for root in self.roots:
            root.parent = None
            degree = len(root.children)
            
            # Keep merging while another tree has the same degree
            while degree in degree_table:
                other = degree_table[degree]
                
                # Ensure root has smaller value (min-heap property)
                if root.val > other.val:
                    root, other = other, root
                
                # Link other as child of root
                self.__link(other, root)
                del degree_table[degree]
                degree += 1
            
            degree_table[degree] = root
        
        # Rebuild roots from degree table
        self.roots = []
        self.min = None
        
        for node in degree_table.values():
            self.roots.append(node)
            if self.min is None or node.val < self.min.val:
                self.min = node
        
        # Update sorted_roots cache for fast next-min lookup
        self.__update_sorted_roots()

    def insert(self, val: int) -> FibNode:
        """
        Insert a new value into the heap.
        
        Same as standard Fibonacci heap insert.
        
        Time Complexity: O(1) (though we update sorted_roots which is O(r log r)
        where r is number of roots, kept small by consolidation)
        
        Args:
            val: The value to insert
            
        Returns:
            The newly created FibNode
        """
        new = FibNode(val)
        self.roots.append(new)
        
        # Update min pointer if this is the new minimum
        if self.min is None or val < self.min.val:
            self.min = new
        
        # Update sorted roots list for fast min lookup after deletions
        self.__update_sorted_roots()
        return new
        
    def delete_min_lazy(self) -> None:
        """
        Delete the minimum element (LAZY VERSION).
        
        KEY OPTIMIZATION: Don't actually remove the node!
        Just mark it as vacant (val = None) and update min pointer.
        
        The actual cleanup happens later in find_min_lazy or when needed.
        
        Time Complexity: O(1) - much faster than standard O(log n) delete_min!
        The work is deferred to the next find_min operation.
        
        Why is this useful?
        - If you do many delete_min operations followed by one find_min,
          you pay O(log n) once instead of O(log n) for each delete
        - Common in algorithms like Dijkstra's that extract many mins
        """
        if self.min is None:
            return  # Heap is empty
        
        # LAZY DELETION: Just mark as vacant, don't actually remove
        self.min.val = None
        
        # Find the next minimum from our cached sorted list
        self.min = None

        # This lookup is O(1) amortized since:
        # - sorted_roots has at most O(log n) elements (maintained by consolidation)
        # - There can only be one vacant root at a time (the old min)
        # - So we find the next valid root very quickly
        for root in self.sorted_roots:
            if root.val is not None:  # Skip the one vacant node
                self.min = root
                break

    def __link(self, child, parent):
        """
        Make child a child of parent (helper for consolidation).
        
        Same as standard Fibonacci heap.
        """
        child.parent = parent
        parent.children.append(child)
        child.flag = False

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        """
        Decrease the priority of a node.
        
        Same algorithm as standard Fibonacci heap, but with extra checks
        to handle vacant nodes (parent.val might be None).
        
        Time Complexity: O(1) amortized
        
        Args:
            node: The node to decrease
            new_val: The new (lower) value
        """
        node.val = new_val
        parent = node.parent
        
        # Cut if this violates heap property (but check parent isn't vacant)
        if parent is not None and parent.val is not None and node.val < parent.val:
            self.__cut(node, parent)
            self.__cut_recursive(parent)
        
        # Update min if this is the new minimum (check min isn't vacant)
        if self.min.val is not None and node.val < self.min.val:
            self.min = node

    def __cut(self, child, parent):
        """
        Cut a child from its parent and move to roots.
        
        Same as standard Fibonacci heap, but update sorted_roots cache.
        
        Args:
            child: Node to cut
            parent: Parent to cut from
        """
        parent.children.remove(child)
        child.parent = None
        self.roots.append(child)
        child.flag = False
        
        # Update sorted roots cache since we added a new root
        self.__update_sorted_roots()

    def __cut_recursive(self, node):
        """
        Perform cascading cuts up the tree.
        
        Same logic as standard Fibonacci heap:
        - Each node gets to lose one child before being cut
        - Flag tracks if a node has already lost a child
        - If flag is set, cut this node too (cascading)
        
        This maintains the structural properties needed for O(1) amortized decrease_priority.
        
        Args:
            node: Node to potentially cut
        """
        parent = node.parent
        
        if parent is not None:
            if not node.flag:
                # First child lost - mark it
                node.flag = True
            else:
                # Already lost a child - cut this node too (cascade)
                self.__cut(node, parent)
                self.__cut_recursive(parent)