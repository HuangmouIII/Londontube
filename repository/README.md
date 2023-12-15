# Londontube

Londontube is a Python package for navigating the London Tube network. # comlete the function of the package!!

## Installation

Install Londontube using pip:

```bash
git clone <SSH>
# where <SSH> can be find in the GitHub repository: https://github.com/UCL-COMP0233-23-24/londontube-Working-Group-07 
cd repository
pip install .
```

## Usage

Invoke the tool with `greet <FirstName> <Secondname>` or use it on your own library:

```python
from londontube.network import Network
from londontube.web_query import query_line_connectivity
# All stations for the special line
from londontube.web_query import station_information
# Station information
from londontube.web_query import update_matrix_disruption
# Update matrix information for disruption
```

## A quick start example

from londontube.network import Network
network = Network()
network.plot('Waterloo', 'Baker Street')

For more detailed documentation, please refer to the docs directory.

## How to Cite Londontube

If you use Londontube in your research, please cite it as follows:

Group7 (2023). londontube: A Python package for navigating the London Tube network. Version 1.0.0. URL: https://github.com/UCL-COMP0233-23-24/londontube-Working-Group-07
