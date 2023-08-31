from PySimpleGUI import PySimpleGUI as sg
from roteirizar_v2 import roteirizar
from functions import link_em_coords
import webbrowser
import os


sg.theme('DarkGrey14')
layout = [
    [sg.Text('Pacotes Grandes:  '), sg.Multiline(size=(42, 5), key='coord_g')],
    [sg.Text('Pacotes Pequenos:'), sg.Multiline(size=(42, 5), key='coord_p')],
    [sg.Text('Capacidade Moto:  '), sg.InputText(size=3, key='cap_moto', default_text=0), sg.Text('QTD de Carros:'),
     sg.InputText(size=3, key='qtd_veic', default_text=3), sg.Text('Tempo Máx(Hrs):'),
     sg.InputText(size=3, key='tempo', default_text=3.5)],
    [sg.Text('                                        '), sg.Button('Gerar Rotas', key='Gerar_Rotas')]
]

# Janela
janela = sg.Window('Rota Econômica', layout, icon=(os.path.abspath("./icon.ico")))

# Ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    elif eventos == 'Gerar_Rotas':
        if not valores['coord_p'] and not valores['coord_g']:
            sg.Popup('Não tem objetos para entregar!', no_titlebar=True)
            continue
        sg.PopupTimed('Gerando rotas...', no_titlebar=True, auto_close_duration=2, button_type=5, non_blocking=True)
        coord_g = link_em_coords(valores['coord_g'])
        coord_p = link_em_coords(valores['coord_p'])
        roteirizar(coord_g, coord_p, int(valores['cap_moto']), float(valores['tempo']), int(valores['qtd_veic']))
        webbrowser.open_new_tab(os.path.abspath("./mapa.html"))
