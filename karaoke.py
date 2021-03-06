#!/usr/bin/python

"""
    Karaokê - by Clovis F Reis

    Programa gerenciador de execução de video clipes de karaokê
    
    20 mar 2021
    
    Utilize  python 3 ou superior
    
"""



import PySimpleGUI as sg
import icons
import sqlite3
import subprocess
import dbFunctions as db
import os
import shutil as sh
#pip install python-vlc
import vlc
from sys import platform as PLATFORM
#pip install pytube
from pytube import YouTube
import hashlib as hl
import time


class eTimer(object):
    def __init__(self):
        self._start_time = time.perf_counter()
    
    def getETime(self):
        elapsed_time = time.perf_counter() - self._start_time
        return(elapsed_time)
    
    def resetETime(self):
        self._start_time = time.perf_counter()
        
        
        
def checkPasswd(con):
    criou = 0
    if not 'passwdTimer' in globals():
        global passwdTimer 
        passwdTimer = eTimer()
        criou = 1

    #print(passwdTimer.getETime(), criou)
        
    if criou == 0 and passwdTimer.getETime() <=90:
        passwdTimer.resetETime()
        return(True)
    else:
        passwd = sg.popup_get_text(title = 'Informe a senha',
                           message = "Por favor, informe a senha de administrador",
                           password_char = "*")
        if passwd ==  None:
            del passwdTimer
            return(False)

        if db.checkPasswdDB(con, passwd, hl):
            passwdTimer.resetETime()
            return(True)
        else:
            sg.Popup('Opps!', 'Senha Incorreta!', font=("Helvetica",18), keep_on_top=True)
            del passwdTimer
            return(False)


def cleanDB(con):
    erro = 0 
    #lista de vídeos
    path='./Musicas'
    dest='./MusicasOut'
    files = os.listdir(path)

    fNames = sorted([tmp.lower().replace('.mp4','') for tmp in files])
    
    #lista de arquivos no DB
    dbNames = db.getAllCodes(con)
    dbNames = sorted([tmp[0] for tmp in dbNames])
    
    #cria string para select no banco    
    extraDb = "'"+"','".join([tmp for tmp in set(dbNames).difference(fNames)])+"'"
    
    #cria lista de nome de arquivos    
    extraFiles = [tmp+'.mp4' for tmp in set(fNames).difference(dbNames)]

    if extraDb != "''":
        #copia musicas a serem apagadas do DB para musicasOut
        try:
            db.insertMusicasOut(con, extraDb)
        except:
            erro = 1
            return(erro)
        #insert apaga do DB musicas
        try:
            db.deleteMusicasOut(con, extraDb)
        except:
            erro = 1
            return(erro)

    
    #move musicas que não estão no DB
    if not os.path.isdir(dest):
        try:
            os.makedirs(dest)
        except:
            erro = 1
            return(erro)
    
    for music in extraFiles:
        try:
            sh.move(path+'/'+music,dest+'/'+music)
        except:
            erro = 1
            return(erro)
    return(erro)
        

def dwYTube(url):
    path = './download'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        sh.rmtree(path)
        os.makedirs(path)
    
    yt = YouTube(url)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    yt.download(path)
    file = os.listdir(path)[0]
    print(file)
    os.rename(path+'/'+file, path+'/tmp.mp4')

