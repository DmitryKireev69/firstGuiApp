import PySimpleGUI as sg
import shelve


def load_data():
    with shelve.open('players.txt') as db:
        try:
            data = db['players']
            db.close()
        except KeyError:
            db['players'] = [
                [1, 'Леброн Джеймс Джеймсович', 206],
                [2, 'Стефен Карри Кариевич', 1.88],
                [3, 'Майкл Джордан Джорджанович', 1.98],
                [4, 'Дуэйн Уэйд Уайдович', 1.93],
                [5, 'Рассел Уэстбрук Расолович', 1.91]
            ]
            data = db['players']
            db.close()
        return data


batsketball_players = load_data()


def save_data(data):
    db = shelve.open('players.txt')
    db['players'] = data
    db.close()


def add_player(data, number):
    last_name = data['last_name']
    first_name = data['first_name']
    surname = data['surname']
    height = data['height']
    player = [number, f'{last_name} {first_name} {surname}', height]
    batsketball_players.append(player)
    window['table'].update(batsketball_players)
    save_data(batsketball_players)


def handler_click_on_table(data):
    if data['table']:
        el_num = data['table'][0]
        ell = batsketball_players[el_num]
        full_name = ell[1].split(' ')
        window['last_name'].Update(full_name[0])
        window['first_name'].Update(full_name[1])
        window['surname'].Update(full_name[2])
        window['height'].Update(ell[2])


def edit_player(data):
    if data['table']:
        el_num = data['table'][0]
        ell = batsketball_players[el_num]
        player = list(filter(lambda x: ell[0] in x, batsketball_players))
        player[0][2] = data['height']
        last_name = data['last_name']
        first_name = data['first_name']
        surname = data['surname']
        player[0][1] = f'{last_name} {first_name} {surname}'
        window['table'].update(batsketball_players)
        save_data(batsketball_players)


layout = [
    [
        sg.Text('Last name'),
    ],
    [
        sg.InputText(key='last_name')
    ],
    [
        sg.Text('First name'),
    ],
    [
        sg.InputText(key='first_name')
    ],
    [
        sg.Text('Surname')
    ],
    [
        sg.InputText(key='surname')
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
            values=batsketball_players, headings=["Index", "Player", "Height"],
            key="table", enable_events=True, auto_size_columns=False,
            col_widths=[8, 40, 8], vertical_scroll_only=True,
            justification="с", font="None 14"
        )
    ],
]

window = sg.Window('My first gui App', layout)
index = len(batsketball_players)
while True:
    event, values = window.read()
    if event == 'add':
        index += 1
        add_player(values, index)
    elif event == 'edit':
        edit_player(values)
    elif event == 'table':
        handler_click_on_table(values)
    elif event in (None, 'Exit', 'Cancel'):
        break
