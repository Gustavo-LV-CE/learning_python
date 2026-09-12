concrete_slump_result = 13
consistency = "Medium"  # Low, Medium or High
has_additives = True  # True or False
if not (0 <= concrete_slump_result <= 30):
    print("Invalid slump result: out of range (0-30 cm)")
    is_valid_sample = False
elif concrete_slump_result > 18 and not has_additives:
    print("A slump over 18 without additives will not be accepted")
    is_valid_sample = False
else:
    if consistency == "Low":
        low_end_slump_threshold = 0.0
        high_end_slump_threshold = 6.5
        is_valid_sample = True
    elif consistency == "Medium":
        low_end_slump_threshold = 2.5
        high_end_slump_threshold = 12.5
        is_valid_sample = True
    elif consistency == "High":
        low_end_slump_threshold = 6.5
        high_end_slump_threshold = 18.0
        is_valid_sample = True
    else:
        print("Unknown consistency type.")
        is_valid_sample = False
if is_valid_sample and has_additives and consistency == "High":
    high_end_slump_threshold = 25.0
if is_valid_sample:
    print(f"Concrete slump result: {concrete_slump_result} centimeters, consistency: {consistency}.")
    if concrete_slump_result < low_end_slump_threshold:
        print("Concrete is too stiff.")
    elif low_end_slump_threshold <= concrete_slump_result <= high_end_slump_threshold:
        print("Concrete slump is within acceptable range.")
    elif concrete_slump_result > high_end_slump_threshold:
        print("Concrete is too fluid.")