import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import pandas as pd
import time
import argparse

LIMIT = 20000 # The limit of documents to write in a single batch operation
DAY = 86400 # The number of seconds in a day
BATCH_SIZE = 500  # Firestore batch size limit

def add_row_to_batch(index: int, row: pd.Series, batch: firestore.WriteBatch, collection: str):
    """
    Add a row to a Firestore batch operation.

    Args:
        index (int): The index of the row to add to the batch operation
        row (pd.Series): The row to add to the batch operation
        batch (firestore.WriteBatch): The Firestore batch operation to add the row to
        collection (str): The collection to add the row to

    Returns:
        None
    """
    try:
        # Create a new document reference in the specified collection
        ref = db.collection(collection).document()
        data = {key: value for key, value in row.items()}

        # If 'date' key is present, convert it to a Firestore timestamp
        if "date" in data:
            data["date"] = pd.to_datetime(data["date"]).to_pydatetime()

        # Set data for the document in the batch operation
        batch.set(ref, data)
        print(f"Row {index} added to batch operation.")

    except Exception as e:
        print(f"Limited batch operation: {e}")
        print("Waiting for a day...")
        time.sleep(DAY)
        return

def add_dataset_to_firestore(dataset: pd.DataFrame, collection: str):
    """
    Add data to Firestore.

    Args:
        dataset (pd.DataFrame): The dataset to add to Firestore
        collection (str): The collection to add the data to

    Returns:
        None
    """

    if (len(dataset) > LIMIT):
        number_of_dfs = len(dataset) // LIMIT
        dfs: list[pd.DataFrame]= np.array_split(dataset, number_of_dfs)
    else:
        dfs: list[pd.DataFrame]= np.array(dataset)

    for df in reversed(dfs):
        batch = db.batch()
        count = 0
        for index, row in df.iterrows():
            if count % BATCH_SIZE == 0:
                batch.commit()
                print("Batch operation committed successfully.")
                batch = db.batch()
                print("New batch operation started.")

            add_row_to_batch(index, row, batch, collection)
            count += 1

        # Commit any remaining writes in the batch
        if count % BATCH_SIZE != 0:
            batch.commit()
            print(f"Final batch of {count % BATCH_SIZE} writes committed.")

    print("All data added to Firestore.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add data to Firestore.")
    parser.add_argument("--path", type=str, default="./data/2000-2021+2023-2024.csv",
                        help="The path to the dataset. Defaults to ./data/2000-2021+2023-2024.csv.")
    parser.add_argument("--path-to-credentials", type=str, default="./.firebase-credentials.json",
                        help="The path to the Firebase credentials. Defaults to ./.firebase-credentials.json.")
    parser.add_argument("--collection", type=str, default="wildfires",
                        help="The collection to add the data to. Defaults to 'wildfires'.")
    
    args = parser.parse_args()

    # Initialize Firebase app
    cred = credentials.Certificate(args.path_to_credentials)
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    dataset = pd.read_csv(args.path)
    collection = args.collection
    
    add_dataset_to_firestore(dataset, collection)
