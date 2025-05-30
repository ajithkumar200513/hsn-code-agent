import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class HSNDataHandler:
    def __init__(self, excel_path):
        self.df = pd.read_excel(excel_path)
        self._preprocess_data()
        self._build_indexes()
        
    def _preprocess_data(self):
        # Clean data
        self.df['HSNCode'] = self.df['HSNCode'].astype(str).str.strip()
        self.df['Description'] = self.df['Description'].astype(str).str.strip().str.lower()
        
    def _build_indexes(self):
        # Code to description mapping
        self.code_to_desc = dict(zip(self.df['HSNCode'], self.df['Description']))
        
        # Setup TF-IDF for suggestions
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Description'])
        
    def get_description(self, hsn_code):
        return self.code_to_desc.get(hsn_code, None)
    
    def code_exists(self, hsn_code):
        return hsn_code in self.code_to_desc
    
    def get_similar_descriptions(self, query, limit=5):
        query_vec = self.vectorizer.transform([query.lower()])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Get top matches
        top_indices = np.argsort(similarities)[-limit:][::-1]
        results = []
        
        for idx in top_indices:
            if similarities[idx] > 0:  # Only return matches with some similarity
                results.append({
                    'hsn_code': self.df.iloc[idx]['HSNCode'],
                    'description': self.df.iloc[idx]['Description'],
                    'score': float(similarities[idx])
                })
                
        return results