from adk.api.agent import Agent
from adk.api.types import Request, Response
from .data_handler import HSNDataHandler
from .validator import HSNValidator
from .suggester import HSNSuggester
import logging

class HSNAgent(Agent):
    def __init__(self):
        super().__init__()
        self.data_handler = HSNDataHandler("data/HSN_Master_Data.xlsx")
        self.validator = HSNValidator(self.data_handler)
        self.suggester = HSNSuggester(self.data_handler)
        logging.basicConfig(level=logging.INFO)
        
    def handle_webhook(self, request: Request) -> Response:
        try:
            if 'hsn_codes' in request.query_params:
                return self._handle_validation(request)
            elif 'description' in request.query_params:
                return self._handle_suggestion(request)
            else:
                return Response({"error": "invalid_request", "message": "Please provide either 'hsn_codes' or 'description' parameter"})
        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
            return Response({"error": "processing_error", "message": str(e)})
    
    def _handle_validation(self, request: Request) -> Response:
        codes = request.query_params['hsn_codes'].split(',')
        results = {}
        
        for code in codes:
            code = code.strip()
            validation_result = self.validator.validate(code)
            results[code] = validation_result
            
        return Response({"validation_results": results})
    
    def _handle_suggestion(self, request: Request) -> Response:
        description = request.query_params['description']
        limit = int(request.query_params.get('limit', 5))
        
        suggestions = self.suggester.suggest(description, limit)
        return Response({"suggestions": suggestions})