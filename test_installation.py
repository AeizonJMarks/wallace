# test_installation.py

import sys
import anthropic
import langchain
import spacy
import git
from transformers import pipeline

def test_environment():
    """Test if all required packages are properly installed."""
    results = {
        "Python": sys.version,
        "Anthropic": anthropic.__version__,
        "LangChain": langchain.__version__,
        "spaCy": spacy.__version__,
        "GitPython": git.__version__,
        "Transformers": transformers.__version__
    }
    
    print("\nWallace Development Environment Test")
    print("===================================")
    for component, version in results.items():
        print(f"{component:12} : v{version}")
    
    # Test spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
        print("\nspaCy model loaded successfully")
    except Exception as e:
        print(f"\nError loading spaCy model: {e}")

if __name__ == "__main__":
    test_environment()