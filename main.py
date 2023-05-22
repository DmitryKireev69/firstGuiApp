import PySimpleGUI as sg
import shelve

def loadData():
    try:
        db = shelve.open('test.txt')
        data = db['test']
        db.close()
        return data
    except:
        db = shelve.open('test.txt')
        db['test'] = [
            [1, 'Леброн Джеймс Джеймсович', 206],
            [2, 'Стефен Карри Кариевич', 1.88],
            [3, 'Майкл Джордан Джорджанович', 1.98],
            [4, 'Дуэйн Уэйд Уайдович', 1.93],
            [5, 'Рассел Уэстбрук Расолович', 1.91]
        ]
        data = db['test']
        db.close()
        return data

batsketballPlayers = loadData()

def saveData(data):
    db = shelve.open('test.txt')
    db['test'] = data
    db.close()

def addPlayer(values, index):
    lastName = values['lastName']
    firstName = values['firstName']
    surname = values['surName']
    height = values['height']
    player = [index, f'{lastName} {firstName} {surname}', height]
    batsketballPlayers.append(player)
    window['table'].update(batsketballPlayers)
    saveData(batsketballPlayers)

def handlerClickOnTable(values):
    if len(values['table']) != 0:
        el_num = values['table'][0]
        ell = batsketballPlayers[el_num]
        fullName = ell[1].split(' ')
        window['lastName'].Update(fullName[0])
        window['firstName'].Update(fullName[1])
        window['surName'].Update(fullName[2])
        window['height'].Update(ell[2])

def editPlayer(values):
    if len(values['table']) != 0:
        el_num = values['table'][0]
        ell = batsketballPlayers[el_num]
        player = list(filter(lambda x: ell[0] in x, batsketballPlayers))
        player[0][2] = values['height']
        lastName = values['lastName']
        firstName = values['firstName']
        surname = values['surName']
        player[0][1] = f'{lastName} {firstName} {surname}'
        window['table'].update(batsketballPlayers)
        saveData(batsketballPlayers)

layout = [
    [
        sg.Text('Last name'),
    ],
    [
        sg.InputText(key='lastName')
    ],
    [
        sg.Text('First name'),
    ],
    [
        sg.InputText(key='firstName')
    ],
    [
        sg.Text('Surname')
    ],
    [
        sg.InputText(key='surName')
    ],
    [
        sg.Text('Height')
    ],
    [
        sg.InputText(key='height')
    ],
    [
        sg.Button('Add', key='add'),
        sg.Button('Edit', key='edit')
    ],
    [
        sg.Table(
            values=batsketballPlayers, headings=["Index", "Player", "Height"], key="table", enable_events=True, auto_size_columns=False,
            col_widths=[8, 40, 8], vertical_scroll_only=True, justification="с", font="None 14"
        )
    ],
]

window = sg.Window('My first gui App', layout)
index = len(batsketballPlayers)
while True:
    event, values = window.read()
    if event == 'add':
        index += 1
        addPlayer(values, index)
    elif event == 'edit':
        editPlayer(values)
    elif event == 'table':
        handlerClickOnTable(values)

    if event in (None, 'Exit', 'Cancel'):
        break