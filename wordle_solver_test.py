import wordle_data
import wordle_solver

expected_solution = ''

def test_solutions(solutions):
    global expected_solution

    solutions_found = []
    solutions_not_found = []

    for index, solution_to_test in enumerate(solutions):
        expected_solution = solution_to_test
        solution, guesses = wordle_solver.play_wordle(get_result_input = get_result_input)
        if solution != None:
            solutions_found.append((solution, guesses))
            print('🟩 Test ' + str(index + 1) + ' / ' + str(len(solutions)) + ': "' + expected_solution.upper() + '" => ' + str(guesses))
        else:
            solutions_not_found.append((solution, guesses))
            print('🟥 Test ' + str(index + 1) + ' / ' + str(len(solutions)) + ': "' + expected_solution.upper() + '" => ' + str(guesses))

    return solutions_found, solutions_not_found

def get_result_input(guess, _):
    result_input = ''

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

solutions_found, solutions_not_found = test_solutions(wordle_data.solutions)
print(
    '\nValid solutions found for ' + str(len(solutions_found)) + ' out of ' + str(len(wordle_data.solutions)) + ' cases' + \
    ' (' + str(round((len(solutions_found) * 100.0) / len(wordle_data.solutions), 2)) + '%)' + \
    ' with an average of ' + str(round(sum(len(guesses) for _, guesses in solutions_found) / len(solutions_found), 2)) + ' guesses per found solution.')