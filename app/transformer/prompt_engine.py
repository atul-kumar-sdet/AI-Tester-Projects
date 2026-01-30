class PromptEngine:
    XRAY_TEMPLATE = """
You are an expert QA Engineer. Your task is to generate comprehensive test cases based on the following requirements.

Output strictly in JSON format matching this schema:
{
  "test_cases": [
    {
      "summary": "Concise title of the test case",
      "preconditions": "Any setup required (e.g. 'User is logged in')",
      "steps": [
        {
          "action": "Step action (e.g. 'Click Login')",
          "data": "Input data (e.g. 'user@example.com')",
          "expected_result": "Expected result of this step"
        }
      ],
      "priority": "Medium (default) or High/Low"
    }
  ]
}

Ensure the test cases cover positive, negative, and edge scenarios.
If a test case has multiple steps, include them in the 'steps' array.
Do not include any markdown formatting (like ```json) in the response if possible, just the raw JSON string.

Requirements:
{requirements}
"""

    def __init__(self):
        pass

    def create_prompt(self, requirements: str) -> str:
        """Injects requirements into the Xray template."""
        if not requirements:
            raise ValueError("Requirements text cannot be empty.")
            
        return self.XRAY_TEMPLATE.replace("{requirements}", requirements)
