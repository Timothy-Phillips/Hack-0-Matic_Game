import PySimpleGUI as sg
import random
import numpy as np

# Constants
MIN_WORD_SET_SIZE = 10 # Determins how many similar words are required to accept the word
NUM_ATTEMPTS = 4
WORD_LEN_EASY = 5
WORD_LEN_MED = 7
WORD_LEN_HARD = 9

NUM_WORDS_EASY = 10
NUM_WORDS_MED = 12
NUM_WORDS_HARD = 12
# Number of silimar types of words per difficulty must be a factor of the NUM_WORDS 
# associated with the same difficulty
NUM_SIM_EASY = 2
NUM_SIM_MED = 4
NUM_SIM_HARD = 6
# How simlar words needs to be per difficulty
SIM_SCORE_EASY = 0.5
SIM_SCORE_MED = 0.6
SIM_SCORE_HARD = 0.6

DEFAULT_FONT = "consolas"
DEFAULT_FONT_SIZE = 12

# This is not designed to be secure!
ADMIN_HASH = 186320432

attempts = NUM_ATTEMPTS

def consistant_hash(string):
    seed = 1
    for char in string:
        seed = (seed * 31 + ord(char)) & 0xFFFFFFFF
    return seed
    

def find_words(difficulty, seed):
    # Set difficulty parameters
    if difficulty == "Easy":
        word_len = WORD_LEN_EASY
        num_words = NUM_WORDS_EASY
        num_sim = NUM_SIM_EASY
        threshold = SIM_SCORE_EASY
    elif difficulty == "Medium":
        word_len = WORD_LEN_MED
        num_words = NUM_WORDS_MED
        num_sim = NUM_SIM_MED
        threshold = SIM_SCORE_MED
    else:
        word_len = WORD_LEN_HARD
        num_words = NUM_WORDS_HARD
        num_sim = NUM_SIM_HARD
        threshold = SIM_SCORE_HARD

    # Seed RNG
    random.seed(consistant_hash(seed))
    np.random.seed(consistant_hash(seed))

    words_not_found_flag = True
    choice_not_selected = True
    word_list = []
    final_choice = ""
    
    input_file_path = 'input.txt'
    with open(input_file_path, 'r') as input_file:
        words = input_file.read().splitlines()

    filtered_words = [word for word in words if len(word) == word_len]

    # Determine selected words
    while (words_not_found_flag):
        choice = random.choice(filtered_words)
        similar_strings = [string for string in filtered_words if compare_words(string, choice) > threshold]
        if len(similar_strings) >= MIN_WORD_SET_SIZE:
            if (choice_not_selected):
                final_choice = choice
                choice_not_selected = False
            word_list.append(choice)
            similar_strings.remove(choice)
            for i in range(int(num_words/num_sim) - 1):
                choice = random.choice(similar_strings)
                similar_strings.remove(choice)
                word_list.append(choice)
        if (len(word_list) == num_words):
            words_not_found_flag = False
    
    for i in range(0, random.randint(0, 6)):
        word_list.append(gib_gen(difficulty))

    while (len(word_list) % 4 != 0):
        word_list.append(gib_gen(difficulty))

    # Get a good shuffle
    np.random.shuffle(word_list)
    np.random.shuffle(word_list)
    np.random.shuffle(word_list)

    # Place word_list into 2d array
    word_array = split_array(word_list)

    return final_choice, word_array
            
# Only compares words of equal length
def compare_words(word1, word2):
    total_similar = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            total_similar += 1
    return total_similar / len(word1)

#TODO: Improve the seeds by making them words
def get_default_seed():
    input_file_path = 'input.txt'
    with open(input_file_path, 'r') as input_file:
        words = input_file.read().splitlines()
    seed = random.choice(words)
    return seed

def change_attempts(attempt = None):
    global attempts
    if attempt == None:
        attempts -= 1
    else:
        attempts = attempt
    window["attempts_text"].update("\n\nAttempts: " + str(attempts))
    return

def send_output(string):
    window["output_box"].update(window["output_box"].get() + "\n" + string)

