import pytest
from unittest.mock import patch
from journey_planner import main
#from ..londontube.journey_planner import main #import from the correct place in directory

#negative tests of the CLI:

#testing that appropriate errors raised when inputted date format is incorrect
def test_wrong_date_formats():
    #the case of the entire date being too long
    with pytest.raises(ValueError, match="Date must be of the format YYYY-MM-DD"):
        with patch('sys.argv', ['journey_planner.py', '0', '1', '20000-01-01']):
            main()
    #the case of supplying MM-DD-YYYY instead
    with pytest.raises(ValueError, match="Date must be of the format YYYY-MM-DD"):
        with patch('sys.argv', ['journey_planner.py', '0', '1', '01-01-2000']):
            main()

#negative tests of the API:

