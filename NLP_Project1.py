# Project 1 by Andrew Henkel for CS 631V

import re
from collections import Counter
from string import ascii_lowercase

# Part 1


def delete_char(word):
    all_possible = []

    for index in range(len(word)):
        result = word[:index] + word[index + 1 :]
        all_possible.append(result)

    return all_possible


def switch_char(word):
    all_possible = []

    for index in range(1, len(word)):
        to_switch = word[index] + word[index - 1]
        result = word[: index - 1] + to_switch + word[index + 1 :]
        all_possible.append(result)

    return all_possible


def replace_char(word):
    all_possible = []
    word = word.lower()

    for index in range(len(word)):
        for letter in ascii_lowercase:
            result = word[:index] + letter + word[index + 1 :]
            if result != word:
                all_possible.append(result)

    return all_possible


def insert_char(word):
    all_possible = []
    word = word.lower()

    for index in range(len(word) + 1):
        for letter in ascii_lowercase:
            result = word[:index] + letter + word[index:]
            all_possible.append(result)

    return all_possible


# Edit 2


def edit_distance_one(word, allow_switches=True):
    result = set(delete_char(word)).union(replace_char(word)).union(insert_char(word))

    if allow_switches:
        result.update(switch_char(word))

    return result


def edit_distance_two(word, allow_switches=True):
    first_pass = edit_distance_one(word, allow_switches)
    second_pass = set()

    for s in first_pass:
        second_pass.update(edit_distance_one(s, allow_switches))

    return second_pass


# Part 3


def your_read_function():
    with open("shakespeare.txt") as vocabulary_file:
        return [
            word.group().lower() for word in re.finditer(r"\w+", vocabulary_file.read())
        ]


def fix_edits(word, n):
    word = word.lower()
    vocab = your_read_function()
    vocab_counter = Counter(your_read_function())

    if word in vocab_counter:
        suggestions = {word}

    elif one_edit_suggestions := edit_distance_one(word).intersection(vocab_counter):
        suggestions = one_edit_suggestions

    elif two_edit_suggestions := edit_distance_two(word).intersection(vocab_counter):
        suggestions = two_edit_suggestions

    else:
        suggestions = {word}

    # Sorts by frequency in descending order.
    return sorted(
        (
            (suggestion, vocab_counter[suggestion] / len(vocab))
            for suggestion in suggestions
        ),
        key=lambda x: x[1],
        reverse=True,
    )[:n]


def fix_edits_and_print(word, n):
    fixed = fix_edits(word, n)

    print(f"entered word = {word}")
    print(
        "suggestions = {"
        + ", ".join(f"'{suggestion}'" for suggestion, _ in fixed)
        + "}"
    )

    for index, (suggestion, frequency) in enumerate(fixed):
        print(f"word {index}: {suggestion}, probability {frequency:0.6f}")