def gib_gen(difficulty):
    output = "</"
    characters = [".", ",", "!", "@", "#", "^", "?", "-", "*"]
    if difficulty == "Easy":
        for i in range(WORD_LEN_EASY - 4):
            output += random.choice(characters)
    if difficulty == "Medium":
       for i in range(WORD_LEN_MED - 4):
            output += random.choice(characters)
    if difficulty == "Hard":
       for i in range(WORD_LEN_HARD - 4):
            output += random.choice(characters)
    output += "/>"
    return output

def split_array(arr):
    num_columns = 4
    num_items = len(arr)
    num_rows = num_items // num_columns

    result = [[0] * num_columns for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_columns):
            result[i][j] = arr[i * num_columns + j]

    return result

def toggle_visiblility_upper(on_or_off):
    if (on_or_off == "on"):
        window["seed_text"].update(visible=True)
        window["seed_input"].update(visible=True)
        window["difficulty_text"].update(visible=True)
        window["difficulty_input"].update(visible=True)
        window["begin_game_button"].update(visible=True)
    else:
        window["seed_text"].update(visible=False)
        window["seed_input"].update(visible=False)
        window["difficulty_text"].update(visible=False)
        window["difficulty_input"].update(visible=False)
        window["begin_game_button"].update(visible=False)        

def toggle_visiblility_lower(on_or_off):
    if (on_or_off == "on"):
        window["attempts_text"].update(visible=True)
        window["col1"].update(visible=True)
        window["col2"].update(visible=True)
        window["col3"].update(visible=True)
        window["col4"].update(visible=True)
        window["text_input"].update(visible=True)
        window["enter_password_text"].update(visible=True)
        window["Check Password"].update(visible=True)
        window["output_box"].update(visible=True)
        window["terminal"].update(visible=True)
    else:
        window["attempts_text"].update(visible=False)
        window["col1"].update(visible=False)
        window["col2"].update(visible=False)
        window["col3"].update(visible=False)
        window["col4"].update(visible=False)
        window["text_input"].update(visible=False)
        window["enter_password_text"].update(visible=False)
        window["Check Password"].update(visible=False)
        window["output_box"].update(visible=False)
        window["terminal"].update(visible=False) 

# Assumes that both are the same length
def score_guess(guess, answer):
    score = 0
    for i in range(len(answer)):
        if guess[i] == answer[i]:
            score += 1
    return "("+ str(score) + "/" + str(len(guess)) +")"

def update_playfield(word_array):
    num_rows = len(word_array)
    col1_text=""
    col2_text=""
    col3_text=""
    col4_text=""

    # Not the most elagent solution, but effective
    for i in range(0, num_rows):
        col1_text += word_array[i][0] + "\n\n"
    for i in range(0, num_rows):
        col2_text += word_array[i][1] + "\n\n"    
    for i in range(0, num_rows):
        col3_text += word_array[i][2] + "\n\n"
    for i in range(0, num_rows):
        col4_text += word_array[i][3] + "\n\n"

    window["col1_text"].update(col1_text)
    window["col2_text"].update(col2_text)
    window["col3_text"].update(col3_text)
    window["col4_text"].update(col4_text)
    
    return

# Fallout Theme
fallout_pipboy_theme = {
    'BACKGROUND': "#002f00",
    'TEXT': "#00ee00",
    'INPUT': "#002f00",
    'TEXT_INPUT': "#00ee00",
    'SCROLL': '#002f00',
    'BUTTON': ("#00ee00", "#002f00"),
    'PROGRESS': ("#00ee00", "#002f00"),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}

# Set the theme
sg.theme_add_new('FalloutPipBoyTheme', fallout_pipboy_theme)
sg.theme('FalloutPipBoyTheme')

