import json
import logging
import pandas as pd
import re

logger = logging.getLogger(__name__)

class ResponseParser:
    def parse_json(self, raw_content: str) -> dict:
        """Parses the raw LLM output into a dictionary."""
        try:
            # Try direct parse
            return json.loads(raw_content)
        except json.JSONDecodeError:
            logger.info("Direct JSON parse failed. Attempting to clean markdown...")
            # Remove ```json and ``` patterns
            cleaned = re.sub(r'```json\s*', '', raw_content)
            cleaned = re.sub(r'```', '', cleaned)
            return json.loads(cleaned.strip())

    def to_dataframe(self, json_data: dict) -> pd.DataFrame:
        """Converts the parsed JSON to a Xray-compatible DataFrame."""
        if "test_cases" not in json_data:
            raise ValueError("JSON output missing 'test_cases' key.")
        
        flat_data = []
        for tc in json_data["test_cases"]:
            summary = tc.get("summary", "")
            preconditions = tc.get("preconditions", "")
            priority = tc.get("priority", "Medium")
            
            steps = tc.get("steps", [])
            if not steps:
                # Handle case with no steps (legacy or simple)
                flat_data.append({
                    "Test Summary": summary,
                    "Preconditions": preconditions,
                    "Action": tc.get("action", ""), # Fallback
                    "Data": "",
                    "Expected Result": tc.get("expected_result", ""), # Fallback
                    "Priority": priority
                })
            else:
                for step in steps:
                    flat_data.append({
                        "Test Summary": summary,
                        "Preconditions": preconditions,
                        "Action": step.get("action", ""),
                        "Data": step.get("data", ""),
                        "Expected Result": step.get("expected_result", ""),
                        "Priority": priority
                    })
        
        df = pd.DataFrame(flat_data)
        
        required_cols = ["Test Summary", "Preconditions", "Action", "Data", "Expected Result", "Priority"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
                
        return df[required_cols]
