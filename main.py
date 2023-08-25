import requests
import folium


with open("api-key.txt", "r") as file:
    api_key = file.readline().strip()
base_url = 'https://api.openrouteservice.org/v2/'

coords = [
    [-87.7898356, 41.8879452],
    [-87.7808524, 41.8906422],
    [-87.7895149, 41.8933762],
    [-87.7552925, 41.8809087],
    [-87.7728134, 41.8804058],
    [-87.7702890, 41.8802231],
    [-87.7787924, 41.8944518],
    [-87.7732345, 41.8770663],
]
vehicle_start = [-87.800701, 41.876214]
m = folium.Map(location=list(reversed([-87.787984, 41.8871616])), tiles="cartodbpositron", zoom_start=14)

for coord in coords:
    folium.Marker(location=list(reversed(coord))).add_to(m)

folium.Marker(location=list(reversed(vehicle_start)), icon=folium.Icon(color="red")).add_to(m)

# Configuração dos veículos
vehicles = [
    {
        "id": 0,
        "start": vehicle_start,
        "end": vehicle_start,
        "capacity": [5],
        "profile": "driving-car"
    },
    {
        "id": 1,
        "start": vehicle_start,
        "end": vehicle_start,
        "capacity": [5],
        "profile": "driving-car"
    }
]

# Configuração dos trabalhos (jobs)
jobs = [
    {
        "id": index,
        "location": coords,
        "amount": [1]
    }
    for index, coords in enumerate(coords)
]

# Preparando os dados para a requisição
data = {
    "jobs": jobs,
    "vehicles": vehicles,
    "options": {
        "g": True
    }
}

# Fazendo a requisição para otimização
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
response = requests.post(f"{base_url}optimization", json=data, headers=headers)
optimized = response.json()

line_colors = ['green', 'orange', 'blue', 'yellow']
for route in optimized['routes']:
    route_geometry = route['geometry']['coordinates']
    folium.PolyLine(locations=[list(reversed(coords)) for coords in route_geometry],
                    color=line_colors[route['vehicle']]).add_to(m)

m.save('map.html')  # Salva o mapa em um arquivo HTML