def make_window1(theme,data,dataFila,nome,titulo,cantor):
    
    sg.theme('BlueMono')
    #sg.theme('GreenMono')
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']] ]
    right_click_menu_def = [[], ['Exit']]

    headings1 = ["Intéprete", "Codigo","Título", "Letra","Idioma"]
    headings2 = ["Intéprete", "Título","Codigo"]
     
    col1=[[sg.Text('Seu nome:', font=("Helvetica",18))], 
            [sg.Input(key='nome', font=("Helvetica",18),default_text=nome)],
            [sg.Text('Título da música:', font=("Helvetica",11))], 
            [sg.Input(key='titulo', font=("Helvetica",11), default_text= titulo)],
            [sg.Text('Intéprete:                                                                                   ', font=("Helvetica",11)),
                sg.Button('',
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.filefind, 
                          key='find',
                          tooltip='Filtra a lista de músicas',
                          bind_return_key=True)], 
            [sg.Input(key='cantor', font=("Helvetica",11),default_text = cantor)],
            [sg.Text('Selecione uma música:', font=("Helvetica",11))],
            [sg.Table(values=data,
                    size=(175,20),
                    font=("Helvetica",11),
                    headings=headings1, 
                    max_col_width=25,
                    background_color='white',
                    auto_size_columns=False,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=15,
                    col_widths = (25, 0,25,30,3),
                    alternating_row_color='white',
                    key='tabela',
                    row_height=25),
                #sg.Button('Bad Key', font=("Helvetica",11)), sg.Button('Hello', font=("Helvetica",11)), 
                sg.Button('',button_color=(sg.theme_background_color(),sg.theme_background_color()), border_width=0, image_data=icons.forward, key='add',tooltip='Adiciona a música selecionada à fila')]]
            
    col2=[[sg.Text('Fila:', font=("Helvetica",18)), 
           #sg.Text('Cancela player ', font=("Helvetica",12)),
           sg.Button('',
                     button_color=(sg.theme_background_color(),sg.theme_background_color()),
                     disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                     disabled=True, 
                     tooltip='Remove música da fila', 
                     border_width=0, 
                     pad=(20,0),
                     image_data=icons.button_cancel, 
                     key='cancel'),
           sg.Button('',
                     button_color=(sg.theme_background_color(),sg.theme_background_color()),
                     disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                     disabled=True, 
                     tooltip='Exclui toda a fila de execução', 
                     border_width=0, 
                     pad=(200,0),
                     image_data=icons.trash, 
                     key='trash')],
            [sg.Table(values=dataFila,
                    size=(175,20),
                    font=("Helvetica",11),
                    headings=headings2, 
                    max_col_width=25,
                    background_color='white',
                    auto_size_columns=False,
                    display_row_numbers=False,
                    enable_events = False,
                    justification='left',
                    num_rows=20,
                    col_widths = (25, 25,10),
                    alternating_row_color='white',
                    key='fila',
                    row_height=25)]]
                    #sg.Multiline('Line 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nYou get the point.', font=("Helvetica",11),size=(75,30), k='-MLINE-')]]

    layout = [[sg.Text('Karaokê', font=("Helvetica",20)),
               sg.Button('', 
                         font=("Helvetica",11),
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.exit, 
                          key='exit',
                          tooltip='Sai do aplicativo'),
              sg.Button('', 
                         font=("Helvetica",11),
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.configure, 
                          key='config',
                          tooltip='Ferramentas administrativas')],
              [sg.Column(col1),sg.Column(col2)]] 
    
    location = (0,0)
    size =(800,600)
    
    return sg.Window('Karaokê - by Clovis F Reis', layout, right_click_menu=right_click_menu_def)

def make_admin(theme):
    
    sg.theme('BlueMono')
    #sg.theme('GreenMono')
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']] ]
    right_click_menu_def = [[], ['Exit']]

    headings1 = ["Senha Anterior", "Nova Senha","Confirma Senha"]
    
     
    col1=[[sg.Text('Nova Senha:', key='tnSenha',font=("Helvetica",11),visible = False)], 
            [sg.Input(key='nSenha', font=("Helvetica",11),visible = False, password_char = "*", do_not_clear = False)],
            [sg.Text('Confirme a Senha:',key='tcSenha', font=("Helvetica",11),visible = False)], 
            [sg.Input(key='cSenha', font=("Helvetica",11),visible = False,password_char = "*", do_not_clear = False)]]

    col2=[[sg.Button('',
                        button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                        border_width=0, 
                        image_data=icons.button_ok, 
                        key='save',
                        tooltip='Atualiza a senha',
                        visible = False)],
          
          [sg.Button('',
                        button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                        border_width=0, 
                        image_data=icons.undo, 
                        key='reset',
                        tooltip='Restaura senha original',
                        visible = False)]]            

    layout = [[sg.Button('', 
                         font=("Helvetica",11),
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.exit, 
                          key='exit',
                          tooltip='Sai desta tela'),
               sg.Button('', 
                         font=("Helvetica",11),
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.lock, 
                          key='passwd',
                          tooltip='Altera a senha'),
               sg.Button('',
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.filenew, 
                          key='new',
                          tooltip='Inclui clipe na lista de músicas'),
               sg.Button('',
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.wizard, 
                          key='clean',
                          tooltip='Realiza uma limpeza na base de dados')],
              [sg.Column(col1),sg.Column(col2)]] 
    
    location = (0,0)
    size =(800,600)
    
    return sg.Window('Administração Karaokê - by Clovis F Reis', layout, modal = True, keep_on_top = True)


