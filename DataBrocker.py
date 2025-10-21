import firebase_admin
from firebase_admin import firestore

class DataBrocker:
    def __init__(self):

        # Application Default credentials are automatically created.
        self.app = firebase_admin.initialize_app()
        self.db = firestore.client()
        
        '''# Reference a collection
            collection_ref = db.collection("gps_data")

            # Create a document with a specific ID
            doc_ref = collection_ref.document("device_001")

            # Set data in the document
            doc_ref.set({
                "lat": 39.7386,
                "lon": -105.0004,
                "timestamp": "2025-10-20T20:48:07"
            })'''
            
            
            
        '''Possible Structure 
            collection-date
                -> document-date_time 1000 gps hits
                    -> list of json data points
                -> document-date_time 1000 gps hits'''
        
    def upload_backend(self,current_date,json_data_entry):
        master_collection_ref = db.collection('date_gps_data')
        
        current_date_collection = master_collection_ref.collection(current_date)
        
        latest_doc_query = current_date_collection.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1)
        docs = latest_doc_query.stream()
        
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            num_fields = len(data)
            print(f"Document has {num_fields} fields")
        else:
            print("Document does not exist")
        
        
            
            