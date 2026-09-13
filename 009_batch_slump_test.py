slump_tests = [1, 4, 4, 6, 10, 1, 17]
slump_test_count = len(slump_tests)
acceptable_count = 0
too_stiff_count = 0
too_high_count = 0
for slump_test in slump_tests:
    if slump_test > 12.5:
        print(f"Slump test value: {slump_test} is too high.")
        too_high_count += 1
    elif slump_test < 2.5:
        print(f"Slump test value: {slump_test} is too stiff.")
        too_stiff_count += 1
    else:
        print(f"Slump test value: {slump_test} is in the acceptable range.")
        acceptable_count += 1

print("--- Batch Slump Test Summary ---")
print(f"Total samples tested: {slump_test_count}")
print(f"Acceptable samples: {acceptable_count}")
print(f"Too stiff samples: {too_stiff_count}")
print(f"Too high samples: {too_high_count}")