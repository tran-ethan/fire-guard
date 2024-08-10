import pandas as pd

df_1 = pd.read_csv("data/2000-2021+2023-2024.csv")

df_1 = df_1.drop(['agency', 'cause', 'response_type'], axis=1)

df_2 = pd.read_csv("data/2022_fires.csv")

for x in df_2.index:
    date = df_2.loc[x, "date"]
    df_2.loc[x, "date"] = df_2.loc[x, "date"].split(" ")[0]

merged_df = pd.concat([df_1, df_2], ignore_index=True)

merged_df.to_csv("data/2000-2024_fires.csv", index=False)

