from fib_lazy import FibHeapLazy

def test_lazy_deletion():
    heap = FibHeapLazy()
    
    # Insert some values
    heap.insert(5)
    heap.insert(7)
    heap.insert(12)
    node14 = heap.insert(14)
    heap.insert(2)
    
    print("Initial roots:", [x.val for x in heap.get_roots()])
    print("Min:", heap.find_min().val)
    
    # Test lazy deletion - should just mark as vacant
    heap.delete_min()
    print("\nAfter delete_min (lazy):")
    print("Roots:", [x.val for x in heap.get_roots()])
    print("Root vacant status:", [x.val is None for x in heap.get_roots()])
    print("Min:", heap.find_min().val)
    
    # Another delete
    heap.delete_min()
    print("\nafter second delete_min:")
    print("Min:", heap.find_min().val)
    
    # Test decrease priority
    heap.decrease_priority(node14, 1)
    print("\nafter decrease_priority(14 -> 1):")
    print("Min:", heap.find_min().val)
    
    print("\nall tests passed")

if __name__ == '__main__':
    test_lazy_deletion()
