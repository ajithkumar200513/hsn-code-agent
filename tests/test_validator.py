import pytest
from agent.validator import HSNValidator
from agent.data_handler import HSNDataHandler
import os

@pytest.fixture
def validator(sample_data):
    handler = HSNDataHandler(sample_data)
    return HSNValidator(handler)

def test_valid_code(validator):
    result = validator.validate('0101')
    assert result['valid'] == True
    assert 'horses' in result['description'].lower()

def test_invalid_code(validator):
    result = validator.validate('9999')
    assert result['valid'] == False
    assert result['reason'] == 'not_found'

def test_hierarchy(validator):
    result = validator.validate('01011010')
    assert result['hierarchy']['2-digit']['exists'] == True
    assert result['hierarchy']['4-digit']['exists'] == True