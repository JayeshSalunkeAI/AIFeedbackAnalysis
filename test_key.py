import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Test 1: Check if variable is set
api_key = os.getenv('PERPLEXITY_API_KEY')
print(f"✅ API Key found: {bool(api_key)}")

if api_key:
    print(f"✅ Key starts with: {api_key[:10]}...")
    print(f"✅ Key length: {len(api_key)}")
else:
    print("❌ API Key NOT found!")

# Test 2: Try to import and check
try:
    from utils.perplexity_client import call_perplexity
    print("✅ utils.perplexity_client imported successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
