from google.cloud import firestore

db = firestore.Client()

def fetch_all_documents(collection_name):
    docs = db.collection(collection_name).stream()
    return [doc.to_dict() for doc in docs]

def fetch_document(collection_name, document_id):
    doc_ref = db.collection(collection_name).document(document_id).get()
    return doc_ref.to_dict() if doc_ref.exists else None

def get_collection(name):
    return db.collection(name)

# Search documents by a specific field and query
def search_documents(collection_name, field, comparison, value):
    collection_ref = db.collection(collection_name)

    if comparison == "==":
        query = collection_ref.where(field, "==", value)
    elif comparison == "<":
        query = collection_ref.where(field, "<", value)
    elif comparison == ">":
        query = collection_ref.where(field, ">", value)
    else:
        return []

    return [doc.to_dict() for doc in query.stream()]

def fetch_two_documents(collection_name, doc_id1, doc_id2):
    doc1_ref = db.collection(collection_name).document(doc_id1).get()
    doc2_ref = db.collection(collection_name).document(doc_id2).get()
    if doc1_ref.exists and doc2_ref.exists:
        return doc1_ref.to_dict(), doc2_ref.to_dict()
    return None, None