def make_saveMusic(theme, tituloNew,cantorNew,letraNew,idiomaNew,arquivoNew):
    
    sg.theme('BlueMono')
    #sg.theme('GreenMono')
     
    layout=[[sg.Button('', 
                font=("Helvetica",11),
                button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                border_width=0, 
                image_data=icons.exit, 
                key='exit',
                tooltip='Cancela a operação e fecha esta janela'),
            sg.Button('',
                button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                border_width=0, 
                image_data=icons.filesave, 
                key='save',
                tooltip='Salva clipe na lista de músicas')],
            [sg.Text('\nAtenção! É necessário o download antecipado do arquivo MP4 no formato karaokê. \nEste programa não trata esta informação!\n', font=("Helvetica",12))],
            [sg.Text('Título da música:', font=("Helvetica",18))], 
            [sg.Input(key='titulo', font=("Helvetica",18), default_text= tituloNew)],
            [sg.Text('Intéprete:', font=("Helvetica",18))], 
            [sg.Input(key='cantor', font=("Helvetica",18),default_text = cantorNew)],
            [sg.Text('Idioma:', font=("Helvetica",18))], 
            [sg.Input(key='idioma', font=("Helvetica",18),default_text = idiomaNew)],
            [sg.Text('Trecho da letra:', font=("Helvetica",18))], 
            [sg.Input(key='letra', font=("Helvetica",18), default_text= letraNew)],
            [sg.Text('Nome do arquivo:', font=("Helvetica",18))], 
            [sg.Input(key='arquivo', font=("Helvetica",18), default_text= arquivoNew)]]
            #[sg.Button('',
                #button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                #border_width=0, 
                #image_data=icons.fileopen, 
                #key='save',
                #tooltip='Salva clipe na lista de músicas')]]
    location = (0,0)
    size =(800,600)
    
    return sg.Window('Karaokê - Insere Música - by Clovis F Reis', layout, modal = True, keep_on_top = True)
    #else:

def updateWindow1(window, con, nome, titulo, cantor):
    data = db.select(con,titulo,cantor)
    dataFila = db.selectFila(con)
    window.find_element('titulo').update(titulo)
    window.find_element('nome').update(nome)
    window.find_element('cantor').update(cantor)
    window.find_element('tabela').update(data)
    window.find_element('fila').update(dataFila)
    reg = db.countFila(con)[0]
    if reg[0] > 0 :
        window.Element('fila').update(select_rows=[0])
        window.Element('cancel').update(disabled = False)
        window.Element('trash').update(disabled = False)
    else:
        window.Element('cancel').update(disabled = True)
        window.Element('trash').update(disabled = True)


def updateWindowNew(window, con, nome, titulo, cantor):
    data = db.select(con,titulo,cantor)
    dataFila = db.selectFila(con)
    window.find_element('titulo').update(titulo)
    window.find_element('nome').update(nome)
    window.find_element('cantor').update(cantor)
    window.find_element('tabela').update(data)
    window.find_element('fila').update(dataFila)
    reg = db.countFila(con)[0]
    if reg[0] > 0 :
        window.Element('fila').update(select_rows=[0])
        window.Element('cancel').update(disabled = False)
    else:
        window.Element('cancel').update(disabled = True)








def tocaProxima(data):
    if data != []:
        codigo=data[0][2]
        process = subprocess.Popen("mplayer -geometry 1500:0 -fs ./Musicas/"+codigo+".mp4 </dev/null >/dev/null 2>&1" , shell=True, stdout=subprocess.PIPE)
        process.wait()
        return(0)
    else:
        return(1)
        
def nextSinger(theme):
    sg.theme('BlueMono')
    layout= [[sg.Image('', size=(300, 170), key='-VID_OUT-'),
            sg.Button('',
                button_color=(sg.theme_background_color(),sg.theme_background_color()),
                disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                disabled=False, 
                tooltip='Tela cheia', 
                border_width=0, 
                pad=(20,0),
                visible = True,
                image_data=icons.fullscreen, 
                key='fscreen'),
        sg.Button('',
                button_color=(sg.theme_background_color(),sg.theme_background_color()),
                disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                disabled=False, 
                tooltip='Sair da Tela cheia', 
                border_width=0, 
                pad=(0,0),
                visible = False,
                image_data=icons.nofscreen, 
                key='nfscreen'),
        sg.Button('',
                button_color=(sg.theme_background_color(),sg.theme_background_color()),
                disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                disabled=True, 
                tooltip='Interrompe a execução', 
                border_width=0, 
                pad=(0,100),
                image_data=icons.button_cancel, 
                key='break')],
        [sg.Text('Fila vazia! Aguardando o próximo intérprete.                                                        ', font=("Helvetica",20), key = 'txt1')]]
            
    #layout=[[col1,sg.Column(col2)],[sg.Text('Fila vazia! Aguardando o próximo intérprete.', font=("Helvetica",20), key = 'txt1')]]

    return sg.Window('Karaokê - by Clovis F Reis', layout, element_justification='center', finalize=True, resizable=True,force_toplevel = True).Finalize()


