# Import the required libraries
import numpy as np
import pandas as pd

# Read the uploaded file
file_path = '3_Baseline_landscape.xlsx'
land_use_data = pd.read_excel(file_path, header=None)

# Access to land use types and current landscape ratios
land_use_types = land_use_data.iloc[0].tolist()
current_proportions = land_use_data.iloc[1].tolist()

# Convert the current landscape scale to a dictionary
current_proportions_dict = {}
for land_use, proportion in zip(land_use_types, current_proportions):
    current_proportions_dict[land_use] = proportion

# Parameters for defining land use types
land_use_params = {
    'Paddy field': {'type': None, 'fixed': 0.1018},
    'Dry land': {'type': None, 'fixed': 0.2634},
    'Dense woodland': {'grow': 1, 'fixed': None},
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

# Creating an empty DataFrame
result = pd.DataFrame()

# 1. Generation of land class data with fixed parameters
for land_use in land_use_types:
    if land_use_params[land_use]['fixed'] is not None:
        data = np.repeat(land_use_params[land_use]['fixed'], 2000)
        result[land_use] = data

# 2. Generate ground class data with grow=1
for land_use in land_use_types:
    if land_use_params[land_use]['grow'] == 1:
        values = np.linspace(0, 1 - sum(land_use_params[l]['fixed'] for l in land_use_types if land_use_params[l]['fixed'] is not None), 2000)
        result[land_use] = values

# 3. Calculate and add random residuals
remaining_values = 1 - result.sum(axis=1)
grow_zero_types = [land_use for land_use in land_use_types if land_use_params[land_use]['grow'] == 0]

# Generate 2000 different random weights for the entire dataset
random_weights_list = [np.random.dirichlet(np.ones(len(grow_zero_types))) for _ in range(2000)]

# Iterate through each ground class with grow=0 and assign residual values using 200 different random weights for each copy of the entire dataset
for i, land_use in enumerate(grow_zero_types):
    # Assign the residual value using the ith random weight
    allocated_values = [remaining_values[j] * random_weights_list[j][i] for j in range(2000)]

    # Add the assigned values to the resulting DataFrame
    result[land_use] = allocated_values

result = result.round(4)

# Reordering of columns
result = result[list(land_use_params.keys())]

# Merge current landscape scale data
current_proportions_df = pd.DataFrame(current_proportions_dict, index=[0])
result = pd.concat([current_proportions_df, result]).reset_index(drop=True)

# Setting the incremental ID column
result.insert(0, 'ID', range(len(result)))

# Save results to Excel file
result.to_excel('particular sample set.xlsx', index=False)

# Display of selected data
print(result.head())
