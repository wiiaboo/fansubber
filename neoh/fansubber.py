# -*- coding: utf-8 -*-
''' Fansubber Teste '''

# Bibliotecas
import sqlite3, os, re, sys
from optparse import OptionParser
from sys import argv

#Variáveis Globais
bd = 'fansub.sqlite'    # Nome da base de dados
mkvmerge = 'mkvmerge'   # Localização do mkvmerge // É sempre "mkvmerge", acho que não é preciso.

# Cria uma nova base de dados se não existir
if not os.path.isfile(bd):
    open(bd, 'w')

''' Cria o nome do ficheiro muxado '''
def createFilename(str):    
    return re.sub('_{2,}', '_', re.sub('[/\\\?%*:|<>. ]', '_', str))

''' Executa e devolve uma query na base de dados, podendo também imprimir no ecrã '''
def execDatabase(statement, screen = False, feedback = True):    
    # Liga-se à base de dados
    ligacao = sqlite3.connect(bd)
    query = ligacao.cursor()
    
    # Executa a query    
    query.execute(statement)
    
    # Se queremos mostrar no ecrã ou enviar o resultado
    if feedback:
        fetch = query.fetchall()
    
    # Se queremos mostrar no ecrã
    if screen:
        for row in fetch:
            [print(item, end = ' ') for item in row]
            print()        
    
    # Se queremos enviar o resultado
    query.close()
    return fetch

''' Devolve o tipo de argumento recebido '''
def getType(arg):
    types = {'subs' : ['ssa', 'ass', 'srt'], 'video' : ['avi', 'mkv', 'mp4'], 'fonts' : ['ttf', 'otf'], 'chapters' : ['xml'], 'projects' : ['fma']}

    try:
        return [type for type in types if arg[-3:].lower() in types[type]].pop()
    except:
        return

"""
mkvmerge

# muxed ep
'-o "<muxed>" --language "1:jpn" --track-name "1:[<rawsauce-video>] <nome projecto> <título do ep>" 
--default-track "1:yes" --aspect-ratio "1:16/9" --language "2:jpn" --track-name 
"2:[<rawsauce-audio>] LC-AAC 2.0" --default-track "2:yes" -a 2 -d 1 -S --no-global-tags --no-chapters "<raw>"

# cenas da sub
--language "0:Por" --track-name "0:[<fansub>] ASS com Estilos" --default-track "0:yes" -s 0 "<ass>" # tens que fazer uma linha destas por cada fonte

--track-order "0:1,0:2,1:0"

# uma linha destas por cada fonte
--attachment-mime-type "application/x-truetype-font" --attach-file "<sítio onde está a fonte>"

--title "<fansub> <nome projecto> <título do ep>" --chapters "<capitulos>"
"""

def mux(muxed, video, videoTitle, aspectRatio = "16/9", audio = False, audioTitle, title, subs, fonts, chapters):
        command = '''{} -o {} ''' % (mkvmerge, muxed)
        command += '''--language "1:jpn --track-name "1:{}" --default-track "1:yes" --aspect-ratio "1:{}" ''' % (videoTitle, aspectRatio)
        if not audio:
                command += '''--language "2:jpn" --trackname "2:{}" --default-track "2:yes" -a 2 -d 1 -S --no-global-tags --no-chapters "{}" ''' % (audioTitle, video)
        else:
                command += '''-d 1 -A -S --no-global-tags --no-chapters "{}" --language "2:jpn" --trackname "1:{}" --default-track "1:yes" -a 1 -D -S --no-global-tags --no-chapters "{}" ''' % (video, audioTitle, audio)

def getSource(arg):
    try:
        return re.search('\[([^[]*)\].*', arg).group(0)
    except:
        return 'Default' # Será chamada À BD
    
'''
#
# To-do:
#
# getRaw
# getSubs
# getFonts
# getChapters
# getProject
# Your mom
#
'''

''' Cria os argumentos de muxing '''
def getMuxingArgs(vargs, output = mkvmerge):
    
    projectlist = ['fma', 'chi', 'ss', 'needless']  # Será chamada À BD
    
    mux = {'video' : [], 'subs' : [], 'fonts' : [], 'chapters' : [], 'projects' : []}
        
    for arg in vargs:
        if getType(arg) in mux:
            mux[getType(arg)].append(arg)        

    
    print(mux)
            
    return output

# Menu
print('Projectos existentes:')
execDatabase('SELECT id, fansub FROM encodes', True)

'''
# Ciclo da escolha do projecto
while True:
    try:
        # Número do projecto na lista existente
        id = int(input('Número do projecto: '))
                
        # Se for negativo, é inválido
        if id < 1:
            print('Número inválido, insere outro.')            
        # Se o número do projecto não existir, é inválido
        else:
            print('Escolheste', execDatabase('SELECT id, fansub FROM encodes')[id - 1][1])
            break # Se for válido, sai do ciclo
    
    # Lança uma excepção sempre que não se inserir um número ou for maior que o número de indices na lista
    except:
        print('Número inválido, insere outro.')

# Imprime no ecrã as opções de muxing do procjeto
print(execDatabase('SELECT param FROM encodes WHERE id = ' + str(id))[0][0])

# Confirma se as opções de muxing estão certas
input('Está correcto? ')
'''

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")

args = ['fma', 'raw.mp4', 'chapters.xml', 'font1.otf', 'font2.ttf', 'subs.ass', 'subs2.ass']
(options, args) = parser.parse_args(args)

print(options, args)
print(getType('rawr.mkv'))

print(getMuxingArgs(args))