def make_windowAll(theme,data,dataFila,nome,titulo,cantor):
    
    sg.theme('BlueMono')
    #sg.theme('GreenMono')
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']] ]
    right_click_menu_def = [[], ['Exit']]

    headings1 = ["Intéprete", "Codigo","Título", "Letra","Idioma"]
    headings2 = ["Intéprete", "Título","Codigo"]
     
    col1=[[sg.Column(
                [[sg.Text('Seu nome:     ', font=("Helvetica",11))], 
                [sg.Text('Título da música:', font=("Helvetica",11))],
                [sg.Text('Intéprete:      ', font=("Helvetica",11))]]),
            sg.Column(
                [[sg.Input(key='nome', font=("Helvetica",11),default_text=nome, size=(25,1))], 
                [sg.Input(key='titulo', font=("Helvetica",11), default_text= titulo, size=(25,1))],
                [sg.Input(key='cantor', font=("Helvetica",11),default_text = cantor, size=(25,1))]])], 
            [sg.Button('',
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.filefind, 
                          key='find',
                          tooltip='Filtra a lista de músicas',
                          bind_return_key=True)],
            [sg.Text('Selecione uma música:', font=("Helvetica",11))],
            [sg.Table(values=data,
                    size=(175,20),
                    font=("Helvetica",8),
                    headings=headings1, 
                    max_col_width=25,
                    background_color='white',
                    auto_size_columns=False,
                    display_row_numbers=False,
                    justification='left',
                    num_rows=7,
                    col_widths = (25, 0,25,0,0),
                    alternating_row_color='white',
                    key='tabela',
                    row_height=18)]]
                #sg.Button('Bad Key', font=("Helvetica",11)), sg.Button('Hello', font=("Helvetica",11))]]
            
    col2=[[sg.Text('Fila:', font=("Helvetica",11)), 
           #sg.Text('Cancela player ', font=("Helvetica",12)),
           sg.Button('',
                     button_color=(sg.theme_background_color(),sg.theme_background_color()),
                     disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                     disabled=True, 
                     tooltip='Remove música da fila', 
                     border_width=0, 
                     pad=(20,0),
                     image_data=icons.button_cancel, 
                     key='cancel'),
           sg.Button('',
                     button_color=(sg.theme_background_color(),sg.theme_background_color()),
                     disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                     disabled=True, 
                     tooltip='Exclui toda a fila de execução', 
                     border_width=0, 
                     pad=(40,0),
                     image_data=icons.trash, 
                     key='trash'), 
                sg.Button('',button_color=(sg.theme_background_color(),sg.theme_background_color()), border_width=0, image_data=icons.button_ok, key='add',tooltip='Adiciona a música selecionada à fila')],
            [sg.Table(values=dataFila,
                    size=(175,20),
                    font=("Helvetica",11),
                    headings=headings2, 
                    max_col_width=25,
                    background_color='white',
                    auto_size_columns=False,
                    display_row_numbers=False,
                    enable_events = False,
                    justification='left',
                    num_rows=15,
                    col_widths = (20, 20,10),
                    alternating_row_color='white',
                    key='fila',
                    row_height=16)]]
                    #sg.Multiline('Line 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nYou get the point.', font=("Helvetica",11),size=(75,30), k='-MLINE-')]]

    sg.theme('BlueMono')
    colM2= [[sg.Image('', size=(300, 170), key='-VID_OUT-')],
        [sg.Text('Fila vazia! Aguardando o próximo intérprete.                                                        ', font=("Helvetica",20), key = 'txt1')]]
            
    #layout=[[col1,sg.Column(col2)],[sg.Text('Fila vazia! Aguardando o próximo intérprete.', font=("Helvetica",20), key = 'txt1')]]

    colM1 = [[sg.Text('Karaokê', font=("Helvetica",16)),
               sg.Button('', 
                         font=("Helvetica",11),
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.exit, 
                          key='exit',
                          tooltip='Sai do aplicativo'),
               sg.Button('', 
                         font=("Helvetica",11),
                          button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                          border_width=0, 
                          image_data=icons.configure, 
                          key='config',
                          tooltip='Ferramentas administrativas'),
            sg.Button('',
                button_color=(sg.theme_background_color(),sg.theme_background_color()),
                disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                disabled=False, 
                tooltip='Tela cheia', 
                border_width=0,
                visible = True,
                image_data=icons.fullscreen, 
                key='fscreen'),
        sg.Button('',
                button_color=(sg.theme_background_color(),sg.theme_background_color()),
                disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                disabled=False, 
                tooltip='Sair da Tela cheia', 
                border_width=0,
                visible = False,
                image_data=icons.nofscreen, 
                key='nfscreen'),
        sg.Button('',
                button_color=(sg.theme_background_color(),sg.theme_background_color()),
                disabled_button_color=(sg.theme_background_color(),sg.theme_background_color()), 
                disabled=True, 
                tooltip='Interrompe a execução', 
                border_width=0,
                image_data=icons.button_cancel, 
                key='break')],
              [sg.Column(col1)],[sg.Column(col2)]] 
    
    layout = [[sg.Column(colM1),sg.Column(colM2,expand_x =True,expand_y = True)]]
    location = (0,0)
    size =(800,600)
    
    #return sg.Window('Karaokê - by Clovis F Reis', layout, right_click_menu=right_click_menu_def)
    return sg.Window('Karaokê - by Clovis F Reis', layout, element_justification='center', finalize=True, resizable=True,force_toplevel = True).Finalize()

