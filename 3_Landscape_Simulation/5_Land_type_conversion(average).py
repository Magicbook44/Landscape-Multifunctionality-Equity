import numpy as np
import pandas as pd


file_path = '3_Baseline_landscape.xlsx'
land_use_data = pd.read_excel(file_path, header=None)


land_use_types = land_use_data.iloc[0].tolist()
current_proportions = land_use_data.iloc[1].tolist()


current_proportions_dict = {}
for land_use, proportion in zip(land_use_types, current_proportions):
    current_proportions_dict[land_use] = proportion

land_use_params = {
    'Paddy field': {'type': None, 'fixed': 0.1018},
    'Dry land': {'type': None, 'fixed': 0.2634},
    'Dense woodland': {'grow': None, 'fixed': 0.2507},
    'Shrubland': {'grow': 0, 'fixed': None},
    'Sparse woodland': {'grow': 0, 'fixed': None},
    'Other woodlands': {'grow': 0, 'fixed': None},
    'High covered grassland': {'grow': None, 'fixed': 0.0291},
    'Medium covered grassland': {'grow': None, 'fixed': 0.069},
    'Low covered grassland': {'grow': None, 'fixed': 0.0035},
    'Waters': {'type': None, 'fixed': 0.019},
    'Wetland': {'type': None, 'fixed': 0.0005},
    'Construction land': {'type': None, 'fixed': 0.0410}
}


result = pd.DataFrame()


for land_use in land_use_types:
    if land_use_params[land_use]['fixed'] is not None:
        data = np.repeat(land_use_params[land_use]['fixed'], 2000)
        result[land_use] = data


for land_use in land_use_types:
    if land_use_params[land_use]['grow'] == 1:
        values = np.linspace(0, 1 - sum(land_use_params[l]['fixed'] for l in land_use_types if land_use_params[l]['fixed'] is not None), 2000)
        result[land_use] = values


remaining_values = 1 - result.sum(axis=1)
grow_zero_types = [land_use for land_use in land_use_types if land_use_params[land_use]['grow'] == 0]

# Even distribution of residual values
for i, land_use in enumerate(grow_zero_types):

    allocated_values = remaining_values / len(grow_zero_types)


    result[land_use] = allocated_values

result = result.round(4)


result = result[list(land_use_params.keys())]


current_proportions_df = pd.DataFrame(current_proportions_dict, index=[0])
result = pd.concat([current_proportions_df, result]).reset_index(drop=True)


result.insert(0, 'ID', range(len(result)))


result.to_excel('particular sample set.xlsx', index=False)


print(result.head())
