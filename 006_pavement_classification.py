defects_per_km = 2
print(f"Defects per km: {defects_per_km}")
if defects_per_km < 5:
    print("Good condition")
elif defects_per_km < 15:
    print("Moderate condition")
elif defects_per_km < 30:
    print("Poor condition")
else:
    print("Critical condition")
