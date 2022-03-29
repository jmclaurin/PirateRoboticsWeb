import pandas as pd


def normalize(df):
    return ((df - df.min())/(df.max()-df.min()))

input_path = "sorted_user_resources.csv"
output_path = "normalized_access_data.csv"

df = pd.read_csv(input_path)
df['access_date'] = pd.to_datetime(df['access_date'],format="%Y-%m-%d").astype('int64')

norm_df = normalize(df)
norm_fd.to_csv(output_path)
