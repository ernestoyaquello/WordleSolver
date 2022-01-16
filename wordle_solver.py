from collections import defaultdict

cached_solutions_letter_count = None

def play_wordle(candidate_guesses, candidate_solutions, get_result_input):
    global cached_solutions_letter_count

    solution = None
    guesses = []

    # Calculate the number of occurrences of each letter in all the possible solutions so we can later give each potential guess a score
    solutions_letter_count = cached_solutions_letter_count
    if solutions_letter_count == None:
        solutions_letter_count = defaultdict(int)
        for candidate_solution in candidate_solutions:
            for position, letter in enumerate(list(candidate_solution)):
                solutions_letter_count[letter] += 1
                solutions_letter_count[(letter, str(position))] += 1
        cached_solutions_letter_count = solutions_letter_count

    # Row after row, calculate the next best guess and then iterate after getting the result formated as 01201
    discarded_letters = []
    letters_in_wrong_positions = defaultdict(str)
    letters_in_right_positions = defaultdict(str)
    row = 0
    while solution == None and row < 6:
        best_guess, candidate_guesses = calculate_best_guess(candidate_guesses, candidate_solutions, solutions_letter_count, discarded_letters, letters_in_wrong_positions, letters_in_right_positions)

        if best_guess != None:
            guesses.append(best_guess.upper())
            result_input = get_result_input(best_guess, row)
            if result_input == '22222':
                # The game is solved!
                solution = best_guess.upper()
            else:
                # Parse the input result so we can calculate the next best guess
                for position, result_input_character in enumerate(list(result_input)):
                    letter_in_guess = best_guess[position]
                    if result_input_character == '0':
                        letters_in_right_positions[position] = ''
                        letters_in_wrong_positions[position] = ''
                        if letter_in_guess not in letters_in_right_positions.values() and letter_in_guess not in letters_in_wrong_positions.values():
                            discarded_letters.append(letter_in_guess)
                    else:
                        letters_in_right_positions[position] = letter_in_guess if result_input_character == '2' else ''
                        letters_in_wrong_positions[position] = letter_in_guess if result_input_character == '1' else ''
                        if letter_in_guess in discarded_letters:
                            discarded_letters.remove(letter_in_guess)
            row += 1
        else:
            # This should never happen, but for some reason, it was impossible to find a valid guess?
            print('\nIt seems like there are no possible guesses, which shouldn\'t be possible! Are you sure you typed your results correctly? 🤔')
            break

    return solution, guesses

def calculate_best_guess(candidate_guesses, candidate_solutions, solutions_letter_count, discarded_letters, letters_in_wrong_positions, letters_in_right_positions):
    best_guess = None
    updated_candidate_guesses = []

    # Calculate the best possible valid guess
    best_guess_score = -1
    for guess in candidate_guesses:
        if is_guess_valid(guess, discarded_letters, letters_in_wrong_positions, letters_in_right_positions):
            updated_candidate_guesses.append(guess)
            guess_score = calculate_guess_score(guess, solutions_letter_count)
            if guess_score > best_guess_score or (guess_score == best_guess_score and guess in candidate_solutions):
                best_guess = guess
                best_guess_score = guess_score

    # Along with the guess, we also return the updated (i.e., reduced) list of valid candidate guesses so there are less ones to iterate over on the next attempt
    return best_guess, updated_candidate_guesses

def is_guess_valid(guess, discarded_letters, letters_in_wrong_positions, letters_in_right_positions):
    # Iterate over each letter to discard the ones that are not present in the solution and the ones that are in positions we know to be invalid
    for position, letter in enumerate(guess):
        if letter in discarded_letters or \
            (letters_in_right_positions[position] != '' and letters_in_right_positions[position] != letter) or \
            (letters_in_wrong_positions[position] != '' and letters_in_wrong_positions[position] == letter):
            return False

    # In addition, the letters that have been detected in wrong positions must be present in the guess for it to be valid
    expected_letters = set(filter(lambda l: l != '', letters_in_wrong_positions.values()))
    expected_letters_min_occurrences = { expected_letter: list(letters_in_wrong_positions.values()).count(expected_letter) for expected_letter in expected_letters }
    if any(guess.count(expected_letter) < expected_letters_min_occurrences[expected_letter] for expected_letter in expected_letters):
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