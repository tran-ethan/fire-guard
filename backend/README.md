# Fire Guard Backend
Data processing part of the Fire Guard web application.

## How to get started

1. **Install conda**
    [https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html#regular-installation](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html#regular-installation)


2. **Create an environment**
    ```bash
    conda create --name <EnvName>
    ```

3. **Activate your environment**
    ```bash
    conda activate <EnvName>
    ```

4. **Install the ArcGIS API for Python**
    ```bash
    conda install -c esri arcgis
    ```
5. **Install the additional packages**
    ```bash
    pip install firebase_admin
    pip install openmeteo-requests
    ```

**After installing your own dependencies, update requirements.txt**
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