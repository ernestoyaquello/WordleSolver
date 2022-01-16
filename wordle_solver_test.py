import wordle_data
import wordle_solver

expected_solution = ''

def test_wordle_solver():
    global expected_solution

    solutions = sorted(wordle_data.SOLUTIONS)
    solutions_solved = []
    solutions_not_solved = []

    for index, solution_to_test in enumerate(solutions):
        expected_solution = solution_to_test
        solution, guesses = wordle_solver.play_wordle(wordle_data.GUESSES_AND_SOLUTIONS, wordle_data.SOLUTIONS, get_result_input = get_result_input)
        if solution != None:
            solutions_solved.append((solution, guesses))
            print('🟩 Test ' + str(index + 1) + ' / ' + str(len(wordle_data.SOLUTIONS)) + ': "' + expected_solution.upper() + '" => ' + str(guesses))
        else:
            solutions_not_solved.append((solution, guesses))
            print('🟥 Test ' + str(index + 1) + ' / ' + str(len(wordle_data.SOLUTIONS)) + ': "' + expected_solution.upper() + '" => ' + str(guesses))

    return solutions_solved, solutions_not_solved

def get_result_input(guess, _):
    result_input = ''

    # Simulate the result input the user would type when using the solver to play the game
    counted_characters = []
    for position, guess_character in enumerate(list(guess)):
        if guess_character == expected_solution[position]:
            result_input += '2'
        elif guess_character in expected_solution and (expected_solution.count(guess_character) > counted_characters.count(guess_character)):
            result_input += '1'
            counted_characters.append(guess_character)
        else:
            result_input += '0'

    return result_input

solutions_solved, solutions_not_solved = test_wordle_solver()
print(
    '\nValid solutions found for ' + str(len(solutions_solved)) + ' out of ' + str(len(wordle_data.SOLUTIONS)) + ' cases' + \
    ' (' + str(round((len(solutions_solved) * 100.0) / len(wordle_data.SOLUTIONS), 2)) + '%)' + \
    ' with an average of ' + str(round(sum(len(guesses) for _, guesses in solutions_solved) / len(solutions_solved), 2)) + ' guesses per found solution.')