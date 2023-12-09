import pytest
import sys
import os

# to import packages from src
# https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure
testdir = os.path.dirname(__file__)
srcdir = "../src"
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import main

def test_token_usage_fee():
    token_usage = [1000, 1000]
    model = "gpt-4"

    result = main.calculate_price(model, token_usage)
    assert result == 9
