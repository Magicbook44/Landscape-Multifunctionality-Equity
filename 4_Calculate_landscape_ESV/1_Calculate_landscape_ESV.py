import pandas as pd

file_path_1_new = 'Customized datasets.xlsx'
file_path_2_new = '1_ES_equivalent_table.xlsx'


data_1_new = pd.read_excel(file_path_1_new)
data_2_new = pd.read_excel(file_path_2_new)

# Get the transpose of the second to last row of the first column of the table of value equivalents as a column name
value_names = data_2_new.iloc[0:, 0].values

# Delete first column (row and column keys)
data_1_calc_new = data_1_new.iloc[:, 1:]
data_2_calc_new = data_2_new.iloc[:, 1:]

# Initialize a DataFrame to store the results, with column names transposed from the second to the last row of the first column of the value equivalent table
result_df = pd.DataFrame(columns=value_names)

# Iterate through each row of table 1
for i in range(len(data_1_calc_new.index)):
    row_values = data_1_calc_new.iloc[i].values
    result_row = []

    # Iterate through each row of table 2
    for j in range(len(data_2_calc_new.index)):
        result_sum = (row_values * data_2_calc_new.iloc[j].values).sum()
        result_row.append(result_sum)

    # Assign the result to the corresponding column
    result_df.loc[i] = result_row

# Add the ID column, using the first column of data from Table 1
result_df.insert(0, 'ID', data_1_new.iloc[:, 0])

# Save the calculation result DataFrame directly
output_excel_path = '1_Calculate_landscape_ESV.xlsx'
result_df.to_excel(output_excel_path, index=False)

