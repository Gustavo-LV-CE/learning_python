concrete_slump_result = 19
consistency = "High"  # Low, Medium or High
has_additives = True  # True or False
if concrete_slump_result < 0 or concrete_slump_result > 30:
    print("Invalid slump result: out of range (0-30 cm)")
else:
    if concrete_slump_result > 18 and not has_additives:
        print("A slump over 18 without additives will not be accepted")
    else:
        print(f"Concrete slump result: {concrete_slump_result} centimeters, consistency: {consistency}")
        if consistency == "Low":
            low_end_slump_threshold = 0.0
            high_end_slump_threshold = 6.5
            is_valid_consistency = True
        elif consistency == "Medium":
            low_end_slump_threshold = 2.5
            high_end_slump_threshold = 12.5
            is_valid_consistency = True
        elif consistency == "High":
            low_end_slump_threshold = 6.5
            high_end_slump_threshold = 18.0
            is_valid_consistency = True
        else:
            print("Unknown consistency type")
            is_valid_consistency = False
        if is_valid_consistency:
            if concrete_slump_result < low_end_slump_threshold:
                print("Concrete is too stiff")
            elif concrete_slump_result > high_end_slump_threshold:
                print("Concrete is too fluid.")
                if has_additives and concrete_slump_result > 18 and consistency == "High":
                    print("When high consistency is specified, a slump over 18 with additives will be accepted")
            else:
                print("Concrete slump is within acceptable range")