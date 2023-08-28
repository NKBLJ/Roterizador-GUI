from PySimpleGUI import PySimpleGUI as sg

sg.theme('DarkGrey14')
layout = [
    [sg.Text('Pacotes Grandes:  '), sg.Multiline(size=(42,5), key='coord_g')],
    [sg.Text('Pacotes Pequenos:'), sg.Multiline(size=(42,5), key='coord_p')],
    [sg.Text('Capacidade Moto:  '), sg.InputText(size=3, key='nome', default_text=0), sg.Text('QTD de Carros:'),
     sg.InputText(size=3, key='qtd_veic', default_text=3), sg.Text('Tempo Máx(Hrs):'),
     sg.InputText(size=3, key='tempo', default_text=3.5)],
    [sg.Text('                                        '), sg.Button('Gerar Rotas', key='Gerar_Rotas')]
]

# Janela
janela = sg.Window('Rota Econômica', layout, icon='icon.ico')

# Ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
