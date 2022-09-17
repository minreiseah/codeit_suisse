# test_answers = ["VVIDH", "MZLPS", "BPCYN", "XYGGM"]
# test_attempts = ["JKGJB", "ZGRUJ", "XYGGM", "BPCYN", "MHXGE", "DZENT", "ZXWQW", "VVIDH", "MZLPS"]
# test_numbers = [761, 720, 13, 750, 936, 237, 482, 609, 585, 706, 240, 23, 76, 61, 700, 711, 823, 406, 376, 455, 818, 482, 338, 572, 257]

def letters_in_list(list_of_strings):
    # takes list of strings
    # returns list of the characters in the strings
    holder = []
    for thing in list_of_strings:
        holder.append(list(thing))
    letters_in_answers = set([char for item in holder for char in item])
    return letters_in_answers

def quordle(ans_list, attempt_list):
    answers = ans_list
    letters_in_ans = sorted(letters_in_list(answers))
    all_letters_guessed = sorted(letters_in_list(attempt_list))
    answer_dict = dict.fromkeys(all_letters_guessed, 0)

    for guess in attempt_list:
        unique_chars = set([guess[chr] for chr in range(0, len(guess))])
        if guess in answers:
            answers.remove(guess)
            letters_in_ans = sorted(letters_in_list(answers))
            # updates the letters

            for chr in unique_chars:
                if chr not in letters_in_ans and answer_dict[chr] == 0:
                    answer_dict[chr] += 1
        else:
            for chr in unique_chars:
                if chr not in letters_in_ans and answer_dict[chr] == 0:
                    answer_dict[chr] += 1
        for key in answer_dict:
            if answer_dict[key] > 0:
                answer_dict[key] += 1
    
    for key in answer_dict:
        answer_dict[key] -= 1
    # i added 1 to everything somehow above, so this fixes it lol

    answer_string = ''.join(str(item) for item in answer_dict.values())
    print(answer_string)

    return answer_string

def quordle2(ans_list, attempt_list, number_list):
    full_alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    guessed_letters = sorted(letters_in_list(attempt_list))
    quordle1_ans = quordle(ans_list, attempt_list)
    true_false_list = []
    for num in number_list:
        if str(num) in quordle1_ans:
            true_false_list.append("1")
        else:
            true_false_list.append("0")
    split_num_list = [true_false_list[0:5], true_false_list[5:10], true_false_list[10:15], true_false_list[15:20], true_false_list[20:25]]
    # turn an mf into binary
    
    letters = []
    for i in split_num_list:
        bin_value = int(''.join(i), 2)
        letters.append(chr(ord('@')+bin_value))
    # turn an mf into a letter

    remaining_letters = full_alphabet
    print(guessed_letters)
    for i in guessed_letters:
        if i in remaining_letters:
            remaining_letters.remove(i)
    # collect the unused letters
    
    for i in remaining_letters:
        letters.append(i)
    final_string = ''.join(i for i in letters)
    # put it together

    return final_string
