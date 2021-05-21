"""Code by Geir Anderson
   Based on the ELIZA system.
   The longer I use Python, the more I want to call it Camelot.
"""
"""
Needed:
[✓] Rand Responder
[✓] Single Keyword Responder
[✓] Pattern Responder w/ single or multiple adaptive sections
[✓] Pattern Matcher
[✓] Keyword Matcher
[✓] Quit Phrase

Optional:
[] Special Cases (i.e. greetings, certain user questions, etc.)
"""

#!/usr/bin/python3

import sys
import random

#=====================================================================================
#Some cleanup to wording
def cleanup(list_to_clean, is_user = False):
    return_list = []

    if is_user is False:
        for item in list_to_clean:
            if item == "i":
                return_list.append("you")

            elif item == "my":
                return_list.append("your")

            elif item == "myself":
                return_list.append("yourself")

            elif item == "am":
                return_list.append("are")

            else:
                return_list.append(item)

    else:
        for item in list_to_clean:
            if item == "i'm":
                return_list.append("i")
                return_list.append("am")

            elif item == "i've":
                return_list.append("i")
                return_list.append("have")

            elif item == "i'd":
                return_list.append("i")
                return_list.append("would")

            elif item == "i'll":
                return_list.append("i")
                return_list.append("will")

            else:
                return_list.append(item)

    if len(return_list) >= 1:
        return return_list

    return list_to_clean

#=====================================================================================
#Key loop
def keyword_loop(keyword_list, word):
    for keyword in keyword_list:
        if keyword == word:
            return keyword

        else:
            pass

    return None

#=====================================================================================
#Key match
def keyword_match (user_input_list, keyword_list):
    return_list = []

    for word in user_input_list:
        string = keyword_loop(keyword_list, word)

        if string is not None:
            return_list.append(string)

        else:
            pass

    if len(return_list) >= 1:
        return return_list

    else:
        return None

#=====================================================================================
#Pattern match
def pattern_match (user_input_list, pattern_list):
    replaced_strings = ["***"]

    count = 0
    another_count = 0

    bubble = []
    bubble_list = []

    return_pair = ()

    for pattern in pattern_list:
        count = 0
        another_count = 0

        if len(pattern) > len(user_input_list):
            pass

        else:
            while (another_count < len(pattern) and count < len(user_input_list)):
                if pattern[another_count] in replaced_strings:
                    if ((another_count + 1) < len(pattern) \
                            and pattern[another_count + 1] == user_input_list[count]):

                        b = " ".join(bubble)
                        bubble_list.append(b)
                        bubble[:] = []

                        another_count += 1

                    elif (another_count + 1 >= len(pattern) and count <= len(user_input_list)):

                        a = " ".join(user_input_list[count : len(user_input_list)])
                        bubble.append(a)

                        s = " ".join(bubble)
                        bubble_list.append(s)

                        another_count += 1

                    else:
                        bubble.append("".join(user_input_list[count]))
                        count += 1

                elif pattern[another_count] == user_input_list[count]:
                    count += 1
                    another_count += 1

                else:
                    bubble_list[:] = []
                    bubble[:] = []

                    count = len(user_input_list)
                    another_count = len(pattern)

            if bubble_list == []:
                pass

            elif (not return_pair or len(return_pair[1]) > len(bubble_list)):
                paired_bubble_list = []

                for item in bubble_list:
                    cleaning = cleanup(item.split())
                    cleaned = " ".join(cleaning)
                    paired_bubble_list.append(cleaned)

                return_pair = (pattern, paired_bubble_list)

    if not return_pair:
        return None

    else:
        return return_pair

#=====================================================================================
#Is done?
def is_done (user_input_list):
    s = " ".join(user_input_list)

    if s == "goodbye":
        return True

    return False

#=====================================================================================
#Random responder
def random_response (response_list):
        return random.choice(response_list)

