import glob
import pandas as pd

# Function to process files and generate a DataFrame with the specified structure
def process_files(file_paths):
    columns = ['LIN', 'LAS', 'RID', 'eNET', 'RFR']
    row_names = ['mae', 'mae p-value', 'mse', 'mse p-value', 'rmse', 'rmse p value', 'r2', 'r2 p-value', 'mape', 'mape p-value', 'medae', 'medae p-value']

    # Initialize a DataFrame to store the final results
    final_df = pd.DataFrame(index=row_names, columns=columns)

    # Loop through each file and extract the metrics
    for file_path in file_paths:
        # Extract the model name from the file path
        model_name = file_path.split('/')[-2]

        # Read the CSV file
        df = pd.read_csv(file_path, index_col=0)

        # Extract the metrics and p-values
        metrics = df.loc['value'].values
        p_values = df.loc['p-value'].values

        # Combine metrics and p-values into a single list
        combined = [val for pair in zip(metrics, p_values) for val in pair]

        # Add the combined list to the final DataFrame under the appropriate model
        final_df[model_name] = combined

    return final_df

# Define the paths to the CSV files
results_persuasiveness = glob.glob("results/MT/persuasiveness/full/*/metrics.csv")
results_engagement = glob.glob("results/MT/engagement/full/*/metrics.csv")

# Process the files and generate the DataFrames
df_persuasiveness = process_files(results_persuasiveness)
df_engagement = process_files(results_engagement)

# Save the final DataFrames to separate CSV files
df_persuasiveness.to_csv('compiled_metrics_persuasiveness.csv')
df_engagement.to_csv('compiled_metrics_engagement.csv')

# Save the final DataFrames to separate LaTeX files
# df_persuasiveness.style.to_latex('compiled_metrics_persuasiveness.tex')
# df_engagement.style.to_latex('compiled_metrics_engagement.tex')

