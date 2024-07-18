# Fire Guard Backend
Data processing part of the Fire Guard web application.

## How to get started

1. Initialize python virtual environment
```bash
python3 -m venv venv
```

2. Activate virtual environment
```bash
source venv/bin/activate # Linux / MacOS
venv\Scripts\activate # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

After installing your own dependencies, update requirements.txt
```bash
pip freeze > requirements.txt
```

## Scripts

### Add to Firestore 
General python script that adds a csv to Firestore.
Specify the path to the csv, the collection name and the path to the firestore credentials file located on your local machine.

Example usage:
```bash
python add_to_firestore.py --path data/wildfires.csv --collection wildfires --path-to-credentials credentials.json
```