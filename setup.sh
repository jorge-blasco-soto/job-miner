#!/bin/bash
# Quick setup script for JobMiner

set -e

echo "════════════════════════════════════════════════════════════════"
echo "  JobMiner - Automated Job Scraper Setup"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check Python version
echo "📦 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $PYTHON_VERSION"

# Check if Poetry is installed
echo ""
echo "📦 Checking Poetry installation..."
if ! command -v poetry &> /dev/null; then
    echo "   Poetry not found. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    echo "   ✅ Poetry installed"
else
    echo "   ✅ Poetry found: $(poetry --version)"
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
poetry install
echo "   ✅ Dependencies installed"

# Setup environment
echo ""
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   ✅ Created .env file"
else
    echo "   ℹ️  .env already exists"
fi

# Create data directory
mkdir -p data
echo "   ✅ Created data directory"

# Check Ollama
echo ""
echo "🤖 Checking Ollama (LLM engine)..."
if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama found: $(ollama --version 2>&1 || echo 'installed')"

    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "   ✅ Ollama is running"

        # Check if model is pulled
        if ollama list | grep -q "llama2"; then
            echo "   ✅ llama2 model already available"
        else
            echo "   📥 Pulling llama2 model (this may take a few minutes)..."
            ollama pull llama2
            echo "   ✅ Model downloaded"
        fi
    else
        echo "   ⚠️  Ollama not running. Start it with: ollama serve"
    fi
else
    echo "   ⚠️  Ollama not installed"
    echo ""
    echo "   Install Ollama to enable LLM filtering:"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   macOS: brew install ollama"
    else
        echo "   Linux: curl -fsSL https://ollama.com/install.sh | sh"
    fi
    echo ""
    echo "   Or visit: https://ollama.com"
fi

# Summary
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ Setup Complete!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "  1. If Ollama isn't running, start it:"
echo "     $ ollama serve"
echo ""
echo "  2. Run the job scraper:"
echo "     $ poetry run jobminer"
echo "     or"
echo "     $ make run"
echo ""
echo "  3. Check results:"
echo "     $ cat data/jobs_latest.json"
echo "     or"
echo "     $ make view-latest"
echo ""
echo "  4. For automated GitHub Actions setup:"
echo "     - Create a GitHub repository"
echo "     - Push this code"
echo "     - Enable Actions in repository settings"
echo ""
echo "For more information, see README.md"
echo ""
