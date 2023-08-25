def roteirizar(coord_g, coord_p, cap_moto):
    # Pegar Key da API
    with open("api-key.txt", "r") as file:
        api_key = file.readline().strip()

    # Coordenada da sede:

    # Criar mapa com todos os pontos

    # Criar os jobs pequenos
    jobs_p = [{"id": index + 1, "location": coords, "amount": [1]} for index, coords in enumerate(coord_p)]
    # Criar os jobs grandes
    qtd_p = len(jobs_p)
    jobs_g = [{"id": index + qtd_p + 1, "location": coords, "amount": [1]} for index, coords in enumerate(coord_p)]

    # Concatenar os jobs
    jobs = jobs_p + jobs_g
    for job in jobs:
        print(job)
    # Criar os veículo (duas motos e um carro com o restante da capacidade) Requisitar a api
    # Pegar a rota com maior duração (entre as duas motos) da api
    # Marcar a rota selecionada no mapa
    # Excluir coordenadas da rota já feita
    # Refazer requisição com 3 veículos e os jobs que sobraram


if __name__ == '__main__':
    coord_g = [('-5.0835298', '-42.8165683'), ('-5.0651632', '-42.7936305'), ('-5.0442248', '-42.8310981'),
               ('-5.0502492', '-42.8189285'), ('-5.0395227', '-42.829918'), ('-5.0652146', '-42.7938826'),
               ('-5.0925823', '-42.7966214'), ('-5.0775346', '-42.8141138'), ('-5.0705826', '-42.8296627'),
               ['-5.0593186', '-42.8149973'], ('-5.0608146', '-42.7863733'), ('-5.0758626', '-42.7846063'),
               ('-5.0865104', '-42.8205631'), ('-5.0596706', '-42.8277191'), ('-5.0528064', '-42.8183544'),
               ('-5.1285821', '-42.7840148'), ('-5.0937283', '-42.7479283'), ('-5.1010805', '-42.7393168'),
               ('-5.1375676', '-42.8032882'), ('-5.1142868', '-42.7989141'), ('-5.1046203', '-42.7611874')]

    coord_p = [('-5.0888927', '-42.8142082'), ('-5.057743', '-42.818781'), ('-5.0653836', '-42.7993096'),
               ('-5.0340124', '-42.8152407'), ('-5.092503', '-42.736583'), ('-5.1401542', '-42.7926263'),
               ('-5.1511816', '-42.7805975'), ('-5.116329', '-42.7546262')]
    cap_moto = 5
    roteirizar(coord_g, coord_p, cap_moto)
