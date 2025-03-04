import pandas as pd
import numpy as np

# Read the paths of two Excel files
file_path_1 = '2_Normalization_priority.xlsx'
file_path_2 = '1_Calculate_landscape_ESV.xlsx'

# Reading Excel files
data_1 = pd.read_excel(file_path_1)
data_2 = pd.read_excel(file_path_2)

# Define column names (excluding non-numeric columns in the first column)
column_names = data_1.columns[1:]

# Initialize a list to store the result dataframe
result_dataframes = []

# Initialize an ID counter
id_count = 0


def gini(array):
    """Compute the negative Gini coefficient for numpy arrays"""
    array = array.flatten()  # flatten an array
    if np.amin(array) < 0:
        array -= np.amin(array)  # Flatten the array to ensure that the minimum value is zero
    array += 0.0000001  # Avoid dividing by zero
    array = np.sort(array)  # Sorted Arrays
    index = np.arange(1, array.shape[0] + 1)  # Creating an Indexed Array
    n = array.shape[0]  # Number of array elements
    return -((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))  # Negative Gini coefficient formula


# Iterate through each row of data_2 and multiply it by data_1
for idx, row in data_2.iterrows():
    result = data_1.copy()  # Copy data_1 to preserve column names
    result[column_names] = result[column_names].mul(row.values[1:], axis='columns')
    result.insert(0, 'id', id_count)  # Insert the id column
    numeric_cols = result.select_dtypes(include=[np.number]).drop('id', axis=1)
    result['total_MF'] = numeric_cols.sum(axis=1)  # Calculate the total score for each row
    result_dataframes.append(result)
    id_count += 1

# Combine all results into one DataFrame
final_result = pd.concat(result_dataframes, ignore_index=True)

# Calculate the Gini coefficient for each id group
gini_indices = final_result.groupby('id')['total_MF'].apply(lambda x: gini(x.values))

# Add the Gini coefficients to the corresponding first row of each id group
for gid in gini_indices.index:
    final_result.loc[final_result['id'] == gid, 'gini'] = gini_indices[gid]

# Keep Gini coefficients only in the first row of each grouping
final_result['gini'] = final_result.groupby('id')['gini'].transform('first')

# Calculate the average value of total_MF for each id group and store it in a new column community_MF
final_result['community_MF'] = final_result.groupby('id')['total_MF'].transform('mean')

# Calculating MF_differ and gini_differ
id_0_community_MF = final_result[final_result['id'] == 0]['community_MF'].iloc[0]
id_0_gini = final_result[final_result['id'] == 0]['gini'].iloc[0]
final_result['MF_differ'] = (final_result['community_MF'] - id_0_community_MF) / id_0_community_MF
final_result['gini_differ'] = final_result['gini'] - id_0_gini

# Get all total_MF values for group id=0
id_0_total_MF_values = final_result[final_result['id'] == 0]['total_MF'].values

# Calculating change_MF and change_gini
row_count_per_id = len(final_result[final_result['id'] == 0])
final_result['change_MF_percent'] = (final_result['community_MF'] - id_0_community_MF) / id_0_community_MF * 100

# Setting the random seed
np.random.seed(0)
id_0_gini_percent = final_result[final_result['id'] == 0]['gini'].iloc[0]
final_result['change_gini_percent'] = -(final_result['gini'] - id_0_gini) / id_0_gini * 100

# Now that each id group has multiple rows, we select the first row of each id group
reduced_result = final_result.groupby('id').first().reset_index()

# Select the desired column
columns_to_keep = ['id', 'change_MF_percent', 'change_gini_percent']
reduced_result = reduced_result[columns_to_keep]

# Save the simplified results to a new Excel file
output_file_path = 'Customized datasets all information.xlsx'
final_result.to_excel(output_file_path, index=False)
output_file_path_equity = 'Customized datasets MF_EQ_differ percent.xlsx'
reduced_result.to_excel(output_file_path_equity, index=False)

# Display the first few lines of the simplified results
print(reduced_result.head(5))
