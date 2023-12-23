import pytest
import sys
import os

# to import packages from src
# https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure
testdir = os.path.dirname(__file__)
srcdir = "../src"
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import main

def test_token_usage_fee_1():
    token_usage = [255, 347]
    model = "gpt-4"

    result = main.calculate_price(model, token_usage)
    assert result == 2.847


def test_token_usage_fee_2():
    token_usage = [1000, 1000]
    model = "gpt-4"

    result = main.calculate_price(model, token_usage)
    assert result == 9


def test_token_usage_fee_3():
    token_usage = [1000, 1000]
    model = "gpt-3.5-turbo-1106"

    result = main.calculate_price(model, token_usage)
    assert result == 0.3


def test_parse_args_default(monkeypatch):
    # test with no command line arguments
    monkeypatch.setattr('sys.argv', [''])
    assert main.parse_args() == ("gpt-3.5-turbo-1106", "default")


def test_parse_args_gpt3(monkeypatch):
    # Test with --gpt3 argument
    monkeypatch.setattr('sys.argv', ['', '--gpt3'])
    assert main.parse_args() == ("gpt-3.5-turbo-1106", "default")


def test_parse_args_gpt4_32k(monkeypatch):
    # Test with --gpt4-32k argument
    monkeypatch.setattr('sys.argv', ['', '--gpt4-32k'])
    assert main.parse_args() == ("gpt-4-32k", "default")


def test_parse_args_gpt4(monkeypatch):
    # Test with --gpt4-32k argument
    monkeypatch.setattr('sys.argv', ['', '--gpt4'])
    assert main.parse_args() == ("gpt-4", "default")


def test_parse_args_gpt4_followup(monkeypatch):
    # Test with --gpt4-32k argument
    monkeypatch.setattr('sys.argv', ['', '--gpt4', '--follow-up'])
    assert main.parse_args() == ("gpt-4", "follow-up")
    

def test_parse_args_token_count(monkeypatch):
    # Test with --token-count argument
    monkeypatch.setattr('sys.argv', ['', '--token-count'])
    assert main.parse_args() == ("gpt-3.5-turbo-1106", "token-count")