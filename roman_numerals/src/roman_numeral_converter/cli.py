import click

from roman_numeral_converter.converters import number_to_roman, roman_to_number


@click.command()
@click.argument("value")
def convert(value):
    try:
        # if value is a float, raise Error
        if isinstance(value, float):
            raise ValueError("Please insert roman numeral or integer")
        value = int(value)

    # if value can't be converted to integer, try to convert to string
    except ValueError:
        try:
            value = str(value)
        except TypeError:
            raise TypeError("Please insert roman numeral or integer")
        else:
            print(roman_to_number(value))

    # if value is an integer, convert number to roman
    else:
        print(number_to_roman(value))


if __name__ == "__main__":
    convert()
