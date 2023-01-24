import hashlib
import PySimpleGUI as sg

#LOGIN VARIABLES
sg.theme("Dark Purple 7")
sg.Window._move_all_windows = True

Playing = False



def title_bar(title, text_color, background_color):
    """
    Creates a "row" that can be added to a layout. This row looks like a titlebar
    :param title: The "title" to show in the titlebar
    :type title: str
    :param text_color: Text color for titlebar
    :type text_color: str
    :param background_color: Background color for titlebar
    :type background_color: str
    :return: A list of elements (i.e. a "row" for a layout)
    :rtype: List[sg.Element]
    """
    bc = background_color
    tc = text_color
    font = 'Helvetica 12'

    return [sg.Col([[sg.T(title, text_color=tc, background_color=bc, font=font, grab=True)]], pad=(0, 0), background_color=bc),
            sg.Col([[sg.Text('❎', text_color=tc, background_color=bc, font=font, enable_events=True, key='Exit')]], element_justification='r', key='-C-', grab=True,
                pad=(0, 0), background_color=bc)]

def GUI():

    def login():

        background_layout = [title_bar("Eddie's Chess Program", "White", "Gray"), [sg.Image(r'images/background4.gif')]]

        window_background = sg.Window('LOG IN', background_layout, no_titlebar=True, finalize=True, margins=(0, 0), element_padding=(0,0), right_click_menu=[[''], ['Exit',]])
        window_background['-C-'].expand(True, False, False)  # expand the titlebar's rightmost column so that it resizes correctly

        column_to_be_centered = [
            [sg.Text("Eddie's Chess Program", font=('Century_Gothic 36'))],
            [sg.Text('', font=('Century_Gothic 110'))],
            [sg.Text('Username '), sg.InputText(key= 'Username')],
            [sg.Text('Password '), sg.InputText(key= 'Password', password_char = '*')],
            [sg.Button('Log In')]
        ]

        layout = [
            [
                [sg.VPush()],
                [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
                [sg.VPush()]
            ]
        ]

        top_window = sg.Window('LOG IN WINDOW', layout, finalize=True, keep_on_top=True, grab_anywhere=False,  transparent_color=sg.theme_background_color(), no_titlebar=True)

        # window_background.send_to_back()
        # top_window.bring_to_front()

        while True:
            window, event, values = sg.read_all_windows()
            #print(event, values)
            
            #print (event)
            if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
                break
            elif event == 'Log In':
                #readlines in the login file
                file1 = open('logIn.txt', 'r')
                Lines = file1.readlines()
                #print(Lines)
                
                count = 0
                # Strips the newline character
                for line in Lines:
                    Lines[count] = line.strip()
                    count = count + 1
                
                pointer2 = 0
                loggedIn = False
        
                try:
                    while loggedIn == False:
                        if Lines[pointer2] == (values['Username']):
                            #username is correct
                            if Lines[pointer2 + 1] == hashlib.sha256(values['Password'].encode('ascii')).hexdigest():
                                #password is also correct
                                print("Logged in")
                                loggedIn = True
                                global USERNAME
                                USERNAME = values["Username"]
                                top_window.close()
                                window_background.close()
                                mainMenu()
                            else:
                                pointer2 = pointer2 + 2
                        else:
                            pointer2 = pointer2 + 2
        
                except IndexError:
                    sg.popup('ERROR LOGGING IN', 'Please try again!')
        
        top_window.close()
        window_background.close()

        '''
        Main Menu GUI #####################################################################################################
        '''

    def mainMenu():

        background_layout = [title_bar("Eddie's Chess Program", "White", "Gray"), [sg.Image(r'images/background4.gif')]]

        window_background = sg.Window('MAIN MENU', background_layout, no_titlebar=True, finalize=True, margins=(0, 0), element_padding=(0,0), right_click_menu=[[''], ['Exit',]])
        window_background['-C-'].expand(True, False, False)  # expand the titlebar's rightmost column so that it resizes correctly

        column_to_be_centered = [
            [sg.Text("Main Menu", font=('Century_Gothic 36'))],
            [sg.Text(USERNAME, font=('Century_Gothic 8'))],
            [sg.Text('', font=('Century_Gothic 120'))],
            [sg.Button('Play'), sg.Text('   ', font=('Century_Gothic 16')), sg.Button('Settings'), sg.Text('   ', font=('Century_Gothic 16')), sg.Button('Quit')]
        ]

        layout = [
            [
                [sg.VPush()],
                [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
                [sg.VPush()]
            ]
        ]

        top_window = sg.Window('MAIN MENU', layout, finalize=True, keep_on_top=True, grab_anywhere=False,  transparent_color=sg.theme_background_color(), no_titlebar=True)

        # window_background.send_to_back()
        # top_window.bring_to_front()

        while True:
            window, event, values = sg.read_all_windows()
            #print(event, values)
            
            #print (event)
            if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
                break
            elif event == "Play":
                global Playing
                Playing = True
                break
            elif event == "Settings":
                top_window.close()
                window_background.close()
                settings()
            else:
                top_window.close()
                window_background.close()
                return event
                
        
        top_window.close()
        window_background.close()

        '''
        SETTINGS WINDOW ############################################################################################
        '''
    def settings():

        background_layout = [title_bar("Eddie's Chess Program", "White", "Gray"), [sg.Image(r'images/background4.gif')]]

        window_background = sg.Window('SETTINGS', background_layout, no_titlebar=True, finalize=True, margins=(0, 0), element_padding=(0,0), right_click_menu=[[''], ['Exit',]])
        window_background['-C-'].expand(True, False, False)  # expand the titlebar's rightmost column so that it resizes correctly

        column_to_be_centered = [
            [sg.Text("SETTINGS", font=('Century_Gothic 36'))],
            [sg.Text('', font=('Century_Gothic 120'))],
            [sg.Button('Preferences + Customisation')],
            [sg.Button('Help + Extras')],
            [sg.Button('Back')]
        ]

        layout = [
            [
                [sg.VPush()],
                [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
                [sg.VPush()]
            ]
        ]

        top_window = sg.Window('SETTINGS', layout, finalize=True, keep_on_top=True, grab_anywhere=False,  transparent_color=sg.theme_background_color(), no_titlebar=True)

        # window_background.send_to_back()
        # top_window.bring_to_front()

        while True:
            window, event, values = sg.read_all_windows()
            #print(event, values)
            
            #print (event)
            if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                break
            elif event == "Preferences + Customisation":
                sg.popup("Work in Progress!")
                # opens a how to play window or link to the web
            elif event == "Help + Extras":
                top_window.close()
                window_background.close()
                helpAndExtras()
            elif event == "Back":
                top_window.close()
                window_background.close()
                mainMenu()
            else:
                top_window.close()
                window_background.close()
                return event
                
        
        top_window.close()
        window_background.close()

    '''
    HELP AND EXTRAS WINDOW ############################################################################################
        '''        

    def helpAndExtras():

        background_layout = [title_bar("Eddie's Chess Program", "White", "Gray"), [sg.Image(r'images/background4.gif')]]

        window_background = sg.Window('HOW TO PLAY', background_layout, no_titlebar=True, finalize=True, margins=(0, 0), element_padding=(0,0), right_click_menu=[[''], ['Exit',]])
        window_background['-C-'].expand(True, False, False)  # expand the titlebar's rightmost column so that it resizes correctly

        column_to_be_centered = [
            [sg.Text("HELP AND EXTRAS", font=('Century_Gothic 36'))],
            [sg.Text('', font=('Century_Gothic 120'))],
            [sg.Button('How to Play'), sg.Text('   ', font=('Century_Gothic 16')), sg.Button('Credits')],
            [sg.Button('Back')]
        ]

        layout = [
            [
                [sg.VPush()],
                [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
                [sg.VPush()]
            ]
        ]

        top_window = sg.Window('HELPANDEXTRAS', layout, finalize=True, keep_on_top=True, grab_anywhere=False,  transparent_color=sg.theme_background_color(), no_titlebar=True)

        # window_background.send_to_back()
        # top_window.bring_to_front()

        while True:
            window, event, values = sg.read_all_windows()
            #print(event, values)
            
            #print (event)
            if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                break
            elif event == "How to Play":
                sg.popup("Work in Progress!")
                # opens a how to play window or link to the web
            elif event == "Credits":
                sg.popup("Created by Eddie", "AQA A-Level Programming Project")
            elif event == "Back":
                top_window.close()
                window_background.close()
                settings()
            else:
                top_window.close()
                window_background.close()
                return event
                
        
        top_window.close()
        window_background.close()

    login()
    return Playing

'''
CHOOSING A PROMOTION ---------------------------------------------------------
'''


def choosePromote(color):
        if color == "Black":
            column_to_be_centered = [
                [sg.Text('Choose a Promotion')],
                [sg.Button('Queen'), sg.Image(r'images/bQ.png'), sg.Button('Knight'), sg.Image(r'images/bN.png')],
                [sg.Button('Rook'), sg.Image(r'images/bR.png'), sg.Button('Bishop'), sg.Image(r'images/bB.png')]
            ]
        else:
            column_to_be_centered = [
                [sg.Text('Choose a Promotion')],
                [sg.Button('Queen'), sg.Image(r'images/wQ.png'), sg.Button('Knight'), sg.Image(r'images/wN.png')],
                [sg.Button('Rook'), sg.Image(r'images/wR.png'), sg.Button('Bishop'), sg.Image(r'images/wB.png')]
            ]

        layout = [
            [
                [sg.VPush()],
                [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
                [sg.VPush()]
            ]
        ]

        top_window = sg.Window('Choose a Promotion', layout, finalize=True, keep_on_top=True, grab_anywhere=False, no_titlebar=True)

        while True:
            window, event, values = sg.read_all_windows()

            if event != 'Exit':
                top_window.close()
                return event

def kingCaptured(color):
    if color == "Black":
        sg.popup("White Wins!")
    else:
        sg.popup("Black Wins!")