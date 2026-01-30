# Findings

## Research
- **Ollama**: Python library `ollama` is the standard way to interact. It supports `chat` and `generate` endpoints.
- **Xray Format**: Jira Xray typically requires a CSV with specific columns:
    - `Test Key` (Optional, for updates)
    - `Test Summary`
    - `Action`
    - `Expected Result`
    - `Priority`
- **Existing Tools**: Most local test generators use simple prompt engineering. We will need a robust prompt template.

## Discoveries
- Need to strictly define the Input/Output JSON schema in `gemini.md` before coding.
- User wants to use `llama3.2`.

## Constraints
- Local execution only.
- Strict adherence to B.L.A.S.T. and A.N.T. protocols.
