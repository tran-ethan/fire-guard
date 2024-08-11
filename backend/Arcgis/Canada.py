import pandas as pd

df = pd.read_csv("data/Active_Fires.csv")
df_head = df.head()

df_head = df_head.drop(0)

print(df_head)