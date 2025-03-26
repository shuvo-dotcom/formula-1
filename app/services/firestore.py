from google.cloud import firestore

db = firestore.Client()

def get_collection(name):
    return db.collection(name)
