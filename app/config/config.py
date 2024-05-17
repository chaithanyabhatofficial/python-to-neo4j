import os
from dotenv import load_dotenv

# load .env
load_dotenv()

# File Path
FILE_PATH = os.environ.get("FILE_PATH")

# Neo4j Credentials
NEO4J_URI = os.environ.get('NEO4J_URI')
NEO4J_USER_NAME = os.environ.get("NEO4J_USER_NAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")