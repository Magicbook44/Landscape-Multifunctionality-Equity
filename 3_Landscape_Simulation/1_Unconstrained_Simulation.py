# Importing numpy and pandas libraries
import numpy as np
import pandas as pd

# List of defined land use types
land_use_types = [
    'Paddy field', 'Dry land', 'Dense woodland', 'Shrubland', 'Sparse woodland',
    'Other woodlands', 'High covered grassland', 'Medium covered grassland', 'Low covered grassland',
    'Waters', 'Wetland', 'Construction land'
]


# Define a function to generate random data
def generate_random_data(num_datasets, num_samples_per_class, current_proportions, random_seed=None):
    data = []  # Initialize an empty list to store the dataset

    # If a random seed is provided, set the random seed to ensure reproducible results
    if random_seed is not None:
        np.random.seed(random_seed)

    # Loop to create a specified number of datasets
    for i in range(num_datasets):
        # Create an empty DataFrame with columns named 'ID' and all land use types
        dataset = pd.DataFrame(columns=['ID'] + land_use_types)

        # Select the land use type corresponding to the current dataset
        land_use = land_use_types[i % len(land_use_types)]
        # Generation of randomized scale data for selected land use types
        dataset[land_use] = np.random.uniform(0, 1, num_samples_per_class)

        # Generate randomized scale data for other land use types
        remaining_land_use_types = [l for l in land_use_types if l != land_use]
        for remaining_land_use in remaining_land_use_types:
            dataset[remaining_land_use] = np.random.uniform(0, 1, num_samples_per_class) / len(remaining_land_use_types)

        # Assign a unique ID to each sample
        dataset['ID'] = range(1, num_samples_per_class + 1)
        # Proportion of selected land-use types ranked
        dataset[land_use] = dataset[land_use].sort_values().values
        # Add the current dataset to the data list
        data.append(dataset)

    # Merge all sub-datasets into one large dataset
    result = pd.concat(data, ignore_index=True)
    # Rounding results to four decimal places
    result = result.round(4)

    # Add the current scale data to the first line of the result
    result.loc[0] = [0] + current_proportions
    # Reordering the ID column
    result['ID'] = range(len(result))
    # Returns the final result
    return result


# Specify the file path
file_path = '3_Baseline_landscape.xlsx'
# Reading Excel files without table headers
land_use_data = pd.read_excel(file_path, header=None)

# Obtaining land use types and current landscape proportions from reads
current_proportions = land_use_data.iloc[1].tolist()

# Setting the parameters for generating a dataset
num_datasets = 12  # Number of data sets
num_samples_per_class = 2000  # Sample size per category
random_seed = 0  # random seed

# Calling a function to generate data
result = generate_random_data(num_datasets, num_samples_per_class, current_proportions, random_seed=random_seed)

# Save the generated data to an Excel file
result.to_excel('Unconstrained data sets.xlsx', index=False)