def mpSetup(window):
    window['-VID_OUT-'].expand(True, True)                # type: sg.Element
    #------------ Media Player Setup ---------#

    inst = vlc.Instance("--no-xlib --play-and-stop --no-loop --no-repeat")
    list_player = inst.media_list_player_new()
    media_list = inst.media_list_new([])
    list_player.set_media_list(media_list)
    player = list_player.get_media_player()
    if PLATFORM.startswith('linux'):
        player.set_xwindow(window['-VID_OUT-'].Widget.winfo_id())
    else:
        player.set_hwnd(window['-VID_OUT-'].Widget.winfo_id())
    return((player, media_list, list_player))
   
    
def updateWindow2(window, txt1, player):
    #print(txt1)
    window.find_element('txt1').update(txt1)
    if player.is_playing():
        window.Element('break').update(disabled = False)
    else:
        window.Element('break').update(disabled = True)
    #window.find_element('txt2').update(txt2)

def pInicializa():
    data=[]
    data2=[]
    con = sqlite3.connect('/var/www/html/karaoke/karaoke.db')
    #db.removeFila(con)
    data1 = db.select(con,'','')
    dataFila = db.selectFila(con)
    sg.SetOptions(window_location = (683,384))
    
    #seleciona quantidade de monitores
    twoMonit = sg.popup_yes_no('Você deseja utilizar dois monitore?\n',title='Seleção de monitores',font=("Helvetica",18),modal = True, keep_on_top=True)#,custom_text=['Sim','Não'])
    if twoMonit == 'Yes':
        windowConsulta = make_window1(sg.theme(),data1,dataFila,'','','')
        windowControle = nextSinger(sg.theme())
    else:
        windowConsulta = make_windowAll(sg.theme(),data1,dataFila,'','','')
        windowControle = windowConsulta
        
    event1, values1 = windowConsulta.read(timeout=1)
    updateWindow1(windowConsulta, con, '', '', '')
    player, media_list, list_player = mpSetup(windowControle)
    event2, values2 = windowControle.read(timeout=1)
    #windowControle.Maximize()
            
#    fullScr = False

    # This is an Event Loop 
    windowConsulta.find_element('tabela').update(select_rows=[0])
    
    return(con,windowConsulta,windowControle,player,media_list,list_player, twoMonit)
    
def pTimeOut(con, windowConsulta, values1):
    nome=values1['nome']
    titulo=values1['titulo']
    cantor=values1['cantor']
    updateWindow1(windowConsulta, con, nome, titulo, cantor)
    try:
        selected_row = values1['tabela'][0]
        linha=windowConsulta.find_element('tabela').get()[selected_row]
        #print(selected_row)
        windowConsulta.find_element('tabela').update(select_rows=[selected_row])
    except:
        #print('Faio!')
                pass

def pAdd(con, windowConsulta, values1):
    #print("[LOG] Clicked Add!")
    if values1['tabela'] == [] or values1['nome'] == '':
        sg.Popup('Opps!', 'Digite seu nome e selecione uma música!', font=("Helvetica",18), keep_on_top=True)
    else:
        selected_row = values1['tabela'][0]
        linha=windowConsulta.find_element('tabela').get()[selected_row]
        titulo=linha[2]
        codigo=linha[1]
        nome=values1['nome']
        db.atuRanking(con, codigo)
        db.insertFila(con,nome,titulo, codigo)
        titulo=''
        nome=''
        cantor=''
        updateWindow1(windowConsulta, con, nome, titulo, cantor)
        
