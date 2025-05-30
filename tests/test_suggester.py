import pytest
from agent.suggester import HSNSuggester
from agent.data_handler import HSNDataHandler

@pytest.fixture
def suggester(sample_data):
    handler = HSNDataHandler(sample_data)
    return HSNSuggester(handler)

def test_suggestion(suggester):
    results = suggester.suggest('horses', 2)
    assert len(results) == 2
    assert results[0]['score'] > 0