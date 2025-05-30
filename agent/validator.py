class HSNValidator:
    def __init__(self, data_handler):
        self.data = data_handler
        
    def validate(self, hsn_code):
        # Format validation
        if not isinstance(hsn_code, str) or not hsn_code.isdigit():
            return {
                "valid": False,
                "reason": "invalid_format",
                "message": "HSN code must be a numeric string"
            }
            
        if len(hsn_code) < 2 or len(hsn_code) > 8:
            return {
                "valid": False,
                "reason": "invalid_length",
                "message": "HSN code must be between 2 and 8 digits"
            }
            
        # Existence validation
        if not self.data.code_exists(hsn_code):
            return {
                "valid": False,
                "reason": "not_found",
                "message": "HSN code not found in master data"
            }
            
        # Hierarchical validation (for codes longer than 2 digits)
        hierarchy = {}
        if len(hsn_code) > 2:
            parent_codes = self._get_parent_codes(hsn_code)
            for level, code in parent_codes.items():
                if not self.data.code_exists(code):
                    hierarchy[level] = {
                        "code": code,
                        "exists": False
                    }
                else:
                    hierarchy[level] = {
                        "code": code,
                        "exists": True,
                        "description": self.data.get_description(code)
                    }
                    
        return {
            "valid": True,
            "description": self.data.get_description(hsn_code),
            "hierarchy": hierarchy if hierarchy else None
        }
        
    def _get_parent_codes(self, hsn_code):
        parents = {}
        code_length = len(hsn_code)
        
        if code_length >= 4:
            parents["2-digit"] = hsn_code[:2]
        if code_length >= 6:
            parents["4-digit"] = hsn_code[:4]
        if code_length == 8:
            parents["6-digit"] = hsn_code[:6]
            
        return parents