from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("PMF_API_KEY")
assert key is not None, "PMF_API_KEY not found in environment variables"
print("PMF_API_KEY loaded successfully")