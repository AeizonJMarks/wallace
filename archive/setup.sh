# Wallace Development Environment Setup

# 1. Create and activate a virtual environment
python -m venv wallace-env
source wallace-env/bin/activate  # On Windows: wallace-env\Scripts\activate

# 2. Install core dependencies
pip install --upgrade pip
pip install anthropic       # Anthropic API
pip install langchain      # LLM integration framework
pip install spacy         # NLP toolkit
python -m spacy download en_core_web_sm  # Download English model
pip install transformers  # Hugging Face transformers
pip install GitPython     # Git integration

# 3. Install development tools
pip install pytest        # Testing
pip install black        # Code formatting
pip install mypy         # Type checking
pip install pylint      # Linting

# Create requirements.txt
pip freeze > requirements.txt

# Basic directory structure
mkdir -p wallace/{core,ai,git,tests}
touch wallace/__init__.py

# Optional: Install Anthropic CLI (if available)
# Note: Check Anthropic's website for current CLI installation instructions
# as these may change with updates

# Test installations
python -c "import anthropic; print(f'Anthropic: {anthropic.__version__}')"
python -c "import langchain; print(f'LangChain: {langchain.__version__}')"
python -c "import spacy; print(f'spaCy: {spacy.__version__}')"
