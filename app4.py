import pyautogui
import time
import logging
import wx
import os

# Definir IDs dos itens do menu de contexto
ID_ATIVAR_DESATIVAR = wx.NewIdRef()
ID_DEFINIR_INTERVALO_F15 = wx.NewIdRef()
ID_DEFINIR_TEMPO_INATIVIDADE = wx.NewIdRef()
ID_SAIR = wx.NewIdRef()

# Configurações
INTERVALO_F15 = 20  # Segundos
TEMPO_INATIVIDADE = 0  # Segundos (0 para nunca)

# Logging
logging.basicConfig(filename='mantemligado.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Flag de ativação
ativo = False

# Definir start_time
start_time = time.time()

# Função para pressionar F15
def pressionar_f15():
    logging.info('Pressionando F15')
    pyautogui.press('f15')

# Função para definir o intervalo F15
def definir_intervalo_f15(event):
    global INTERVALO_F15

    dlg = wx.TextEntryDialog(None, 'Intervalo F15 (segundos)', 'Configurações', str(INTERVALO_F15))
    if dlg.ShowModal() == wx.ID_OK:
        try:
            INTERVALO_F15 = int(dlg.GetValue())
            logging.info('Intervalo F15 definido para %s segundos', INTERVALO_F15)
        except ValueError:
            logging.error('Intervalo F15 inválido')

# Função para definir o tempo de inatividade
def definir_tempo_inatividade(event):
    global TEMPO_INATIVIDADE

    dlg = wx.TextEntryDialog(None, 'Tempo de inatividade (segundos)', 'Configurações', str(TEMPO_INATIVIDADE))
    if dlg.ShowModal() == wx.ID_OK:
        try:
            TEMPO_INATIVIDADE = int(dlg.GetValue())
            if TEMPO_INATIVIDADE == 0:
                logging.info('Tempo de inatividade desativado')
            else:
                logging.info('Tempo de inatividade definido para %s segundos', TEMPO_INATIVIDADE)
        except ValueError:
            logging.error('Tempo de inatividade inválido')

# Função para fechar o aplicativo
def fechar_app(event):
    logging.info('Saindo')
    app.Exit()

# Loop principal
while True:
    # Se ativo, pressiona F15
    if ativo:
        pressionar_f15()
        time.sleep(INTERVALO_F15)

    # Verifica tempo de inatividade
    if TEMPO_INATIVIDADE > 0 and time.time() - start_time > TEMPO_INATIVIDADE:
        logging.info('Desativando por inatividade')
        ativo = False

    # Espera 1 segundo
    time.sleep(1)

# Função para o menu de contexto
def menu_contexto(event):
    global ativo, INTERVALO_F15, TEMPO_INATIVIDADE

    menu = wx.Menu()
    menu.Append(ID_ATIVAR_DESATIVAR, 'Ativar/Desativar')
    menu.Append(ID_DEFINIR_INTERVALO_F15, 'Definir Intervalo F15')
    menu.Append(ID_DEFINIR_TEMPO_INATIVIDADE, 'Definir Tempo de Inatividade')
    menu.AppendSeparator()
    menu.Append(ID_SAIR, 'Sair')

    taskbar = wx.FindWindowByName('TaskBar')
    taskbar.PopupMenu(menu)

# App wxPython
app = wx.App()

# Criação do ícone na bandeja do sistema
taskbar = wx.TaskBarIcon()
icon = wx.NullIcon
try:
    icon = wx.Icon('active_icon.png', wx.BITMAP_TYPE_ICO)
except Exception as e:
    logging.error('Erro ao carregar o ícone: %s', e)

if icon:
    taskbar.SetIcon(icon, 'Mantém PC Desperto')
    taskbar.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, menu_contexto)  # Binding para o clique direito

    # Bind dos eventos do menu
    app.Bind(wx.EVT_MENU, definir_intervalo_f15, id=ID_DEFINIR_INTERVALO_F15)
    app.Bind(wx.EVT_MENU, definir_tempo_inatividade, id=ID_DEFINIR_TEMPO_INATIVIDADE)
    app.Bind(wx.EVT_MENU, fechar_app, id=ID_SAIR)

    # Inicia o loop do wxPython
    app.MainLoop()
else:
    logging.error('Ícone não encontrado, fechando o programa.')
    app.Exit()
