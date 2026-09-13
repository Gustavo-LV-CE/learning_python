slump_tests = [1, 4, 4, 6, 10, 1, 17]
slump_test_count = len(slump_tests)
average_slump = sum(slump_tests) / slump_test_count
min_slump = min(slump_tests)
max_slump = max(slump_tests)
slump_range = max_slump - min_slump
LOW_LIMIT = 2.5
HIGH_LIMIT = 12.5
acceptable_count = 0
too_stiff_count = 0
too_high_count = 0
for slump_test in slump_tests:
    if slump_test > HIGH_LIMIT:
        print(f"Slump test value: {slump_test} is too high.")
        too_high_count += 1
    elif slump_test < LOW_LIMIT:
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
print(f"Average slump test value: {average_slump:.2f} cm")
print(f"Minimum slump test value: {min_slump:.2f} cm")
print(f"Maximum slump test value: {max_slump:.2f} cm")
print(f"Range of slump test values: {slump_range:.2f} cm")