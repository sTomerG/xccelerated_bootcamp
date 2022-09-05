from roman_numeral_converter.roman_referals import (
    ROMAN_LETTER_LIST,
    ROMAN_NUMERAL_DICT,
)


def build_roman_numerals(
    n: int, roman_letter_S: str, roman_letter_M: str, roman_letter_L: str
) -> str:

    """returns roman numeral of a single digit

    Args:
        n (int): integer between 0-9
        roman_letter_S (str): smallest roman letter for that decimal position
        roman_letter_M (str): middle roman letter for that decimal position
        roman_letter_L (str): largest roman letter for that decimal position

    Returns:
        str: roman numeral of the inputted n
    """

    # e.g. return III
    if n <= 3:
        return n * roman_letter_S

    # e.g. return IV
    elif n == 4:
        return roman_letter_S + roman_letter_M

    # e.g. return VI
    elif n < 9:
        return roman_letter_M + (n % 5 * roman_letter_S)

    # e.g. return IX
    else:
        return roman_letter_S + roman_letter_L


def number_to_roman(n: int) -> str:
    """converts a number to a roman representation

    Args:
        n (int): any integer above 0

    Returns:
        str: roman representation of inputted integer
    """
    if n >= 4000 or n < 0:
        raise ValueError("integer must be >0 and <4000")

    roman_numeral = ""
    i = 0

    # loop through the reversed string representation of n
    # e.g. 1024 loop as: 4 2 0 1
    # roman letter lists will be:
    # 1: I V X
    # 0: X, L C
    # 2: C, D, M
    # 4: M, M, M
    for digit in str(n)[::-1]:
        output = build_roman_numerals(
            int(digit),
            ROMAN_LETTER_LIST[i],
            ROMAN_LETTER_LIST[i + 1],
            ROMAN_LETTER_LIST[i + 2],
        )
        roman_numeral = output + roman_numeral
        i += 2

    return roman_numeral


def roman_to_number(r: str) -> int:
    """converts a roman numeral to a number

    Args:
        r (str): a roman numeral

    Returns:
        int: a number representation of that roman numeral
    """

    for letter in set(list(r)):
        if letter not in ROMAN_LETTER_LIST:
            raise (ValueError(f"{letter} is not a valid Roman numeral"))

    number = 0
    for i, letter in enumerate(r):
        try:
            # if the current letter is >= next letter, add the value
            if ROMAN_NUMERAL_DICT[letter] >= ROMAN_NUMERAL_DICT[r[i + 1]]:
                number += ROMAN_NUMERAL_DICT[letter]
            # if the current letter is < next letter, substract the value
            else:
                number -= ROMAN_NUMERAL_DICT[letter]
        # if at the last letter an IndexError will be raised, so add the number
        except IndexError:
            number += ROMAN_NUMERAL_DICT[letter]

    return number
