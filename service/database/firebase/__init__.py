import os
import firebase_admin
from firebase_admin import credentials,firestore

# Get the path to the root directory (one level above the current file's directory)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
json_path = os.path.join(root_dir, 'serviceAccountKey.json')

cred = credentials.Certificate(json_path)
app = firebase_admin.initialize_app(cred)
print(app.name)

db = firestore.client()