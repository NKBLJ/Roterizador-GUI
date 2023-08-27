from PySimpleGUI import PySimpleGUI as sg

sg.theme('DarkGrey14')
layout = [
    [sg.Text('Pacotes Grandes:  '), sg.Multiline(size=(40,5), key='coord_g')],
    [sg.Text('Pacotes Pequenos:'), sg.Multiline(size=(40,5), key='coord_p')],
    [sg.Text('Capacidade Moto:  '), sg.InputText(size=3, key='nome')],
    [sg.Text('                                        '), sg.Button('Gerar Rotas', key='Gerar_Rotas')]
]

# Janela
janela = sg.Window('Roteirizador', layout, icon='os.path.abspath("./Templates/icon.ico")')

# Ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
