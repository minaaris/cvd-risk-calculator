"""
input_handler.py 

Process user input
"""

__author__ = "MINERVA VALENTINE"


def input_int(prompt: str, lower: int, upper: int) -> int:
    """
    Ask the user to enter an integer within a given range, read their response, 
    and continue asking them and reading their response until it is within that range.
    Parameters:
    prompt: str, the message to prompt the user with
    lower: int, the lower bound of the allowed range
    upper: int, the upper bound of the allowed range
    Returns:
    int, the valid value entered by the user
    """

    # prompt the user to input a value, store the value as integer
    value = None
    while value is None:
        try:
            value: int = int(input(f"{prompt}({lower}-{upper})"))
            break
        except ValueError:
            print("Please enter a valid number")
            pass

    # check if value is within range
    while value < lower or value > upper:
        # display out of range message
        print('Value out of range')
        # prompt the user to input a value, store the value as integer
        value: int = int(input(f"{prompt}({lower}-{upper})"))

    return value


def input_float(prompt: str, lower: float, upper: float) -> float:
    """
    Ask the user to enter a float within a given range, read their response, 
    and continue asking them and reading their response until it is within that range.
    Parameters:
    prompt: str, the message to prompt the user with
    lower: float, the lower bound of the allowed range
    upper: float, the upper bound of the allowed range
    Returns:
    float, the valid value entered by the user
    """

    # prompt the user to input a value, store the value as float
    while True:
        try:
            value: float = float(input(f"{prompt}({lower}-{upper})"))
            break
        except ValueError:
            print("Please enter a valid number")
            pass

    # check if value is within range
    while value < lower or value > upper:
        # display out of range message
        print('Value out of range')
        # prompt the user to input a value, store the value as float
        value: float = float(input(f"{prompt}({lower}-{upper})"))

    return value


def input_bool(prompt: str) -> bool:
    """
    Ask the user to enter a yes/no value, read their response,
    and continue asking them and reading their response until it is valid.
    Parameters:
    prompt: str, the message to prompt the user with
    Returns:
    bool, the valid value correspond to the user input
    True, if the user input is yes
    False, if the user input is no
    """

    # prompt the user to input a value, store the value as a lower case string
    value: str = str(input(f"{prompt}(yes/no)")).lower()

    # check if the input is valid or not
    while value not in ["yes","y","true","no","n","false"]:
        # display invalid input message
        print("invalid input, please enter yes or no")
        # prompt the user to input a value, store the value as a lower case string
        value: str = str(input(f"{prompt}(yes/no)")).lower()

    # check if the user input is yes or no
    if value in ["yes","y","true"]:
        #return True if user input is yes
        return True
    elif value in ["no","n","false"]:
        #return False if user input is no
        return False


def input_menu(prompt: str, options: list[str]) -> int:
    """Display a numbered menu of options, prompt the user for their choice,
    and validate that the choice falls within the available range.

    Parameters:
        prompt: str, the message to display before the options.
        options: list[str], the text descriptions of the menu options.

    Returns:
        int, the validated index choice chosen by the user (1-indexed).
    """
    print(f"\n--- {prompt} ---")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    # Reuse input_int to strictly validate user input
    return input_int("Select an option: ", 1, len(options))


if __name__ == "__main__":
    #All variables are initialised so code will run without error before all functions are implemented and called
    stars = -1     #user's star (between 0 and 5)
    volume = -1.0  #continuously variable speaker volume (as a value between 0 and 11)
    again = False  #do they want to try some action again?
    options = ["Start", "Resume", "Quit"]

    print("Test 1 Testing input_int... the number should be saved in stars.")
    print(" - Enter '6' (should loop with error)")
    print(" - Enter '-1' (should loop with error")
    print(" - Enter '2' and it should work")
    stars = input_int("Rate the last movie you saw", 0, 5)
    print(f"Star rating: {stars}");
    print()

    print("Test 2 Testing input_float... the number should be saved in volume.")
    print(" - Enter '20' (should loop with error)")
    print(" - Enter '-1' (should loop with error)")
    print(" - Enter '9.5' and it should work")
    volume = input_float("Enter amplifier volume", 0.0, 11.0)
    print(f"Volume: {volume}")
    print()

    print("Testing input_bool... the result is saved in again.")
    print(" - Extend these boolean tests by adding more messages to verify your solution!")
    print(" - Enter 'nah' and it should loop with error")
    print(" - Enter 'yes' and it should succeed")
    again = input_bool("Try again?")
    print(f"Again: {again}")
    print()
    print(" - Verify that it can also read in False...")
    again = input_bool("Try again?")
    print(f"Again: {again}")
    print()

    print("Testing input menu")
    print("Enter something from the option list and it should work")
    choice = input_menu("Select", options)
    print(f"Choice: {choice}")
    print("Enter something that is not in the option list and it should return an error")
    choice = input_menu("Select", options)
    
    print("Tests complete...")
