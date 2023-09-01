import folium
from functions import otimizar_rota, dist_numero, add_categorical_legend, otimizar_rota_moto
import openrouteservice as ors


# Com restrição de tempo nas entregas
def roteirizar(coord_g, coord_p, cap_moto, tempo, qtd_veic):
    """Recebe:
    coord_g: Coordenadas dos objetos grandes
    coord_p: Coordenadas dos objetos pequenos
    cap_moto: A capacidade de objetos que a moto transporta
    tempo: Tempo em horas para realizar as entregas
    """
    # Pegar Key da API
    with open("api-key.txt", "r") as file:
        api_key = file.readline().strip()

    # Hora final dos veiculos
    final = int((8 + tempo) * 60*60)

    # Coordenada da sede:
    sede = [-5.069952794832667, -42.82680303516773]

    # Concertar coordenadas
    coord_p = list(map(lambda lat_long: [float(lat_long[0]), float(lat_long[1])], coord_p))
    coord_g = list(map(lambda lat_long: [float(lat_long[0]), float(lat_long[1])], coord_g))

    # Criar mapa com todos os pontos
    m = folium.Map(location=sede, tiles="cartodbpositron", zoom_start=13)
    folium.Marker(location=sede, icon=folium.Icon(color="red")).add_to(m)
    for coord in coord_p+coord_g:
        folium.Marker(location=coord).add_to(m)

    # Indicadores
    distancia = []
    duracao = []

    # Criar os jobs pequenos
    jobs_p = [{"id": index + 1, "location": list(reversed(coords)), "amount": [1], 'skills': [1]} for index, coords in
              enumerate(coord_p)]
    # Criar os jobs grandes
    qtd_p = len(jobs_p)
    jobs_g = [{"id": index + qtd_p + 1, "location": list(reversed(coords)), "amount": [1], 'skills': [2]} for
              index, coords in enumerate(coord_g)]
    qtd_g = len(jobs_g)

    # Concatenar os jobs
    jobs = jobs_p + jobs_g

    if cap_moto > 0:
        # Criar os veículos (duas motos e um carro com o restante da capacidade) Requisitar a api
        capacidades = [cap_moto, qtd_g+qtd_p-2]
        skills = [[1], [1, 2]]
        custos = [{"per_hour": 200}, {"per_hour": 250}]
        vehicles = [{"id": index+1, "profile": "driving-car", "start": list(reversed(sede)), "end": list(reversed(sede)),
                     "capacity": [capacidade], "skills":skills[index], "time_window": [28800, final], "costs": custos[index]} for index, capacidade in enumerate(capacidades)]

        # Requisitar api
        otimizado = otimizar_rota_moto(api_key, jobs, vehicles)
        print(otimizado)

        # Pegar a rota com maior duração (entre as duas motos) da api
        rota_moto = otimizado['routes'][0]

        distancia.append(rota_moto['distance'])
        duracao.append((rota_moto['duration']))

        # Marcar a rota selecionada no mapa
        folium.PolyLine(
            locations=[list(reversed(coords)) for coords in ors.convert.decode_polyline(rota_moto['geometry'])['coordinates']],
            color='black').add_to(m)

        # Excluir jobs da rota já feita
        excluir = {rota_moto['steps'][i+1]['id'] for i in range(len(rota_moto['steps']) - 2)}
        jobs = [job for job in jobs if job['id'] not in excluir]

    else:
        distancia.append(0)

    # Capacidade dos veículos que sobraram
    capacidades = dist_numero(len(jobs), qtd_veic)

    # Colocar os carros furgões
    vehicles = [{"id": index + 1, "profile": "driving-car", "start": list(reversed(sede)), "end": list(reversed(sede)),
                 "capacity": [capacidade], "skills": [1,2], "time_window": [28800, final]} for index, capacidade in enumerate(capacidades)]

    # Refazer requisição com 3 veículos e os jobs que sobraram
    otimizado = otimizar_rota(api_key, jobs, vehicles)

    # Marcar as 3 rotas restantes em cores diferentes
    line_colors = ['green', 'orange', 'blue', 'yellow']
    for route in otimizado['routes']:
        distancia.append((route['distance']))
        duracao.append((route['duration']))
        folium.PolyLine(
            locations=[list(reversed(coords)) for coords in ors.convert.decode_polyline(route['geometry'])['coordinates']],
            color=line_colors[route['vehicle']]).add_to(m)

    # Concertar duração e distancia
    duracao = (sum(duracao) / len(duracao))/60
    distancia = distancia + [0]*(4 - len(distancia))

    m = add_categorical_legend(m, f'Custo: {(sum(distancia)-(3/4)*distancia[0])/10000} L<br>'
                                  f'Total: {str(sum(distancia)/1000).replace(".", ",")} Km<br>'
                                  f'Tempo Médio:<br>{duracao//60:.0f}Hr {duracao%60:.0f} Min',
                               colors=["#000", "#FA0", "#00F", "#FF0"],
                               labels=[f'{dist: ,} Km' for dist in distancia])

    # Salvar o mapa
    m.save('mapa.html')


if __name__ == '__main__':
    coord_g = [('-5.0835298', '-42.8165683'), ('-5.0651632', '-42.7936305'), ('-5.0442248', '-42.8310981'),
               ('-5.0502492', '-42.8189285'), ('-5.0395227', '-42.829918'), ('-5.0652146', '-42.7938826'),
               ('-5.0925823', '-42.7966214'), ('-5.0775346', '-42.8141138'), ('-5.0705826', '-42.8296627'),
               ('-5.0593186', '-42.8149973'), ('-5.0608146', '-42.7863733'), ('-5.0758626', '-42.7846063'),
               ('-5.0865104', '-42.8205631'), ('-5.0596706', '-42.8277191'), ('-5.0528064', '-42.8183544'),
               ('-5.1285821', '-42.7840148'), ('-5.0937283', '-42.7479283'), ('-5.1010805', '-42.7393168'),
               ('-5.1375676', '-42.8032882'), ('-5.1142868', '-42.7989141'), ('-5.1046203', '-42.7611874')]

    coord_p = [('-5.0888927', '-42.8142082'), ('-5.057743', '-42.818781'), ('-5.0653836', '-42.7993096'),
               ('-5.0340124', '-42.8152407'), ('-5.092503', '-42.736583'), ('-5.1401542', '-42.7926263'),
               ('-5.1511816', '-42.7805975'), ('-5.116329', '-42.7546262')]
    cap_moto = 6
    tempo = 8
    qtd_veic = 3
    roteirizar(coord_g, coord_p, cap_moto, tempo, qtd_veic)
