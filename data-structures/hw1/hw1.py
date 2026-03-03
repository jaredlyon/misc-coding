def analyze_decrement_amortized_cost(initial_capacity=2048):
    # Initialize the dynamic array state
    capacity = initial_capacity
    size = initial_capacity  # Start with a full array
    
    # Tracking variables
    total_actual_cost = 0
    num_resizes = 0
    resize_costs = []
    operations_between_resizes = []
    current_ops_since_resize = 0
    op_num = 0
    
    print(f"\n{'='*80}")
    print(f"Dynamic Array Decrement Simulation")
    print(f"{'='*80}")
    print(f"Initial: capacity={capacity}, size={size}")
    print(f"Resize to m/2 when size < m/8")
    print(f"{'='*80}\n")
    
    # Simulate decrement operations until array is empty
    while size > 0:
        op_num += 1
        # Each decrement has base cost of 1
        operation_cost = 1
        
        # Perform the decrement
        size -= 1
        current_ops_since_resize += 1
        
        resize_triggered = False
        threshold = capacity / 8
        
        # Check if we need to resize (shrink)
        if size < threshold:
            # Resize is triggered
            resize_cost = size  # Cost to copy all elements to new array
            new_capacity = capacity // 2
            
            resize_triggered = True
            operation_cost += resize_cost
            num_resizes += 1
            resize_costs.append(resize_cost)
            operations_between_resizes.append(current_ops_since_resize)
            
            print(f"Op {op_num:3d}: size={size:3d} < {threshold:.1f} (capacity/8) → RESIZE")
            print(f"         capacity: {capacity} → {new_capacity}")
            print(f"         resize_cost={resize_cost}, op_cost={operation_cost}, total_cost={total_actual_cost + operation_cost}")
            
            capacity = new_capacity
            current_ops_since_resize = 0
        else:
            # Normal operation
            print(f"Op {op_num:3d}: size={size:3d}, capacity={capacity:3d}, threshold={threshold:.1f}, op_cost={operation_cost}, total_cost={total_actual_cost + operation_cost}")
        
        total_actual_cost += operation_cost
    
    # Calculate metrics from the simulation
    num_operations = op_num
    amortized_cost = total_actual_cost / num_operations
    
    # Calculate theoretical values from actual resize data
    if num_resizes > 0:
        avg_resize_cost = sum(resize_costs) / len(resize_costs)
        avg_ops_between = sum(operations_between_resizes) / len(operations_between_resizes)
        
        # Additional cost of expensive operation
        additional_cost = avg_resize_cost
        
        # Calculate additional savings for each resize cycle
        savings_per_cycle = []
        for i in range(len(resize_costs)):
            if operations_between_resizes[i] > 0:
                savings = resize_costs[i] / operations_between_resizes[i]
                savings_per_cycle.append(savings)
        
        # Additional savings required per operation
        if avg_ops_between > 0:
            additional_savings = additional_cost / avg_ops_between
        else:
            additional_savings = 0
        
        # Get min, max savings
        if savings_per_cycle:
            min_savings = min(savings_per_cycle)
            max_savings = max(savings_per_cycle)
        else:
            min_savings = 0
            max_savings = 0
        
        # Amortized time = base cost + additional savings
        calculated_amortized = 1 + additional_savings
    else:
        avg_resize_cost = 0
        avg_ops_between = 0
        additional_cost = 0
        additional_savings = 0
        min_savings = 0
        max_savings = 0
        calculated_amortized = 1
    
    print(f"\n{'='*80}")
    print(f"Simulation Results")
    print(f"{'='*80}")
    print(f"Total operations:                    {num_operations}")
    print(f"Total cost:                          {total_actual_cost}")
    print(f"Number of resizes:                   {num_resizes}")
    print(f"Average resize cost:                 {avg_resize_cost:.2f}")
    print(f"Average operations between resizes:  {avg_ops_between:.2f}")
    print(f"Actual amortized cost (simulated):   {amortized_cost:.4f}")
    print(f"{'='*80}\n")
    
    print(f"{'='*80}")
    print(f"SOLUTION: Amortized Analysis")
    print(f"{'='*80}")
    print(f"\n✓ Additional cost of expensive operation (C/8):")
    print(f"    Theoretical: C/8 (where C is capacity before resize)")
    print(f"    From simulation: {additional_cost:.2f}")
    print(f"\n✓ Additional savings required per operation:")
    print(f"    Theoretical: 2")
    print(f"    From simulation (average): {additional_savings:.4f}")
    print(f"    From simulation (minimum): {min_savings:.4f}")
    print(f"    From simulation (maximum): {max_savings:.4f}")
    print(f"\n✓ Amortized time for Decrement operation:")
    print(f"    Theoretical: 1 (base) + 2 (savings) = 3, which is O(1)")
    print(f"    From simulation: {calculated_amortized:.4f}, which is O(1)")
    print(f"\n{'='*80}\n")
    
    return {
        'total_operations': num_operations,
        'total_cost': total_actual_cost,
        'amortized_cost': amortized_cost,
        'num_resizes': num_resizes,
        'additional_cost': additional_cost,
        'additional_savings': additional_savings,
        'calculated_amortized': calculated_amortized
    }


def main():
    results = analyze_decrement_amortized_cost(initial_capacity=2048)
    # problem2_function()


if __name__ == "__main__":
    main()
