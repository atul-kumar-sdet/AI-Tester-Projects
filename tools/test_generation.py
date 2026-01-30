import sys
import os

# Create a file to treat the root as a package if needed, or adjust path
sys.path.append(os.getcwd())

from app.nexus.ollama_client import OllamaClient
from app.transformer.prompt_engine import PromptEngine
from app.transformer.response_parser import ResponseParser

def main():
    print("Testing Generation Flow...")
    
    # 1. Setup
    client = OllamaClient(model="llama3.2")
    engine = PromptEngine()
    parser = ResponseParser()
    
    # 2. Input
    requirements = "Login page: User should be able to login with valid email and password. Show error if password is less than 6 chars."
    print(f"Input: {requirements}")
    
    # 3. Prompt
    prompt = engine.create_prompt(requirements)
    # print(f"Generated Prompt: {prompt[:100]}...")
    
    # 4. Generate
    print("Sending to Ollama...")
    try:
        # Note: Using json_mode=True if supported by prompt instruction is good, 
        # but let's rely on prompt instruction strictly first as Llama3.2 is good at it.
        raw_response = client.generate(prompt, json_mode=True)
        print("Received Response.")
        
        # 5. Parse
        print("Parsing...")
        json_data = parser.parse_json(raw_response)
        df = parser.to_dataframe(json_data)
        
        print("\n✅ Verification Successful!")
        print(df.to_string())
        
        # Save sample
        df.to_csv("tools/sample_output.csv", index=False)
        print("\nSaved to tools/sample_output.csv")
        
    except Exception as e:
        print(f"\n❌ Verification Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
