import pytest
from unittest.mock import patch
from journey_planner import main
#from ..londontube.journey_planner import main #import from the correct place in directory
from web_query import query_line_connectivity, station_information, update_matrix_disruption
#from ..londontube.web_query import journey_planner

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

#testing that functions in journey_planner raise an appropriate exception when query unsuccessful (status_code!=200)
def test_journey_planner_query_failure():
    #testing the query_line_connectivity function
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        with pytest.raises(Exception, match="Failed to get line connectivity information"):
            query_line_connectivity(0)

    #testing the station_information function
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        with pytest.raises(Exception, match="Failed to get station information"):
            station_information(0)

    #testing the update_matrix_disruption function
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        with pytest.raises(Exception, match="Failed to get disruption information"):
            update_matrix_disruption([[0, 1], [1, 0]], date="01-01-2000")

#testing that appropriate error thrown when information requested about station/list that doesn't exist

#testing that appropriate error raised if user tries to fetch disruptions on a day that is too far in the future or past