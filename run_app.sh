#!/bin/bash
# Script to run Streamlit app with the correct virtual environment

cd "$(dirname "$0")"
source venv/bin/activate
streamlit run app.py
