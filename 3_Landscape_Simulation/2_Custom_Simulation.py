import numpy as np
import pandas as pd

# Setting random seeds
np.random.seed(0)

# Define constraints on land use types
constraints = {
    'Paddy field': {'min': None, 'max': None, 'fixed': 1018},
    'Dry land': {'min': None, 'max': None, 'fixed': 2634},
    'Dense woodland': {'min': 1254, 'max': 3761, 'fixed': None},
    'Shrubland': {'min': 395, 'max': 1184, 'fixed': None},
    'Sparse woodland': {'min': 699, 'max': 2097, 'fixed': None},
    'Other woodlands': {'min': 64, 'max': 191, 'fixed': None},
    'High covered grassland': {'min': 146, 'max': 437, 'fixed': None},
    'Medium covered grassland': {'min': 345, 'max': 1035, 'fixed': None},
    'Low covered grassland': {'min': 18, 'max': 53, 'fixed': None},
    'Waters': {'min': None, 'max': None, 'fixed': 190},
    'Wetland': {'min': 2, 'max': 8, 'fixed': None},
    'Construction land': {'min': None, 'max': None, 'fixed': 410}
}

# Read uploaded files
file_path = '3_Baseline_landscape.xlsx'
land_use_data = pd.read_excel(file_path, header=None)

# Access to land use types and current landscape ratios
land_use_types = land_use_data.iloc[0].tolist()
current_proportions = land_use_data.iloc[1].tolist()

# Initialize the dataset
num_samples = 6000
data = pd.DataFrame(index=range(num_samples), columns=constraints.keys())

# Assignment of land classes with fixed parameters
for land_type, params in constraints.items():
    if params['fixed'] is not None:
        data[land_type] = params['fixed']

# Generation of areas with range classes
for land_type, params in constraints.items():
    if params['fixed'] is None:
        min_val, max_val = params['min'], params['max']
        data[land_type] = np.random.randint(min_val, max_val + 1, size=num_samples)


# Make sure the sum is 10,000 and adjust
def adjust_totals(dataframe, constraints):
    fixed_sum = dataframe[[lt for lt, params in constraints.items() if params['fixed'] is not None]].sum(axis=1)
    for i in range(num_samples):
        while True:
            total = fixed_sum[i] + dataframe.loc[i, [lt for lt, params in constraints.items() if params['fixed'] is None]].sum()
            if total == 10000:
                break
            else:
                variable_land_types = [lt for lt, params in constraints.items() if params['fixed'] is None]
                adjust_type = np.random.choice(variable_land_types)
                current_value = dataframe.at[i, adjust_type]
                min_val, max_val = constraints[adjust_type]['min'], constraints[adjust_type]['max']
                if total > 10000:
                    dataframe.at[i, adjust_type] = max(min_val, current_value - (total - 10000))
                else:
                    dataframe.at[i, adjust_type] = min(max_val, current_value + (10000 - total))


adjust_totals(data, constraints)

# Convert the current landscape scale to a dictionary and set the ID to 0
current_proportions_dict = {'ID': 0}
for land_use, proportion in zip(land_use_types, current_proportions):
    current_proportions_dict[land_use] = proportion

# Add the current landscape scale to the beginning of the results list
adjusted_results = data.to_dict('records')
adjusted_results.insert(0, current_proportions_dict)

# Convert data to DataFrame, use land use types for column names
results_df = pd.DataFrame(adjusted_results)

# Update the ID column of the DataFrame so that the first row is ID 0 and the rest of the rows are incremented sequentially
results_df['ID'] = list(range(0, len(results_df)))

# Convert to scale by dividing only the generated data by 10000
# Keep the original data read from the file (rows with ID 0)
results_df.iloc[1:, 1:] = results_df.iloc[1:, 1:].div(10000)

# Output results to a new Excel file
output_file = 'Customized datasets.xlsx'
results_df.to_excel(output_file, index=False)

# Display the first few rows of data
print(results_df.head(20))
