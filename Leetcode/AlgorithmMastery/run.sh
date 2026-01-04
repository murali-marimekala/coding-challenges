#!/bin/bash

# Algorithm Mastery Platform - Single Command Runner
# Usage: ./run.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}🎯 Algorithm Mastery Platform${NC}"
echo -e "${BLUE}================================${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python3 found${NC}"

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing required dependencies...${NC}"
    python3 -m pip install -q streamlit plotly pandas pyyaml
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${YELLOW}⚠️  app.py not found in current directory${NC}"
    echo -e "${YELLOW}Please run this script from the AlgorithmMastery directory${NC}"
    exit 1
fi

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}🚀 Starting application...${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo -e "Opening at: ${YELLOW}http://localhost:8501${NC}"
echo -e "Press ${YELLOW}Ctrl+C${NC} to stop"
echo ""

# Run the streamlit app
python3 -m streamlit run app.py
