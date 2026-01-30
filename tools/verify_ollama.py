import ollama
import sys

def verify_ollama():
    print("Link Phase: Verifying Ollama Connectivity...")
    try:
        # Check if service is reachable
        models = ollama.list()
        print(f"✅ Ollama Service Reachable. Found {len(models['models'])} models.")
        
        # Check specific model
        target_model = "llama3.2"
        # Access .model attribute on the Model objects
        available_models = [m.model for m in models['models']] if isinstance(models, dict) else [m.model for m in models.models]
        
        found = any(target_model in m for m in available_models)
        
        if found:
            print(f"✅ Target model '{target_model}' found.")
            
            # Simple Generation Test
            print(f"Testing generation with '{target_model}'...")
            response = ollama.generate(model=target_model, prompt="Say 'Hello System Pilot' and nothing else.")
            print(f"✅ Model Response: {response['response'].strip()}")
            return True
        else:
            print(f"❌ Target model '{target_model}' NOT found. Please run `ollama pull {target_model}`.")
            return False
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return False

if __name__ == "__main__":
    success = verify_ollama()
    if not success:
        sys.exit(1)