def pfind(con, windowConsulta, values1):
    nome=values1['nome']
    titulo=values1['titulo']
    cantor=values1['cantor']
    updateWindow1(windowConsulta, con, nome, titulo, cantor)
        
def pCancel(con, windowConsulta, values1):
    nome=values1['nome']
    titulo=values1['titulo']
    cantor=values1['cantor']
    fila=values1['fila'][0]
    cantor, titulo, codigo = windowConsulta.find_element('fila').get()[fila]
    ret=sg.popup_yes_no('Deseja remover a música '+titulo+ '\nde ' + cantor + ' da fila?',title='Confirmar exclusão',font=("Helvetica",18),modal = True, keep_on_top=True)#,custom_text=['Sim','Não'])
    if ret == 'Yes':
        db.removeFilaFirst(con,codigo)
        if fila == 0:
            process = subprocess.Popen("pkill mplayer; sleep 2" , shell=True, stdout=subprocess.PIPE)
            process.wait()
        nome=values1['nome']
        titulo=values1['titulo']
        cantor=values1['cantor']
        updateWindow1(windowConsulta, con, nome, titulo, cantor)
    # else:
    #     continue
    

def pTrash(con, windowConsulta, values1):
    if not checkPasswd(con):
        return(0)
        #continue
    nome=values1['nome']
    titulo=values1['titulo']
    cantor=values1['cantor']
    ret=sg.popup_yes_no('Esta ação removerá toda a fila de execução!\n\nDeseja continuar?\n',title='Confirmar exclusão da fila',font=("Helvetica",18),modal = True, keep_on_top=True)#,custom_text=['Sim','Não'])
    if ret == 'Yes':
        ret=sg.popup_yes_no('Não queremos uma multidão enfurecida aqui!\n\n Esta ação não pode ser desfeita!!!\n\nTem certeza que deseja excluir a fila toda?\n',title='Confirmar exclusão da fila',font=("Helvetica",18),modal = True, keep_on_top=True)#,custom_text=['Sim','Não'])
        if ret == 'Yes':
            db.removeFila(con)
            process = subprocess.Popen("pkill mplayer; sleep 2" , shell=True, stdout=subprocess.PIPE)
            process.wait()
            updateWindow1(windowConsulta, con, nome, titulo, cantor)
    # else:
    #     continue

def pClean(con, windowConsulta, values1):
    if not checkPasswd(con):
        return(0)
        # continue
    ret=sg.popup_yes_no('Esta ação realizará uma limpeza no banco de dados e arquivos de vídeo, tornando-os consistentes!\nToda fila atual será removida\n\nDeseja continuar?\n',title='Confirmar limpeza',font=("Helvetica",18),modal = True, keep_on_top=True)#,custom_text=['Sim','Não'])
    if ret == 'Yes':
        ret=sg.popup_yes_no('Não queremos uma multidão enfurecida aqui!\n\n Esta ação não pode ser desfeita!!!\n\nTem certeza que deseja excluir a fila toda?\n',title='Confirmar exclusão da fila',font=("Helvetica",18),modal = True, keep_on_top=True)#,custom_text=['Sim','Não'])
        if ret == 'Yes':
            db.removeFila(con)
            process = subprocess.Popen("pkill mplayer; sleep 2" , shell=True, stdout=subprocess.PIPE)
            process.wait()
            erro = cleanDB(con)
            if erro == 1:
                sg.Popup('Opps!', 'Ocorreram erros durante a limpeza!', font=("Helvetica",18), keep_on_top=True)
            elif erro ==0:
                sg.Popup('Limpeza realizada com sucesso!', font=("Helvetica",18), keep_on_top=True)
            updateWindow1(windowConsulta, con, '', '', '')
# else:
#     continue

