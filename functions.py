import requests
import re


def dist_numero(number):
    """Função que distribui os números numa lista de 3"""
    quotient, remainder = divmod(number, 3)
    result = [quotient + (1 if i < remainder else 0) for i in range(3)]
    return result


def otimizar_rota(api_key, jobs, vehicles):
    """Recebe a API, os Jobs e os Vehicles e retorna o json da otimização"""
    base_url = 'https://api.openrouteservice.org/optimization'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "jobs": jobs,
        "vehicles": vehicles,
        "options": {
            "g": True  # Solicita a inclusão da geometria
        }
    }

    response = requests.post(base_url, json=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
    else:
        print('Erro: {}'.format(response))

    return response

def link_em_coords(link):
    """A função recebe o link do Google maps com os pontos da rota e retorna uma lista de tuplas com as cordenadas
    na forma [(lat, long)...]"""
    busca = re.compile(r'/(-?\d*.\d*,-?\d*.\d*)')
    lista = busca.findall(link)
    lista = [(lat, long) for lat, long in (coord.split(',') for coord in lista)]
    return lista
