from tkinter import *
import json
import requests
import random
from tkinter import messagebox
from html import unescape

# Questionnaires
def questionnaires():
    question = unescape(data['results'][0]['question'])
    correct_answer = unescape(data['results'][0]['correct_answer'])
    incorrect_answers = unescape(data['results'][0]['incorrect_answers'])
    answers = unescape(incorrect_answers + [correct_answer])
    random.shuffle(answers)

    questions.config(text=question, fg='black')
    # answer buttons
    for i in range(4):
        choices_buttons[i].config(text=answers[i], state='normal')

    #result
    result_enabler_label.config(text='', background='lightblue', foreground='black')
    next_question.config(state='disabled')

# answer checker
def check_answer(choice):
    choice = choices_buttons[choice]['text']

    if choice == data['results'][0]['correct_answer']:
        global score
        score += 1
        score_tally.config(text=f'Score: {score}/10')
        result_enabler_label.config(text='Nice Answer! On to the next!', foreground='lightblue', background='black')
        
        for button in choices_buttons:
            button.config(state='disabled')
        next_question.config(state='normal')
    else:
        result_enabler_label.config(text='Better luck next time!', foreground='lightblue', background='black')
        for button in choices_buttons:
            button.config(state='disabled')
        next_question.config(state='normal')

# when the question is answered and the next button is pressed
def next_question():
    data['results'].pop(0)
    if len(data['results']) > 0:
        questionnaires()
        
        # the quiz is complete, now they have to press quit in order to quit the app
    else:
        result_enabler_label.config(text='Quiz completed!', foreground='white', background='black')
        next_question.config(state='disabled')
        Button(mainframe, text='Quit', command=root.destroy, bg=button_bg, fg=button_fg, font=font_style).pack(pady=10)

# frame switching
def switch_to_frame(frame):
    frame.tkraise()

# start the game
def start_game():
    switch_to_frame(mainframe)
    questionnaires()
    next_question.config(state='disabled')
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
    json.dump(data, file, indent=4)

# Start Frame
startframe = Frame(root, bg='lightblue')
Label(startframe, text="Click 'Start' to begin the game", font=font_style, fg='black', bg='lightblue').pack(pady=50)
start_button = Button(startframe, text='Start', command=start_game, bg=button_bg, fg=button_fg, font=font_style)
start_button.pack(pady=10)
startframe.pack(fill=Y, expand=True)

# Main Frame
mainframe = Frame(root)
mainframe.configure(bg='lightblue')

# Question Frame
questions = Label(mainframe, anchor=CENTER, wraplength=500, font=font_style)
questions.configure(bg='lightblue', fg='black')
questions.pack(pady=50)

# Answer Frame
choices_buttons = []
for i in range(4):
    button = Button(mainframe, command=lambda i=i: check_answer(i), bg=button_bg, fg=button_fg, font=font_style, state=DISABLED)
    button.pack(pady=5, padx=100, ipady=10, fill='x')
    choices_buttons.append(button)

result_enabler_label = Label(mainframe, anchor=CENTER, font=font_style) 
result_enabler_label.pack(pady=10)

# Score Frame
score = 0

score_tally = Label(mainframe, text=f'Score: 0/10', anchor=CENTER, font=font_style, bg='lightblue', fg='black')
score_tally.pack(pady=10)

# Next button
next_question = Button(mainframe, text='Next', command=next_question, state=DISABLED, bg=button_bg, fg=button_fg, font=font_style, width=7, height=2)
next_question.pack(pady=10)

mainframe.pack()  # Pack the main frame

root.mainloop() 
