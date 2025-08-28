# === README ===
# A simple weighted calculator for helping determine how much each person should pay for some groceries.
# Inspired by the fact boys eat more than girls, on average.

# === Adjustable Variables ===
total_cost = 94.11   # Total cost of groceries
x = 8                 # Number of boys
y = 4                 # Number of girls
ratio_x = 1.25        # Boys' weight (e.g., 1.5 means they pay 1.5x a girl's share)
ratio_y = 1.0         # Girls' weight (baseline = 1.0)

# === Calculation ===
# Total weighted "shares"
total_weight = (x * ratio_x) + (y * ratio_y)

# Cost per weight unit
cost_per_unit = total_cost / total_weight

# Individual shares
boy_share = cost_per_unit * ratio_x
girl_share = cost_per_unit * ratio_y

# === Output ===
print("=== Grocery Split ===")
print(f"Total Cost: ${total_cost:.2f}")
print(f"Boys: {x} (each pays ${boy_share:.2f})")
print(f"Girls: {y} (each pays ${girl_share:.2f})")
print(f"Check: ${(boy_share * x + girl_share * y):.2f} (should equal total)")