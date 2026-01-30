# Gemini Protocol - Project Constitution

## Data Schemas

### Interaction Schema (JSON)
The internal data flow must adhere to this structure:

```json
{
  "input": {
    "requirements_text": "string (User provided requirements)",
    "prompt_template_id": "string (default: 'xray_standard')"
  },
  "output": {
    "test_cases": [
      {
        "summary": "string (Concise title)",
        "preconditions": "string (Setup required)",
        "steps": [
            {
                "action": "string (Step to perform)",
                "data": "string (Input data, optional)",
                "expected_result": "string (Expected outcome)"
            }
        ],
        "priority": "string (Start with 'Medium')"
      }
    ]
  }
}
```

### Xray CSV Export Schema
mapped from `output.test_cases`:
- `Test Summary` <- `summary`
- `Preconditions` <- `preconditions`
- `Action` <- `steps[].action`
- `Data` <- `steps[].data`
- `Expected Result` <- `steps[].expected_result`
- `Priority` <- `priority`

## Behavioral Rules
1.  **Strict JSON Output**: The LLM must output raw JSON matching the `output` schema. No markdown formatting in the raw response if possible, or robust parsing to extract it.
2.  **Reliability First**: If the LLM output is malformed, retry once, then fail gracefully with an error in the UI.
3.  **No Hallucinations**: Do not invent test steps that are not implied by the requirements.

## Architectural Invariants (A.N.T. Architecture)
- **A (Adapter Layer)**: 
    - **Frontend**: HTML5/Vanilla CSS (Dark Mode/Premium). Simple form for input, table for preview, button for CSV download.
    - **Backend**: Flask app serving the static UI and exposing a `/generate` endpoint.
- **N (Nexus Layer)**: 
    - **Ollama Client**: Python wrapper around `ollama` library. Manages model connection and error handling.
- **T (Transformer Layer)**:
    - **PromptEngine**: Loads templates and injects user input.
    - **ResponseParser**: Validates LLM JSON output against the Schema.
