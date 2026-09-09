defects_per_km = 21
road_type = "street"  # "highway" or "local"
print(f"Defects per km: {defects_per_km}")
print(f"Road type: {road_type}")
if road_type == "highway":
    good_condition_threshold = 5
    moderate_condition_threshold = 15
    poor_condition_threshold = 30
    is_valid_road_type = True
elif road_type == "local":
    good_condition_threshold = 10
    moderate_condition_threshold = 20
    poor_condition_threshold = 35
    is_valid_road_type = True
else:
    is_valid_road_type = False
if is_valid_road_type:
    if defects_per_km < good_condition_threshold:
        print("Good condition")
    elif defects_per_km < moderate_condition_threshold:
        print("Moderate condition")
    elif defects_per_km < poor_condition_threshold:
        print("Poor condition")
    else:
        print("Critical condition")
else:
    print("Cannot determine condition due to unknown road type")