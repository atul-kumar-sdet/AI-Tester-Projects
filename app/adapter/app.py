from flask import Flask, render_template, request, jsonify, Response, send_file
import sys
import os
import logging
import pandas as pd
import io

# Ensure app modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.nexus.ollama_client import OllamaClient
from app.transformer.prompt_engine import PromptEngine
from app.transformer.response_parser import ResponseParser

app = Flask(__name__, template_folder='static', static_folder='static')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
nexus = OllamaClient(model="llama3.2")
transformer_engine = PromptEngine()
transformer_parser = ResponseParser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        requirements = data.get('requirements')
        
        if not requirements:
            return jsonify({'error': 'Requirements are required'}), 400

        # Phase 1: Transform Input
        prompt = transformer_engine.create_prompt(requirements)
        
        # Phase 2: Nexus Interaction
        logger.info("Sending prompt to Ollama...")
        # We don't use stream here for simplicity in MVP, but could be added
        raw_response = nexus.generate(prompt, json_mode=True)
        
        # Phase 3: Transform Output
        json_data = transformer_parser.parse_json(raw_response)
        
        # Return structured JSON for UI Preview
        return jsonify(json_data)

    except Exception as e:
        logger.error(f"Error during generation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.json
        # Expecting the JSON list of test cases directly from frontend state
        test_cases_json = data.get('test_cases')
        
        if not test_cases_json:
             return jsonify({'error': 'No test cases provided'}), 400
             
        # Mocking the wrapper dict expected by parser
        wrapper = {"test_cases": test_cases_json}
        
        df = transformer_parser.to_dataframe(wrapper)
        
        # Convert to CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=test_cases_xray.csv"}
        )

    except Exception as e:
        logger.error(f"Error during download: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
