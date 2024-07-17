import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Initialize Firebase app
cred = credentials.Certificate("fire-base-key.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client(app)

# Read CSV data into Pandas DataFrame
df = pd.read_csv("./data/2000-2021+2023-2024.csv")

# Reverse the DataFrame and take the last 5 rows
df = df.iloc[-5:].copy()

# Initialize a batch operation
batch = db.batch()

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    # Create a new document reference in the "wildfires" collection
    ref = db.collection("wildfires").document()

    # Set data for the document in the batch operation
    batch.set(ref, {
        "lat": row["lat"],
        "lon": row["lon"],
        "hectares": row["hectares"],
        "agency": row["agency"],
        "date": row["date"],
    })

# Commit the batch operation
batch.commit()

print("Batch operation committed successfully.")
