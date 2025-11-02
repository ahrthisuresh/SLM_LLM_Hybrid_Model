"""Basic tests for the SLM/LLM Hybrid Model project"""
import pytest


def test_imports():
    """Test that required packages can be imported"""
    import streamlit
    import transformers
    import torch
    assert True


def test_requirements_file():
    """Test that requirements.txt exists"""
    from pathlib import Path
    req_file = Path("requirements.txt")
    assert req_file.exists()
    with open(req_file, 'r') as f:
        content = f.read()
        assert 'streamlit' in content.lower()
        assert 'transformers' in content.lower()