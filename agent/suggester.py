class HSNSuggester:
    def __init__(self, data_handler):
        self.data = data_handler
        
    def suggest(self, description, limit=5):
        if not description or not isinstance(description, str):
            return []
            
        return self.data.get_similar_descriptions(description, limit)