import wordle_solver
import re

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
GREEN = '\033[92m'
YELOW = '\033[93m'
ENDC = '\033[0m'

def prompt_user_for_guess_result(guess, row):
    result_input = ''

    input('\nTry with ' + BOLD + UNDERLINE + guess.upper() + ENDC + " and press ENTER when you are done.")

    if row == 0:
        print('\nNow, type your result here formatted as ' + get_formatted_guess('01201', '01201') + ', where each digit represents:')
        print('  ' + get_formatted_guess('0', '0') + ': The letter is not in the word in any spot 😞')
        print('  ' + get_formatted_guess('1', '1') + ': The letter is in the word, but in a different spot 😐')
        print('  ' + get_formatted_guess('2', '2') + ': The letter is in the word in the correct spot 😀')
        print('For example, if your output was ' + get_formatted_guess('20210', guess.upper()) + ', then type ' + get_formatted_guess('20210', '20210') + '.\n')

    result_input = input('Type your result: ').strip()
    while not bool(re.match('[012]{5}', result_input)):
        print(result_input + ' is not a valid result. Please follow the format ' + get_formatted_guess('20210', '20210') + ' explained in the instructions.')
        result_input = input('Type your result: ').strip()

    return result_input


def get_formatted_guess(result_input, guess):
    formatted_input = ''

    for index, input_character in enumerate(list(result_input)):
        if input_character == '0':
            formatted_input += BOLD + guess[index] + ENDC
        elif input_character == '1':
            formatted_input += BOLD + YELOW + guess[index] + ENDC
        elif input_character == '2':
            formatted_input += BOLD + GREEN + guess[index] + ENDC

    return formatted_input

def create_solution_chart(solution, guesses):
    chart = ''

    for guess in guesses:
        for position, guess_character in enumerate(list(guess)):
            if solution[position] == guess_character:
                chart += '🟩'
            elif guess_character in solution:
                chart += '🟨'
            else:
                chart += '⬛'
        chart += '\n'

    return chart

solution, guesses = wordle_solver.play_wordle(prompt_user_for_guess_result)
if (solution != None):
    print('\nCongratulations on your win! 🎉')
    print('\nHere is your chart:')
    print('\n' + create_solution_chart(solution, guesses))
else:
    print('\nIt seems like we couldn\'t crack it today 😞. Best luck next time! 🤞')