#=====================================================================================
#Keyword responder
def keyword_response (user_input_list, keyword, response_list):
    relation_list = ["mother", "father", "son", "daughter", "brother", "sister", "friend", "husband", "wife", "girlfriend", "boyfriend", "s.o."]

    question_list = ["who", "what", "when", "where", "how"]

    response_piecer = []
    return_response = random.choice(response_list)

    response_piecer.append(" ".join(return_response))

    if keyword in relation_list:
        response_piecer.append("your")

    response_piecer.append(keyword)

    return_string = " ".join(response_piecer)

    if return_response[0] in question_list:
        return_string = return_string + '?'

    else:
        return_string = return_string + '.'

    return_string = return_string.capitalize()

    return return_string

#=====================================================================================
#Pattern responder
def pattern_response (user_input_list, pattern, response_dictionary):
    replaced_strings = ["***"]

    compare_string = " ".join(pattern[0])
    temp_list = []

    count = 0
    return_response = None

    return_list = []

    for item in pattern[1]:
        temp_list.append(item)

    for x, y in response_dictionary.items():
        if x == compare_string:
            return_response = y.split()
            break

    if not return_response:
        return None

    for word in return_response:
        if word in replaced_strings:
            return_list.append(temp_list[count])
            count += 1

        else:
            return_list.append(word)

    return_string = " ".join(return_list)
    return_string = return_string + '?'

    return return_string

#=====================================================================================
#Preprocessor
def preprocessor (passed_string):
    passed_list = []

    temp_string = passed_string.lower()
    passed_list = temp_string.split()

    return passed_list

#=====================================================================================
#Generate dictonary from file
def generate_dictionary (file_name):
    temp_file = open(file_name, 'r')
    return_dictionary = {}

    for line in temp_file:
        generator_list = line.split("|", maxsplit = 1)

        response = generator_list[1].rstrip()
        pattern = generator_list[0].rstrip()

        response = response.lstrip()
        pattern = pattern.lower()

        return_dictionary[pattern] = response

    temp_file.close()

    return return_dictionary

#=====================================================================================
#Generate list from file
def generate_list (file_name):
    temp_file = open(file_name, 'r')
    return_list = []

    for line in temp_file:
        generator_string = line.lower()
        return_list.append(generator_string.split())

    temp_file.close()

    return return_list

#=====================================================================================
#Convert list of list of strings into a list of strings w/ capitalized start letter (used for random responses)
def capitalize_joins (list):
    return_list = []

    for word in list:
        string = " ".join(word)
        return_list.append(string.capitalize())

    return return_list

#=====================================================================================
#Convert list of list of strings into a list of strings (used for keyword list)
def joins (list):
    return_list = []

    for word in list:
        string = " ".join(word)
        return_list.append(string)

    return return_list

#=====================================================================================
#Main function that connects to everything else
def main():
#Lists from txt files
    keyword_list = generate_list("kywrds.txt")
    keyword_responses = generate_list("kyrspns.txt")
    responses = generate_dictionary("rspns.txt")
    randoms = generate_list("rnds.txt")
    patterns = []
    for key in responses.keys():
        patterns.append(key.split())

    fixed_randoms = capitalize_joins(randoms)
    keyword_list = joins(keyword_list)

    print("Please, type as much as you want.\nWhen you are done, type \"goodbye\"(without the quotes).");
    print("==>>", end = ' ', flush = True)

#Receive, process and respond to inputs
    for line in sys.stdin:
        temp_line = preprocessor(line)
        preprocessed_line = cleanup(temp_line, True)

        if is_done(preprocessed_line) is False:
            matched_pattern = pattern_match(preprocessed_line, patterns)
            matched_keyword_list = keyword_match(preprocessed_line, keyword_list)

            if (matched_pattern is not None and matched_keyword_list is None):
                to_screen = pattern_response(preprocessed_line, matched_pattern, responses)

            elif (matched_keyword_list is not None):
                single_keyword = "".join(matched_keyword_list[0])
                to_screen = keyword_response(preprocessed_line, single_keyword, keyword_responses)

            else:
                to_screen = random_response(fixed_randoms)

            print(to_screen)
            print("==>>", end = ' ', flush = True)

        else:
            break

    print("Good day to you!")

#=====================================================================================

#Main call allows program to run properly
if __name__ is "__main__":
    main()
