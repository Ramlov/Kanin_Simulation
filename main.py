import PySimpleGUI as sg
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")
import game
import os


#set the theme for the screen/window
sg.theme("DarkBlue12")



def draw_figure(canvas, figure): #Figure on canvas
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def delete_fig(fig): #Delete or update figure
    fig.get_tk_widget().forget()
    plt.close('all')



#Creating the options frame
options=[[sg.Frame('Choose your gamemode',[[sg.Radio('Fast Mode','mode', key ='FAST'),
                                         sg.Radio('Normal Mode','mode', default=True, key='NORMAL'),
                                         sg.Radio('Slow Mode','mode', key='SLOW')]],border_width=3)],
        [sg.Frame('Choose your gamesettings', [[sg.Text('How many players?'), sg.Slider(orientation ='horizontal', key='players', range=(2,12))],
                                          [sg.Text('How many generations?'), sg.Input('1000',key='generations', size=(9, 1))],
                                          [sg.Checkbox('Confidence interval', key='con_int')]], border_width=3)],
        [sg.Button('Submit', font=('Times New Roman',12))],
        [sg.Text('')],
        [sg.Text('Want to play the game?')],
        [sg.Button('Play game', font=('Times New Roman',12))],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Frame('Datadump',[[sg.Text(' ', key='-TIME-')],
                              [sg.Text(' ', key='-GAMEM-')],
                             [sg.Text(' ', key='-Playerwin-')]])]
        ]


#Creating the choices frame
choices = [[sg.Frame('Game Settings', layout= options, expand_y=True)]]


items_chosen = [[sg.Text('Simulering')],
                [sg.Graph(canvas_size=(600,463),
                            graph_bottom_left=(0,0),
                            graph_top_right=(600,463),
                            key = 'options')]]
              
# Create layout with two columns using precreated frames
layout = [[sg.Column(choices, element_justification='c', vertical_alignment='top'), 
            sg.Column(items_chosen, element_justification='c')]]

#Define Window
window =sg.Window("Kanin Hop Hop",layout)

#Read  values entered by user
#window['players'].update(int(values['players']))
#access all the values and if selected add them to a string

fig_gui = None

while True:
    event, values = window.read()  # Read  values entered by user
    gamemode = 'Normal'
    if event == None or event == 'Exit': #If window is closed then break
        break
    if event == 'Submit':# If submit button is clicked display chosen values
        try:
            if event == 'FAST':
                gamemode = 'Fast'
            elif event == 'NORMAL':
                gamemode = 'Normal'
            elif event == 'SLOW':
                gamemode = 'Slow'
            if fig_gui != None:
                delete_fig(fig_gui)
            fig, time, playerwins = game.run(int(values['generations']), int(values['players']), gamemode, values['con_int'])
            fig_gui = draw_figure(window['options'].TKCanvas, fig)
            window['-TIME-'].update(value=f'{round(time, 2)} seconds')
            window['-GAMEM-'].update(value=f'The gamemode is: {gamemode}')
            window['-Playerwin-'].update(value=f'Players had a {playerwins}player %')
        except Exception as e: #Handling wrong input and other errors
            sg.popup_error(f'An error accoured, contact Mathias. Error code: {e}')
    elif event == 'Play game':
        import py_sgame 
        py_sgame.main_menu()
#Close Window 
window.close()    