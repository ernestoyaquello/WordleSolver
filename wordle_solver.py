import wordle_data
import re
from collections import defaultdict

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
GREEN = '\033[92m'
YELOW = '\033[93m'
ENDC = '\033[0m'

def find_solution():
    solution = None
    guesses = []

    # Calculate the number of occurrences of each letter in all the possible solutions so we can later give each potential guess a score
    solutions_letter_count = defaultdict(int)
    for candidate_solution in wordle_data.solutions:
        for position, letter in enumerate(list(candidate_solution)):
            solutions_letter_count[letter] += 1
            solutions_letter_count[(letter, str(position))] += 1

    # Row after row, calculate the next best guess and ask the user to use it in the game
    discarded_letters = []
    letters_in_wrong_positions = defaultdict(str)
    letters_in_right_positions = defaultdict(str)
    row = 0
    while solution == None and row < 6:
        best_guess = calculate_best_guess(solutions_letter_count, discarded_letters, letters_in_wrong_positions, letters_in_right_positions)

        if best_guess != None:
            guesses.append(best_guess)
            result_input = prompt_user_for_guess_result(best_guess, show_instructions = row == 0)
            if result_input == '22222':
                # The game is solved!
                solution = best_guess
            else:
                # Parse the input result given by the user so we can calculate the next best guess
                for position, result_input_character in enumerate(list(result_input)):
                    letter_in_guess = best_guess[position]
                    if result_input_character == '0':
                        discarded_letters.append(letter_in_guess)
                    elif result_input_character == '1':
                        letters_in_wrong_positions[position] = letter_in_guess
                    elif result_input_character == '2':
                        letters_in_right_positions[position] = letter_in_guess
            row += 1
        else:
            # This should never happen, but for some reason, it was impossible to find a valid guess?
            print('\nIt seems like there are no possible guesses, which shouldn\'t be possible! Are you sure you typed your results correctly? 🤔')
            break

    return solution, guesses

def calculate_best_guess(solutions_letter_count, discarded_letters, letters_in_wrong_positions, letters_in_right_positions):
    best_guess = None

    # Calculate the best possible valid guess
    best_guess_score = 0
    for guess in set(wordle_data.guesses + wordle_data.solutions):
        if is_guess_valid(guess, discarded_letters, letters_in_wrong_positions, letters_in_right_positions):
            guess_score = calculate_guess_score(guess, solutions_letter_count)
            if guess_score > best_guess_score or (guess_score == best_guess_score and guess in wordle_data.solutions):
                best_guess = guess
                best_guess_score = guess_score

    return best_guess

def is_guess_valid(guess, discarded_letters, letters_in_wrong_positions, letters_in_right_positions):
    # The letters that have been detected in wrong positions must be present in the guess for it to be valid
    expected_letters = set(filter(lambda l: l != '', letters_in_wrong_positions.values()))
    expected_letters_min_occurrences = { expected_letter: list(letters_in_wrong_positions.values()).count(expected_letter) for expected_letter in expected_letters }
    if any(guess.count(expected_letter) < expected_letters_min_occurrences[expected_letter] for expected_letter in expected_letters):
        return False

    # Iterate over each letter to discard the ones that are not present in the solution and the ones that are in positions we know to be invalid
    for position, letter in enumerate(guess):
        if letter in discarded_letters or \
            (letters_in_right_positions[position] != '' and letters_in_right_positions[position] != letter) or \
            (letters_in_wrong_positions[position] != '' and letters_in_wrong_positions[position] == letter):
            return False

    return True

def calculate_guess_score(guess, solutions_letter_count):
    guess_score = 0

    counted_letters = []
    for position, letter in enumerate(guess):
        # Calculate a score for the guess taking into account the importance of each letter and its position
        guess_score += solutions_letter_count[letter] if letter not in counted_letters else 0
        guess_score += solutions_letter_count[(letter, str(position))]

        # Keep track of the counted letters to avoid giving guesses extra score points for repeated letters
        counted_letters.append(letter)

    return guess_score

def prompt_user_for_guess_result(guess, show_instructions):
    result_input = ''

    input('\nTry with ' + BOLD + UNDERLINE + guess.upper() + ENDC + " and press ENTER when you are done.")

    if show_instructions:
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

solution, guesses = find_solution()
if (solution != None):
    print('\nCongratulations on your win! 🎉')
    print('\nHere is your chart:')
    print('\n' + create_solution_chart(solution, guesses))
else:
    print('\nIt seems like we couldn\'t crack it today 😞. Best luck next time! 🤞')