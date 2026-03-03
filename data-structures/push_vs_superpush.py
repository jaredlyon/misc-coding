class Stack:
    def __init__(self):
        self.items = []
    
    @staticmethod
    def create():
        return Stack()
    
    def push(self, x):
        self.items.append(x)
    
    def pop(self):
        if not self.items:
            raise IndexError("popped from empty stack")
        return self.items.pop()


def create():
    S = Stack.create()
    
    def push(x):
        S.push(x)
    
    def pop():
        return S.pop()
    
    def superpop(k, A):
        # k is an integer, A is an array with size >= k
        i = 0
        while i < k:
            A[i] = S.pop()
            i = i + 1
    
    def superpush(k, A):
        # k is an integer, A is an array with size >= k
        i = 0
        while i < k:
            S.push(A[i])
            i = i + 1
    
    return push, pop, superpop, superpush


def test_push_only(n, test_num):
    import time
    
    push, pop, superpop, superpush = create()
    
    start_time = time.perf_counter()
    for i in range(n):
        push(i)
    end_time = time.perf_counter()
    
    elapsed_time = end_time - start_time
    amortized_time = elapsed_time / n
    ops_per_sec = n / elapsed_time
    
    return {
        'test': f'Push Test {test_num}',
        'n': n,
        'method': 'push',
        'total_time': elapsed_time,
        'amortized_time': amortized_time,
        'ops_per_sec': ops_per_sec
    }


def test_superpush_only(n, batch_size, test_num):
    import time
    
    push, pop, superpop, superpush = create()
    
    num_batches = n // batch_size
    actual_n = num_batches * batch_size
    
    start_time = time.perf_counter()
    for i in range(num_batches):
        arr = list(range(batch_size))
        superpush(batch_size, arr)
    end_time = time.perf_counter()
    
    elapsed_time = end_time - start_time
    amortized_time = elapsed_time / actual_n
    ops_per_sec = actual_n / elapsed_time
    
    return {
        'test': f'Superpush Test {test_num}',
        'n': actual_n,
        'method': f'superpush(k={batch_size})',
        'batch_size': batch_size,
        'num_batches': num_batches,
        'total_time': elapsed_time,
        'amortized_time': amortized_time,
        'ops_per_sec': ops_per_sec
    }


def print_result(result):
    print(f"{result['test']}: {result['method']}")
    print(f"  Total elements: {result['n']:,}")
    if 'batch_size' in result:
        print(f"  Batch size: {result['batch_size']}, Batches: {result['num_batches']}")
    print(f"  Total time: {result['total_time']:.6f}s")
    print(f"  Amortized time per element: {result['amortized_time']:.9f}s")
    print(f"  Operations per second: {result['ops_per_sec']:,.2f}")
    print()


def compare_results(push_results, super_results):
    avg_push_time = sum(r['amortized_time'] for r in push_results) / len(push_results)
    avg_super_time = sum(r['amortized_time'] for r in super_results) / len(super_results)
    
    avg_push_ops = sum(r['ops_per_sec'] for r in push_results) / len(push_results)
    avg_super_ops = sum(r['ops_per_sec'] for r in super_results) / len(super_results)
    
    print("Average Amortized Time Per Element:")
    print(f"  Regular push:  {avg_push_time:.9f}s")
    print(f"  Superpush:     {avg_super_time:.9f}s")
    print(f"  Ratio (super/push): {avg_super_time/avg_push_time:.4f}x")
    print()
    
    print("Average Operations Per Second:")
    print(f"  Regular push:  {avg_push_ops:,.2f} ops/s")
    print(f"  Superpush:     {avg_super_ops:,.2f} ops/s")
    print(f"  Ratio (super/push): {avg_super_ops/avg_push_ops:.4f}x")
    print()
    
    print("Individual Test Comparisons:")
    for i in range(min(len(push_results), len(super_results))):
        p = push_results[i]
        s = super_results[i]
        ratio = s['amortized_time'] / p['amortized_time']
        print(f"  Test {i+1} ({p['n']:,} elements): Superpush is {ratio:.4f}x the time of regular push")
    print()


if __name__ == "__main__":
    import time
    
    print("REGULAR PUSH TESTS")
    print("-" * 70)
    push_results = []
    push_results.append(test_push_only(10_000, 1))
    print_result(push_results[-1])
    
    push_results.append(test_push_only(100_000, 2))
    print_result(push_results[-1])
    
    push_results.append(test_push_only(1_000_000, 3))
    print_result(push_results[-1])
    
    push_results.append(test_push_only(10_000_000, 4))
    print_result(push_results[-1])
    
    push_results.append(test_push_only(100_000_000, 5))
    print_result(push_results[-1])
    
    push_results.append(test_push_only(1_000_000_000, 6))
    print_result(push_results[-1])
    
    print("SUPERPUSH TESTS")
    print("-" * 70)
    super_results = []
    super_results.append(test_superpush_only(10_000, 10, 1))
    print_result(super_results[-1])
    
    super_results.append(test_superpush_only(100_000, 100, 2))
    print_result(super_results[-1])
    
    super_results.append(test_superpush_only(1_000_000, 1000, 3))
    print_result(super_results[-1])
    
    super_results.append(test_superpush_only(10_000_000, 10000, 4))
    print_result(super_results[-1])
    
    super_results.append(test_superpush_only(100_000_000, 100000, 5))
    print_result(super_results[-1])
    
    super_results.append(test_superpush_only(1_000_000_000, 1000000, 6))
    print_result(super_results[-1])
    
    print("COMPARISON")
    print("-" * 70)
    compare_results(push_results, super_results)
