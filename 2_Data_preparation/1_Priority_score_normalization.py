# Normalized using the total score given for each group
import pandas as pd

# Reading Excel files
df = pd.read_excel('1_ES_equivalent_table.xlsx', index_col=0)

# Keep the original row and column keys, but exclude them from the calculation
df_numeric_only = df.select_dtypes(include='number')

# Normalize numeric data using totals per row
row_sums_numeric = df_numeric_only.sum(axis=1)
df_row_normalized_numeric = df_numeric_only.div(row_sums_numeric, axis=0)

# Calculate the average of each column and add it as a new row
df_row_normalized_numeric.loc['mean'] = df_row_normalized_numeric.mean()

# 将The normalized numeric data is merged back into the original data frame, keeping the original row and column keys
df_with_keys = df[df.columns.difference(df_numeric_only.columns)].join(df_row_normalized_numeric)
output_excel_path = '2_Normalization_priority.xlsx'

# Save final_df as Excel file
df_row_normalized_numeric.to_excel(output_excel_path, index=True)



