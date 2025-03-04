import numpy as np
import pandas as pd

num_data_sets = 6000

# Read the uploaded file
file_path = '3_Baseline_landscape.xlsx'
land_use_data = pd.read_excel(file_path, header=None)

# Access to land use types and current landscape ratios
land_use_types = land_use_data.iloc[0].tolist()
current_proportions = land_use_data.iloc[1].tolist()

# Convert current landscape scale to dictionary
current_proportions_dict = {}
for land_use, proportion in zip(land_use_types, current_proportions):
    current_proportions_dict[land_use] = proportion

# New land use parameters
land_use_params = {
    'Paddy field': {'type': None, 'fixed': 0.1018},
    'Dry land': {'type': None, 'fixed': 0.2634},
    'Dense woodland': {'type': 1, 'fixed': None},
    'Shrubland': {'type': 1, 'fixed': None},
    'Sparse woodland': {'type': 1, 'fixed': None},
    'Other woodlands': {'type': 1, 'fixed': None},
    'High covered grassland': {'type': 0, 'fixed': None},
    'Medium covered grassland': {'type': 0, 'fixed': None},
    'Low covered grassland': {'type': 0, 'fixed': None},
    'Waters': {'type': None, 'fixed': 0.019},
    'Wetland': {'type': None, 'fixed': 0.0005},
    'Construction land': {'type': None, 'fixed': 0.0410}
}

# Creating an empty DataFrame
result = pd.DataFrame()

# 1. Generation of land-use data with fixed parameters
for land_use in land_use_types:
    if land_use_params[land_use]['fixed'] is not None:
        data = np.repeat(land_use_params[land_use]['fixed'], num_data_sets)
        result[land_use] = data

# 2. Calculation of the total value of 'woodlands' and 'grasslands'
total_fixed_values = sum(params['fixed'] for params in land_use_params.values() if params['fixed'] is not None)
land_use_values = 1 - total_fixed_values

# The value of 'woodlands' increases from 0 to the proportion of remaining
result['woodlands'] = np.linspace(0, land_use_values, num_data_sets)

# 3. Calculate the total value of 'grasslands'
# 'The value of 'grasslands' is 1 minus all fixed values and the value of 'woodlands'
result['grasslands'] = 1 - result.sum(axis=1)

# 4. Random assignment of 'woodlands' and 'grasslands' values
forest_types = [land_use for land_use in land_use_types if land_use_params[land_use]['type'] == 1]
grass_types = [land_use for land_use in land_use_types if land_use_params[land_use]['type'] == 0]

# Generate different random weights for the whole dataset
random_forest_weights = [np.random.dirichlet(np.ones(len(forest_types))) for _ in range(num_data_sets)]
random_grass_weights = [np.random.dirichlet(np.ones(len(grass_types))) for _ in range(num_data_sets)]

# Iterate through each type=1 land class, assigning a value of 'woodlands' to each copy of the entire dataset using different random weights
for i, land_use in enumerate(forest_types):
    # Assigning the value of 'woodlands' using the ith randomized weight
    allocated_values = [result['woodlands'][j] * random_forest_weights[j][i] for j in range(num_data_sets)]
    result[land_use] = allocated_values

# Iterate through each type=0 land class, assigning a value of 'grass' to each copy of the entire dataset using different random weights
for i, land_use in enumerate(grass_types):
    # Assigning the value of 'grass' using the ith randomized weight
    allocated_values = [result['grasslands'][j] * random_grass_weights[j][i] for j in range(num_data_sets)]
    result[land_use] = allocated_values

result = result.round(4)

# Reordering of columns
result = result[list(land_use_params.keys()) + ['woodlands', 'grasslands']]

# Merge current landscape scale data
current_proportions_df = pd.DataFrame(current_proportions_dict, index=[0])
result = pd.concat([current_proportions_df, result]).reset_index(drop=True)

# Setting the incremental ID column
result.insert(0, 'ID', range(len(result)))

# Save results to Excel file
result.to_excel('particular sample set.xlsx', index=False)

# Display of selected data
print(result.head())