def pNew(con, windowConsulta, values1):
    if not checkPasswd(con):
        return(0)
        #continue
    nome=values1['nome']
    titulo=values1['titulo']
    cantor=values1['cantor']
    url=sg.popup_get_text('Digite a URL do clip a ser adicionado (necessita Internet)')
    #arquivo = sg.popup_get_file('Escolha um clip para ser adicionado', file_types = (("MP4 Files", "*.mp4"),))
    # if str(arquivo) == 'None':
    #     continue
    # if not os.path.isfile(arquivo):
    #     sg.Popup('Opps!', 'O arquivo selecionado não existe!', font=("Helvetica",18), keep_on_top=True)
    #     continue
    if str(url) == 'None':
        return(0)
        #continue
    else:
        try:
            dwYTube(url)
            #YouTube(url).streams.first().download('./tmp.mp4')
            #continue
            arquivo = './download/tmp.mp4'
        except:
            sg.Popup('Opps!', 'Ocorreu um erro realizando o download!', font=("Helvetica",18), keep_on_top=True)
            return(0)
            #continue
        valuesNew = []
        erro = 0
        codigoNew = 0
        while True:
            if valuesNew == []:
                windowNew = make_saveMusic(sg.theme(), '','','','',arquivo)
            eventNew, valuesNew = windowNew.read(timeout=120000)
            if eventNew == 'exit':
                windowNew.close()
                codigoNew = 0
                break
            elif eventNew == 'save':
                letraNew=valuesNew['letra']
                tituloNew=valuesNew['titulo']
                cantorNew=valuesNew['cantor']
                idiomaNew=valuesNew['idioma']
                arquivoNew = valuesNew['arquivo']
                if tituloNew == '':
                    sg.Popup('Opps!', 'É necessário digitar o título da música!', font=("Helvetica",18), keep_on_top=True)
                elif cantorNew == '':
                    sg.Popup('Opps!', 'É necessário digitar o nome do intérprete da música!', font=("Helvetica",18), keep_on_top=True)
                elif idiomaNew == '':
                    sg.Popup('Opps!', 'É necessário digitar o idioma da música!', font=("Helvetica",18), keep_on_top=True)
                elif not os.path.isfile(arquivoNew):
                    sg.Popup('Opps!', 'O arquivo selecionado não existe!', font=("Helvetica",18), keep_on_top=True)
                codigoNew = db.getNextCodigo(con)
                #print(tituloNew,cantorNew,arquivoNew,codigoNew, letraNew, idiomaNew)
                erro = db.insertMusica(con, cantorNew, codigoNew, tituloNew, letraNew, idiomaNew)
                try: 
                    sh.move(arquivoNew, "./Musicas/"+str(codigoNew)+".mp4")
                except:
                    erro = 1
                if erro == 1:
                    db.deleteMusica(con, codigoNew)
                    sg.Popup('Opps!', 'Não foi possível incluir o vídeo. \nNão me pergunte o porquê...', font=("Helvetica",18), keep_on_top=True)
                    
                break
        windowNew.close()
        updateWindow1(windowConsulta, con, nome, titulo, cantor)
                
def pControle(con,windowControle, event2, values2, player, media_list, list_player, getNext, showNext, first):
    data2 = db.select1Fila(con)
    
    if data2 != []:
        if showNext or first:
            cantor2, titulo2, codigo2 = data2[0]
            txt1 = 'Próximo intérprete: '+cantor2 + ', cantando '+ titulo2
            updateWindow2(windowControle, txt1, player)
            event2, values2 = windowControle.read(timeout=1000)
            #print(values)
            if not first:
                showNext = False
            first = False
            #if event == sg.TIMEOUT_EVENT and values['ID'] == 1:
        #windowControle.close()
        if not player.is_playing():
            player, media_list, list_player = mpSetup(windowControle)
            codigo2 = data2[0][2]
            media_list.add_media("./Musicas/"+codigo2+".mp4")
            list_player.play()
            db.removeFilaFirst(con, codigo2)
            getNext = True
            showNext = True
    else:
        txt1 = 'Fila vazia! Aguardando o próximo intérprete.'
        updateWindow2(windowControle, txt1, player)
        getNext = True
    
    if player.is_playing():
        #event2, values2 = windowControle.read(timeout=1000)
        if event2 == 'break':
            list_player.stop()
            player, media_list, list_player = mpSetup(windowControle)
            #player.set_position(1)
            #data2 = db.select1Fila(con)
            #cantor2, titulo2, codigo2 = data2[0]
            #print(data2)
            getNext = True
            showNext = True
    if event2 == 'fscreen':
        windowControle.Element('fscreen').update(visible = False)
        windowControle.Element('nfscreen').update(visible = True)
        windowControle.Maximize()
    if event2 == 'nfscreen':
        windowControle.Element('nfscreen').update(visible = False)
        windowControle.Element('fscreen').update(visible = True)
        windowControle.Normal()
    return(player, media_list, list_player, getNext, showNext, first)

