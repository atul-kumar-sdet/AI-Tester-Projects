# Technical SOP: Ollama Integration

## Goal
Manage connection to the local Ollama instance and execute generation requests reliably.

## Inputs
- `model_name` (str): e.g., "llama3.2".
- `messages` (list): Chat history or single prompt.
- `options` (dict): Temperature, top_k, etc.

## Logic
1.  **Connection Check**:
    - Before generation, ping `ollama.list()` to ensure service is up.
    - Check if `model_name` exists. If not, raise `ModelNotFoundError`.
2.  **Generation**:
    - Use `ollama.chat` (preferred over generate for better context handling).
    - Set `stream=False` for atomic responses.
    - Set `format='json'` if structured output is requested.
3.  **Error Handling**:
    - Catch `httpx.ConnectError`: execution environment issue.
    - Catch `ollama.ResponseError`: model issue.
    - Wrap all external calls in `try/except` blocks.

## Outputs
- `content` (str): The text content of the response.
- `metadata` (dict): Usage stats (token count, duration).

## Edge Cases
- **Timeout**: If response takes > 60s, consider aborting (or user configurable).
