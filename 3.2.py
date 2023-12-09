import requests
import numpy as np
from network import Network
#0	Bakerloo
#1	Central
#2	Circle
#3	District
#4	Hammersmith & City
#5	Jubilee
#6	Metropolitan
#7	Northern
#8	Piccadilly
#9	Victoria
#10	Waterloo & City
#11	Docklands Light Railway

def query_line_connectivity(line_id):
    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier={line_id}")
    lines = response.text.strip().split('\n')
    network_data = [list(map(int, line.split(','))) for line in lines]
    return network_data

def station_information(line_id):
    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/stations/query?id={line_id}")
    lines = response.text.strip().split('\n')

    # 将每行数据转换为一个列表，除去第一行
    stations_data = [line.split(',') for line in lines[1:]]  # 使用切片排除第一行
    return stations_data

def query_disruptions(date):
    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/disruptions/query?date={date}")
    if response.status_code != 200:
        raise Exception("Failed to get disruption information")
    return response.json()

def update_matrix_disruption(weight_matrix, disruptions):
    for disruption in disruptions:
        stations = disruption.get('stations')
        delay = disruption.get('delay')  # 表示没有延迟

        if len(stations) == 1:
            # 站点关闭
            station = stations[0]
            weight_matrix[station, :] = 0  # 关闭该站点的所有连接
            weight_matrix[:, station] = 0
        elif len(stations) == 2:
            # 站点间延迟
            station1, station2 = stations
            weight_matrix[station1][station2] *= delay
            weight_matrix[station2][station1] *= delay
    return weight_matrix

stations_data = len(station_information('all'))

n_max = stations_data

weight_matrix = np.zeros((n_max,n_max))
allweight_inf= []

for i in range(12):
    allweight_inf +=  query_line_connectivity(i)

num_sta_weight = len(allweight_inf)

for i in range(num_sta_weight):
    a, b, weight = allweight_inf[i]
    weight_matrix[a][b] = weight
    weight_matrix[b][a] = weight

disruption_date = query_disruptions("2023-09-01")
new_matrix = update_matrix_disruption(weight_matrix, disruption_date)

print("After disruption:", new_matrix[179][190])











