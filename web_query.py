import requests
import numpy as np
from londontube.network import Network
from datetime import datetime
from urllib.parse import quote

def query_line_connectivity(line_id):

    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier={line_id}")
    lines = response.text.strip().split('\n')
    network_data = [list(map(int, line.split(','))) for line in lines]
    return network_data