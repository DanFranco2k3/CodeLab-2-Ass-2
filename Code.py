from tkinter import *
import json
import requests
import random
from tkinter import messagebox
from html import unescape

# Questionnaires
def questionnaires():
    question = unescape(data['results'][0]['question'])
    answer_corrected = unescape(data['results'][0]['answer_corrected'])
    answer_incorrected_list = unescape(data['results'][0]['answer_incorrected_list'])
    answers_given = unescape(answer_incorrected_list + [answer_corrected])
    random.shuffle(answers_given)

    questions.config(text=question, fg='black')
    # answer button_widgets
    for l in range(4):
        choices_givens_buttons[l].config(text=answers_given[l], state='normal')

    #result
    result_enabler_label.config(text='', background='lightblue', foreground='black')
    nxt_q.config(state='disabled')

# answer checker
def answer_checker(choices_given):
    choices_given = choices_givens_buttons[choices_given]['text']

    if choices_given == data['results'][0]['answer_corrected']:
        global score
        score_added += 2
        score_tally.config(text=f'Score - tally: {score_added}/20', fg='lightblue', bg='black')
        result_enabler_label.config(text='Nice Answer! On to the next!', foreground='lightblue', background='black')
        
        for button_widget in choices_givens_buttons:
            button_widget.config(state='disabled')
        nxt_q.config(state='normal')
    else:
        result_enabler_label.config(text='Better luck next time!', foreground='lightblue', background='black')
        for button_widget in choices_givens_buttons:
            button_widget.config(state='disabled')
        nxt_q.config(state='normal')

# when the question is answered and the next button_widget is pressed
def nxt_q():
    data['results'].pop(0)
    if len(data['results']) > 0:
        questionnaires()
        
        # the quiz is complete, now they have to press quit in order to quit the app
    else:
        result_enabler_label.config(text='Quiz complete! Thank you for answering!', foreground='white', background='black')
        nxt_q.config(state='disabled')
        button_widget(mainframe, text='Quit', command=root.destroy, bg=button_bg, fg=button_fg, font=font_style).pack(pady=10)

# frame switching
def frame_switching(frame):
    frame.tkraise()

# start the game
def start_game():
    frame_switching(mainframe)
    questionnaires()
    nxt_q.config(state='disabled')
    start_button.pack_forget()
    startframe.destroy()

# main
root = Tk()
root.title('Song Pop')
root.geometry('500x700')
root.resizable(False, False)
root.configure(bg='lightblue')
font_style = ('Times New Roman', 12)
button_bg = 'lightblue'
button_fg = 'black'

# get data from API
url = 'https://opentdb.com/api.php?amount=10&category=12&difficulty=easy&type=multiple'
response = requests.get(url)
data = response.json()

# write data to JSON
with open('song_trivia.json', 'w') as file:
    json.dump(data, file)

# Start Frame
startframe = Frame(root, bg='lightblue')
Label(startframe, text="Click 'Start' to begin the game", font=font_style, fg='black', bg='lightblue').pack(pady=50)
start_button =  Button(startframe, text='Start', command=start_game, bg=button_bg, fg=button_fg, font=font_style)
start_button.pack(pady=10)
startframe.pack(fill=Y, expand=True)

# Main Frame
mainframe = Frame(root)
mainframe.configure(bg='lightblue')

# Question Frame
questions = Label(mainframe, anchor=CENTER, wraplength=600, font=font_style)
questions.configure(bg='lightblue', fg='black')
questions.pack(pady=50)

# Answer Frame
choices_givens_buttons = []
for i in range(4):
    button_widget = Button(mainframe, command=lambda i=i: answer_checker(i), bg=button_bg, fg=button_fg, font=font_style, state=DISABLED)
    button_widget.pack(pady=5, padx=100, ipady=10, fill='x')
    choices_givens_buttons.append(Button)

result_enabler_label = Label(mainframe, anchor=CENTER, font=font_style) 
result_enabler_label.pack(pady=10)

# Score Frame
score = 0

score_tally = Label(mainframe, text=f'Score: 0/20', anchor=CENTER, font=font_style, bg='lightblue', fg='black')
score_tally.pack(pady=10)

# Next button_widget
nxt_q = Button(mainframe, text='Next', command=nxt_q, state=DISABLED, bg=button_bg, fg=button_fg, font=font_style, width=7, height=2)
nxt_q.pack(pady=10)

mainframe.pack()  # Pack the main frame

root.mainloop() 
