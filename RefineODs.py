import numpy as np

def refine_ods(od,
               orig_column="d_orisr", dest_column="d_dessr",
               mode_column="d_mode1", time_column="d_hrede"):
    od.columns = list(map(str.lower, od.columns))
    od = od[od["p_mobil"]==1]
    od = od[[orig_column, dest_column, mode_column, time_column]]
    od.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    od = od.astype(float)
    od.fillna(od.mean(), inplace=True)
    od = od.astype(int)
    print("Data Trimmed successfully")
    print("Starting to refine it even further...")
    od = od[od["d_mode1"].isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])]
    origins = list(set(list(od[orig_column])))
    origins.sort()
    destinations = list(set(list(od[dest_column])))
    destinations.sort()
    location_map = {}
    for i, loc in enumerate(origins):
        location_map[loc] = i + 1
    mode_map = {1: "Vehicle", 2: "Vehicle", 3: "Bus", 4: "Subway", 5: "Bus",
                6: "Bus", 7: "Bus",8: "Train", 9: "Bus", 10: "Bus", 11: "Taxi",
                12: "Motorcycle", 13: "Bike", 14: "Walk"}
    refined_od = od[od[time_column]<=2400]
    refined_od.replace({mode_column: mode_map}, inplace=True)
    refined_od.replace({orig_column: location_map}, inplace=True)
    refined_od.replace({dest_column: location_map}, inplace=True)
    refined_od[time_column] = refined_od[time_column] // 100
    print("DONE REFINING")
    return refined_od