from settings import SKIPABLE_MSG, MSG_PADDING


def print_message(msg: str):
    msg_len = len(msg) + MSG_PADDING
    formatted_msg = "\n" + "-" * msg_len + "\n"
    formatted_msg += msg.center(msg_len) + "\n"
    formatted_msg += "-" * msg_len + "\n"

    print(formatted_msg)


def prompt_input(prompt: str, data_type_name: str, checker, *, func=None, skipable=False):
    """
    This is a convenience function that guarentees that the
    return value satisfies the "checker()" function
    that has been passed in by repeatedly prompting user to input
    until it passes the check.

    Optional Argument:
    1. func : is a function that can be passed in to change
                  the input data before it is checked by the
                  "checker()" function

    2. skip: is a boolean flag that allows the user to not
               pass in anything to 'skip' this input process.
               This is meant to be used during updating, in which
               user might want some part of the data to remain
               unchanged.

    """

    prompt += SKIPABLE_MSG if skipable else ""

    while True:
        chosen = input(f"{prompt}")

        if skipable and chosen == "":
            return None

        if func != None:
            try:
                chosen = func(chosen)
            except Exception:
                print_message(f"'{chosen}' is not a valid {data_type_name}")
                continue

        if not checker(chosen):
            print_message(f"'{chosen}' is not a valid {data_type_name}")
            continue

        return chosen


def prompt_user_to_confirm(msg: str = ""):
    """
    This is a convenience function used to prompt user to confirm their decision during
    deleteing data or exiting the simulation.

    Optional Argument:
    1. msg: additional message that helps to clarify what the user is trying to do
    """
    return prompt_input(f"are you sure to {msg}? (Y/N): ", "response", lambda x: x in ["Y", "N"], func=str.upper) == "Y"


def read_database(filename: str, data_type):
    try:
        with open(filename, "r") as f:
            return [data_type(*line.split(",")) for line in f.read().split("\n")[:-1]]
    except FileNotFoundError:
        with open(filename, "w") as f:
            return []
