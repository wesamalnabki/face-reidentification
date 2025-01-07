from dotenv import load_dotenv, find_dotenv

# Load environment variables
print("Loading env variables --> ", load_dotenv(find_dotenv(usecwd=True)))

PACKAGE_VERSION = "1.0.0"
