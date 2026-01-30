# Technical SOP: Test Case Generation

## Goal
Generate deterministic, Xray-formatted test cases from user input using a local LLM.

## Inputs
- `requirements_text` (str): Raw user requirements.
- `prompt_template` (str): The specific template to frame the request.

## Logic
1.  **Validation**: Ensure `requirements_text` is not empty.
2.  **Prompt Engineering**: 
    - Load the `xray_standard` template.
    - Inject `requirements_text` into the `{requirements}` placeholder.
    - Append strict JSON formatting instructions.
3.  **LLM Interaction**:
    - Call Ollama `generate` with model `llama3.2`.
    - Set `format='json'` (if supported) or rely on prompt instruction.
4.  **Parsing**:
    - Parse the response string into a JSON object.
    - Validate against `Interaction Schema` (from `gemini.md`).
    - If validation fails, retry once.
5.  **Formatting**:
    - Convert JSON list to Pandas DataFrame.
    - Rename columns to Xray standard (`Test Summary`, `Action`, `Expected Result`, `Priority`).

## Outputs
- `test_cases_df` (pd.DataFrame): Structured data ready for CSV export.
- `raw_json` (dict): For debugging or UI preview.

## Edge Cases
- **Ollama Down**: Return explicit error message "Ollama Service Unreachable".
- **Empty Response**: Return error "Model generated empty response".
- **Malformed JSON**: Return error "Failed to parse model output" after retry.
