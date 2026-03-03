from __future__ import annotations

"""
Fibonacci Heap Implementation - Standard Version

A Fibonacci heap is a data structure for priority queue operations with excellent amortized time complexity.
Key properties:
- It's a collection of min-heap-ordered trees (parent ≤ children)
- Trees are not necessarily binomial; they can have any shape
- Provides O(1) amortized time for insert, find-min, and decrease-key
- Provides O(log n) amortized time for delete-min
"""

class FibNode:
    """
    Node in a Fibonacci Heap.
    
    Each node stores:
    - val: the priority/key value
    - parent: reference to parent node (None if root)
    - children: list of child nodes
    - flag: marks if node has lost a child since becoming a child itself
           (used in cascading cuts to maintain heap structure)
    """
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []  # list of child nodes
        self.flag = False   # False initially, set to True after first child cut

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val

class FibHeap:
    """
    Fibonacci Heap - A collection of min-heap-ordered trees.
    
    Main idea: Keep operations lazy and defer expensive work until necessary.
    This gives excellent amortized performance.
    """
    
    def __init__(self):
        """Initialize an empty Fibonacci heap."""
        self.roots = []      # List of root nodes (forest of trees)
        self.min = None      # Pointer to the root with minimum value
        self.node_count = 0  # Total number of nodes in the heap

    def get_roots(self) -> list:
        """Returns a list of all root nodes in the heap."""
        return self.roots
    
    def find_min(self) -> FibNode:
        """
        Find the minimum element in the heap.
        
        Time Complexity: O(1) - we maintain a pointer to the min
        
        Returns:
            The node with the minimum value, or None if heap is empty
        """
        return self.min

    def insert(self, val: int) -> FibNode:
        """
        Insert a new value into the heap.
        
        Strategy: Just create a new tree with a single node and add it to roots.
        Don't consolidate yet - keep it lazy!
        
        Time Complexity: O(1)
        
        Args:
            val: The value/priority to insert
            
        Returns:
            The newly created FibNode (useful for later decrease_priority operations)
        """
        new = FibNode(val)
        self.roots.append(new)  # Add as a new tree in the forest
        self.node_count += 1
        
        # Update min pointer if this is the new minimum
        if self.min is None or val < self.min.val:
            self.min = new
        
        return new
        
    def delete_min(self) -> None:
        """
        Delete the minimum element from the heap.
        
        This is the most complex operation! Steps:
        1. Remove the min node
        2. Promote all its children to be new roots
        3. CONSOLIDATE: Merge trees of the same degree until no two roots have the same degree
           This is where we pay for all the lazy operations
        4. Find the new minimum among the roots
        
        Time Complexity: O(log n) amortized
        
        Why consolidate? To keep the number of roots bounded by O(log n),
        which ensures future operations remain efficient.
        """
        if self.min is None:
            return  # Heap is empty, nothing to delete
        
        to_delete = self.min
        
        # Step 1 & 2: Promote all children of min to be new roots
        for node in to_delete.children:
            node.parent = None   # No longer has a parent
            node.flag = False    # Reset flag when becoming a root
            self.roots.append(node)

        # Remove the old min from roots
        self.roots.remove(to_delete)
        self.node_count -= 1
        
        if len(self.roots) == 0:
            # Heap is now empty
            self.min = None
        else:
            # Step 3: CONSOLIDATION - the key operation that maintains heap efficiency
            # Goal: Ensure no two roots have the same degree (number of children)
            # This keeps the number of roots at O(log n)
            degree_table = {}  # Maps degree -> node with that degree
            
            # Process each root and merge trees with the same degree
            for root in self.roots:
                root.parent = None  # Ensure it's a root
                degree = len(root.children)  # Degree = number of children
                
                # Keep merging while there's another tree with the same degree
                while degree in degree_table:
                    other = degree_table[degree]  # Found a tree with same degree

                    # Make the smaller value the parent (maintain min-heap property)
                    if root.val > other.val:
                        root, other = other, root  # Swap so root has smaller value
                    
                    # Link other as a child of root
                    self.__link(other, root)
                    del degree_table[degree]  # This degree is now handled
                    degree += 1  # New tree has degree increased by 1
                
                # Store this tree in the degree table
                degree_table[degree] = root
            
            # Step 4: Rebuild roots list and find new minimum
            self.roots = []
            self.min = None
            
            # All remaining trees in degree_table are our new roots
            for node in degree_table.values():
                self.roots.append(node)
                # Update min pointer if this is the new minimum
                if self.min is None or node.val < self.min.val:
                    self.min = node

    def __link(self, child, parent):
        """
        Make child a child of parent (helper for consolidation).
        
        Args:
            child: Node to become a child
            parent: Node to become the parent
        """
        child.parent = parent
        parent.children.append(child)
        child.flag = False  # Reset flag when a node becomes a child

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        """
        Decrease the priority (value) of a node.
        
        This is a key operation that makes Fibonacci heaps special!
        
        Strategy:
        - If decreasing violates heap property with parent, cut the node and move to roots
        - Use cascading cuts to prevent trees from becoming too unbalanced
        
        Time Complexity: O(1) amortized
        
        Args:
            node: The node whose priority to decrease
            new_val: The new (lower) priority value
        """
        node.val = new_val
        parent = node.parent
        
        # If this violates the min-heap property (node < parent), cut it
        if parent is not None and node.val < parent.val:
            self.__cut(node, parent)       # Move node to roots
            self.__cut_recursive(parent)   # Cascading cuts if needed
        
        # Update min pointer if this is now the minimum
        if node.val < self.min.val:
            self.min = node

    def __cut(self, child, parent):
        """
        Cut a child from its parent and move it to the roots.
        
        Args:
            child: The node to cut
            parent: The parent to cut from
        """
        parent.children.remove(child)  # Remove from parent's children list
        child.parent = None            # No longer has a parent
        self.roots.append(child)       # Becomes a new root
        child.flag = False             # Reset flag for roots

    def __cut_recursive(self, node):
        """
        Perform cascading cuts up the tree.
        
        This is the key to maintaining amortized O(1) decrease_priority!
        
        Logic:
        - Each node is allowed to lose ONE child before being cut itself
        - The flag tracks whether a node has already lost a child
        - If flag is False: set it to True ("you get one free pass")
        - If flag is True: this node has already lost a child, so cut it too
          and recursively check its parent
        
        Why? This prevents trees from becoming too shallow/unbalanced,
        maintaining the O(log n) bound on tree height.
        
        Args:
            node: The node to potentially cut
        """
        parent = node.parent
        
        if parent is not None:  # Only cut if not already a root
            if not node.flag:
                # First child lost - mark it but don't cut
                node.flag = True
            else:
                # Already lost a child before - cut this one too (cascading cut)
                self.__cut(node, parent)
                self.__cut_recursive(parent)  # Recursively check parent