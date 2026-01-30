import ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.verify_connection()

    def verify_connection(self) -> bool:
        """Verifies that Ollama is running and the model is available."""
        try:
            models_response = ollama.list()
            # Handle both object and dict response types safely
            if hasattr(models_response, 'models'):
                 available_models = [m.model for m in models_response.models]
            else:
                 available_models = [m['name'] for m in models_response['models']]
                 
            # Flexible matching (e.g. 'llama3.2:latest' matches 'llama3.2')
            if not any(self.model in m for m in available_models):
                logger.warning(f"Model '{self.model}' not found in {available_models}. Please run `ollama pull {self.model}`.")
                # We don't raise error here to allow lazy pulling if implemented later, 
                # but valid for now to warn.
                return False
            
            logger.info(f"Connected to Ollama. Model '{self.model}' is ready.")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            raise ConnectionError(f"Ollama service Unreachable: {e}")

    def generate(self, prompt: str, system_prompt: str = None, json_mode: bool = False) -> str:
        """
        Generates a response from the model.
        
        Args:
            prompt: The user input prompt.
            system_prompt: Optional system instruction.
            json_mode: Whether to force JSON output.
        """
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        
        messages.append({'role': 'user', 'content': prompt})

        options = {}
        # if json_mode:
        #     options['format'] = 'json' 
        # Note: ollama-python uses 'format' arg in chat(), not in options dict usually.
        
        try:
            kwargs = {
                'model': self.model,
                'messages': messages,
                'stream': False
            }
            if json_mode:
                kwargs['format'] = 'json'

            logger.info(f"Sending request to {self.model} (JSON={json_mode})...")
            response = ollama.chat(**kwargs)
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise e
