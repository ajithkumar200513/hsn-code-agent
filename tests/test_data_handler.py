import pytest
import pandas as pd
from agent.data_handler import HSNDataHandler
import os

@pytest.fixture
def sample_data(tmp_path):
    data = {
        'HSNCode': ['01', '0101', '010110', '01011010', '85', '8501'],
        'Description': [
            'Live animals',
            'Live horses, asses, mules and hinnies',
            'Pure-bred breeding horses',
            'Thoroughbred horses',
            'Electrical machinery',
            'Electric motors and generators'
        ]
    }
    df = pd.DataFrame(data)
    test_file = tmp_path / "test_hsn.xlsx"
    df.to_excel(test_file, index=False)
    return str(test_file)

def test_data_loading(sample_data):
    handler = HSNDataHandler(sample_data)
    assert len(handler.code_to_desc) == 6
    assert handler.get_description('01') == 'live animals'

def test_suggestion(sample_data):
    handler = HSNDataHandler(sample_data)
    results = handler.get_similar_descriptions('horses', 2)
    assert len(results) == 2
    assert 'horses' in results[0]['description'].lower()