def pAdmin(con, windowConsulta, values1):
    wAdm = make_admin(sg.theme())
    while True:
        event, values = wAdm.read(timeout=30000)
        if event == sg.TIMEOUT_EVENT:
            continue
        elif event == 'exit' or event == sg.WIN_CLOSED :
            wAdm.close()
            break
        elif event == 'clean':
            pClean(con, windowConsulta, values1)
        elif event == 'new':
            pNew(con, windowConsulta, values1)
        elif event == 'passwd':
            if not checkPasswd(con):
                return(0)
                # continue
            wAdm.Element('nSenha').update(visible = True)
            wAdm.Element('cSenha').update(visible = True)
            wAdm.Element('tnSenha').update(visible = True)
            wAdm.Element('tcSenha').update(visible = True)
            wAdm.Element('reset').update(visible = True)
            wAdm.Element('save').update(visible = True)
            wAdm.Element('new').update(disabled = True)
            wAdm.Element('clean').update(disabled = True)
            wAdm.Element('passwd').update(disabled = True)
        elif event == 'reset':
            db.resetPasswdDB(con)
            wAdm.Element('nSenha').update(visible = False)
            wAdm.Element('cSenha').update(visible = False)
            wAdm.Element('tnSenha').update(visible = False)
            wAdm.Element('tcSenha').update(visible = False)
            wAdm.Element('reset').update(visible = False)
            wAdm.Element('save').update(visible = False)
            wAdm.Element('new').update(disabled = False)
            wAdm.Element('clean').update(disabled = False)
            wAdm.Element('passwd').update(disabled = False)
            sg.Popup('Senha padrão restaurada!', font=("Helvetica",18), keep_on_top=True)
            
        elif event == 'save':
            nSenha = values['nSenha']
            cSenha = values['cSenha']
            if nSenha != '' and cSenha != '':
                if cSenha != nSenha:
                    sg.Popup('Opps!', 'As senhas não coincidem!', font=("Helvetica",18), keep_on_top=True)
                else:
                    db.insertPasswdDB(con, nSenha, hl)
            else:
                sg.Popup('Opps!', 'Digite os valores de Senha e confirmção!', font=("Helvetica",18), keep_on_top=True)

            wAdm.Element('nSenha').update(visible = False)
            wAdm.Element('cSenha').update(visible = False)
            wAdm.Element('tnSenha').update(visible = False)
            wAdm.Element('tcSenha').update(visible = False)
            wAdm.Element('reset').update(visible = False)
            wAdm.Element('save').update(visible = False)
            wAdm.Element('new').update(disabled = False)
            wAdm.Element('clean').update(disabled = False)
            wAdm.Element('passwd').update(disabled = False)

    


def main():
    sg.theme('BlueMono')
    getNext = True
    showNext = True
    first = True

    con,windowConsulta,windowControle,player,media_list,list_player,twoMonit = pInicializa()
    while True:
        #controle das ações na janela de consulta
        event1, values1 = windowConsulta.read(timeout=5000)
        #print(event1)
        if event1 in (None, 'exit'):
            ret=sg.popup_yes_no('Você está prestes a encerrar esta aplicação!\n\nDeseja continuar?\n',title='Sair',font=("Helvetica",18),modal = True, keep_on_top=True)#,custom_text=['Sim','Não'])
            if ret == 'Yes':
                if not checkPasswd(con):
                    continue
                process = subprocess.Popen("pkill mplayer; sleep 2" , shell=True, stdout=subprocess.PIPE)
                process.wait()
                break
            if ret == 'No':
                continue
        if event1 == sg.TIMEOUT_EVENT:
            pTimeOut(con, windowConsulta, values1)
        elif event1 == 'add':
            pAdd(con, windowConsulta, values1)
        elif event1 == 'find':
            pfind(con, windowConsulta, values1)
        elif event1 == 'cancel': 
            pCancel(con, windowConsulta, values1)
        elif event1 == 'trash': 
            pTrash(con, windowConsulta, values1)
        elif event1 == 'clean':
            pClean(con, windowConsulta, values1)
        elif event1 == 'new':
            pNew(con, windowConsulta, values1)
        elif event1 == 'config':
            if not checkPasswd(con):
                continue
            
            pAdmin(con, windowConsulta, values1)
        
        
        #controle das ações na janela de controle
        event2, values2 = windowControle.read(timeout=1000)        
        if event2 in (None, 'Exit'):
            break
        
        player, media_list, list_player, getNext, showNext, first = pControle(con,windowControle, event2, values2, player, media_list, list_player, getNext, showNext, first)


    con.close()
    windowControle.close()
    if twoMonit == 'Yes':
        windowConsulta.close()
    exit(0)

if __name__ == '__main__':
    main()

