import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import pandas as pd
import time
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Retrieve documents from Firestore.")
    parser.add_argument("--path-to-credentials", type=str, default="./.firebase-credentials.json",
                        help="The path to the Firebase credentials. Defaults to ./.firebase-credentials.json.")
    parser.add_argument("--collection", type=str, default="wildfires",
                        help="The collection to add the data to. Defaults to 'wildfires'.")
    args = parser.parse_args()

    # Initialize Firebase app
    cred = credentials.Certificate(args.path_to_credentials)
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    collection = args.collection

    # Reference to the collection
    collection_ref = db.collection('your_collection_name')
    # Get all documents in the collection
    docs = collection_ref.stream()
    # Print document data
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')