layout = [[sg.Column([[sg.Text(" Welcome to the", font=("consolas 20 bold"))],
                       [sg.Text("HACK-0-MATIC", font=("consolas 30 bold"))]
                       ], justification="center")],

          [sg.Text("Seed:", key="seed_text", font=(DEFAULT_FONT,DEFAULT_FONT_SIZE))],
          [sg.Input(default_text=get_default_seed(), key="seed_input", font=(DEFAULT_FONT,DEFAULT_FONT_SIZE))],
          [sg.Text("\nDifficulty:", key="difficulty_text", font=(DEFAULT_FONT,DEFAULT_FONT_SIZE))],
          [sg.Combo(["Easy", "Medium", "Hard"], default_value="Easy", key="difficulty_input", font=(DEFAULT_FONT,DEFAULT_FONT_SIZE))],
          [sg.Button("Begin Game", key="begin_game_button", font=(DEFAULT_FONT,DEFAULT_FONT_SIZE))],
          [sg.Text("\n\nAttempts: " + str(attempts), key="attempts_text", visible=False, font=(DEFAULT_FONT,DEFAULT_FONT_SIZE))],

 
[
        sg.Column([
            [sg.Frame("Terminal", layout=[
                [
                    sg.Column([
                        [sg.Text("Col 1", key="col1_text", font=("Courier New", 14), background_color="black")],
                    ], visible=False, key="col1", justification="c", background_color="black"),
                    sg.Column([
                        [sg.Text("Col 2", key="col2_text", font=("Courier New", 14), background_color="black")],
                    ], visible=False, key="col2", justification="c", background_color="black"),
                    sg.Column([
                        [sg.Text("Col 3", key="col3_text", font=("Courier New", 14), background_color="black")],
                    ], visible=False, key="col3", justification="c", background_color="black"),
                    sg.Column([
                        [sg.Text("Col 4", key="col4_text", font=("Courier New", 14), background_color="black")],
                    ], visible=False, key="col4", justification="c", background_color="black"),
                ]
            ], background_color="black", font=("Courier New", 14, "underline"), border_width=0)],
        ], justification="c", background_color="black", visible=False, key="terminal")
    ],

          [sg.Column(
            [[sg.Text("Enter Password:", key="enter_password_text", visible=False, font=(DEFAULT_FONT,DEFAULT_FONT_SIZE))],
             [sg.Input(key="text_input", visible=False, font=("Courier New", 12), size=(20, 1)), sg.Button("Check Password", visible=False)],
             [sg.Multiline(key="output_box", size=(43, 8), visible=False, disabled=True, autoscroll=True, write_only=True, font=(DEFAULT_FONT,DEFAULT_FONT_SIZE))]],
            justification="c")],
        ]

window = sg.Window("Hacker", layout, size=(550, 800))

words_guessed = []

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "begin_game_button":
        words_guessed.clear()
        window["text_input"].update("")
        window["output_box"].update("")
        change_attempts(NUM_ATTEMPTS)
        if (len(values["seed_input"]) > 0):
            toggle_visiblility_lower("on")
            toggle_visiblility_upper("off")
            answer, word_array = find_words(values["difficulty_input"], values["seed_input"])
            print(answer)
            update_playfield(word_array)
        else:
            sg.PopupError("Invalid Seed!")
    elif event == "Check Password":
        guess = values["text_input"].lower()
        if guess == answer:
            toggle_visiblility_lower("off")
            sg.popup("HACK SUCCESSFUL\nPASSWORD: " + guess, background_color="black", text_color="green", font=(DEFAULT_FONT, 16))
            toggle_visiblility_upper("on")
            window["seed_input"].update(get_default_seed())
        elif guess in words_guessed:
            send_output("You already guessed " + guess)
            window["text_input"].update("")
        elif guess == "":
            send_output("No input found...")
        elif (consistant_hash(guess) == ADMIN_HASH):
            send_output("Welcome Admin:\nPassword is: " + answer)
            window["text_input"].update("")
        else:
            words_guessed.append(guess)
            change_attempts()
            if (len(guess) == len(answer)):
                score = score_guess(guess, answer)
                send_output("Incorrect Password - " + guess + " " + score)
            else:
                send_output("Incorrect Password Length - " + guess)
            window["text_input"].update("")

        if attempts == 0:
            toggle_visiblility_lower("off")
            sg.popup("HACK FAILED", background_color="black", text_color="red", font=(DEFAULT_FONT, 16))
            toggle_visiblility_upper("on")
            window["seed_input"].update(get_default_seed())
