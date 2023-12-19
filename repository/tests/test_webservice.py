import pytest
import importlib
from unittest.mock import patch, Mock
#journey_planner = importlib.import_module("journey-planner")
from ..londontube.journey_planner import main, get_station_name
#journey_planner = importlib.import_module("..londontube.journey-planner")
#from web_query import query_line_connectivity, station_information, update_matrix_disruption
from ..londontube.web_query import query_line_connectivity, station_information, update_matrix_disruption

#1. positive tests of the functions in journey_planner and web_query:

#testing that query_line_connectivity unpacks webservice data as expected by mocking requests.get()
def test_query_line_connectivity():
    with patch('requests.get') as mock_get:
        #setting up the mock webservice response
        mock_response = Mock()
        mock_response.text = "1,2,10\n2,3,15\n3,4,12\n"
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        network_data = query_line_connectivity("mock_line_id")
        #assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with("https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier=mock_line_id")

        assert network_data == [
            [1, 2, 10],
            [2, 3, 15],
            [3, 4, 12]
        ]
        
#testing that station_information unpacks webservice data as expected by mocking requests.get()
def test_station_information():
    with patch('requests.get') as mock_get:
        #setting up the mock webservice response
        mock_response = Mock()
        mock_response.text = "station index,station name,latitude,longitude\n1,Station A,51.123,-0.456\n2,Station B,51.234,-0.567\n"
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        stations_data = station_information(line_id="mock_line_id")
        #assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with("https://rse-with-python.arc.ucl.ac.uk/londontube-service/stations/query?id=mock_line_id")

        assert stations_data == [
            ["1", "Station A", "51.123", "-0.456"],
            ["2", "Station B", "51.234", "-0.567"]
        ]

#testing update_matrix_disruption unpacks webservice data as expected by mocking requests.get()
def test_update_matrix_disruption():
    with patch('requests.get') as mock_get:
        #setting up the mock webservice response
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "line": 7,
                "stations": [0, 1],
                "delay": 2
            },
            {
                "stations": [2],
                "delay": 0
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        mock_weight_matrix = [[1, 1, 1], 
                              [1, 1, 1],
                              [1, 1, 1]]
        updated_matrix = update_matrix_disruption(weight_matrix=mock_weight_matrix, date="mock_date")
        #assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with("https://rse-with-python.arc.ucl.ac.uk/londontube-service/disruptions/query?date=mock_date")

        assert updated_matrix == [[1, 2, 0], 
                                  [2, 1, 0],
                                  [0, 0, 0]]

#testing get_station_name gives the expected output by mocking station_information
def test_get_station_name():
    with patch('web_query.station_information') as mock_station_information:
        mock_station_information.return_value = [["1", "Station A", "51.123", "-0.456"], ["2", "Station B", "51.234", "-0.567"]]

        name = get_station_name(1)
        assert name == "Station A"

#2. negative tests of the CLI:

#testing that appropriate errors raised when inputted date format is incorrect
def test_wrong_date_formats():
    #the case of supplying MM-DD-YYYY instead
    with pytest.raises(ValueError, match="Date must be of the format YYYY-MM-DD"):
        with patch('sys.argv', ['journey_planner.py', '0', '1', '01-01-2000']):
            main()
    #the case of supplying YY-MM-DD instead
    with pytest.raises(ValueError, match="Date must be of the format YYYY-MM-DD"):
        with patch('sys.argv', ['journey_planner.py', '0', '1', '23-01-01']):
           main()

#testing that appropriate error raised if user tries to fetch disruptions on a day that is too far in the future or past
def test_wrong_date_range():
    #the case of the date being too far in the past
    with pytest.raises(ValueError, match="Date must be between 2023-01-01 and 2024-12-31 inclusive"):
        with patch('sys.argv', ['journey_planner.py', '0', '1', '2010-01-01']):
            main()
    #the case of the date being too far in the future
    with pytest.raises(ValueError, match="Date must be between 2023-01-01 and 2024-12-31 inclusive"):
        with patch('sys.argv', ['journey_planner.py', '0', '1', '2030-01-01']):
            main()

#testing that appropriate error thrown when information requested about station that doesn't exist
def test_nonexistent_station():
    #the case of start ID being too large
    with pytest.raises(ValueError, match="Station ID must be between 0 and 295 inclusive"):
        with patch('sys.argv', ['journey_planner.py', '300', '1', '2023-01-01']):
            main()
    #the case of destination ID being too large
    with pytest.raises(ValueError, match="Station ID must be between 0 and 295 inclusive"):
        with patch('sys.argv', ['journey_planner.py', '1', '300', '2023-01-01']):
            main()
    #the case of start ID being too small
    with pytest.raises(ValueError, match="Station ID must be between 0 and 295 inclusive"):
        with patch('sys.argv', ['journey_planner.py', '-5', '1', '2023-01-01']):
            main()
    #the case of destination ID being too small
    with pytest.raises(ValueError, match="Station ID must be between 0 and 295 inclusive"):
        with patch('sys.argv', ['journey_planner.py', '1', '-5', '2023-01-01']):
            main()

#3. negative tests of API functions:

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

#testing that functions in journey_planner raise appropriate error when information requested about line that doesn't exist
def test_nonexistent_line():
    with pytest.raises(ValueError, match="Line ID must be between 0 and 11 inclusive"):
        query_line_connectivity(-1)
    with pytest.raises(ValueError, match="Line ID must be between 0 and 11 inclusive"):
        query_line_connectivity(12)
    with pytest.raises(ValueError, match="Line ID must be between 0 and 11 inclusive"):
        station_information(-1)
    with pytest.raises(ValueError, match="Line ID must be between 0 and 11 inclusive"):
        station_information(12)
