from settings import *


def print_message(*msg: str, formatting=str.center):
    """
    This function is responsible for the pretty formatting of messages by
    adding borders and "pillars" for each line of messages

    This function takes in any number of strings, and prints each of them out
    line-by-line

    Optional Argument:
    1. formatting: This is a function, usually a built-in string function,
                   to allow for the messages to be formatted in different ways
    """
    max_msg_len = len(max(msg, key=lambda msg: len(msg)))
    msg_len = max_msg_len + MSG_PADDING

    formatted_msg = "\n" + "-" * (msg_len + PILLAR_LEN * 2) + "\n"
    if formatting is str.center:
        for m in msg:
            formatted_msg += PILLAR + formatting(m, msg_len) + PILLAR + "\n"
    elif formatting is str.ljust:
        for m in msg:
            # extra padding are given to avoid the text from sticking directly to the pillars
            half_len = MSG_PADDING // 2
            formatted_msg += PILLAR + " " * half_len + formatting(m, msg_len - half_len) + PILLAR + "\n"

    formatted_msg += "-" * (msg_len + PILLAR_LEN * 2) + "\n"
    print(formatted_msg)


def prompt_input(prompt: str, data_type_name: str, guide: str, checker, *, func=None, skipable=False):
    """
    This is a convenience function that guarentees that the
    return value satisfies the "checker()" function
    that has been passed in by repeatedly prompting user to input
    until it passes the check.
    The guide is a message that will guide the user to input the correct message
    if the user has inputted an invalid data

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
                print_message(f"'{chosen}' is not a valid {data_type_name}", "", guide)
                continue

        if not checker(chosen):
            print_message(f"'{chosen}' is not a valid {data_type_name}", "", guide)
            continue

        return chosen


def prompt_user_to_confirm(msg: str = "", ans: str = "Y"):
    """
    This is a convenience function used to prompt user to confirm their decision during
    deleteing data or exiting the simulation.

    Optional Argument:
    1. msg: additional message that helps to clarify what the user is trying to do
    """
    return (
        prompt_input(
            f"{msg} (Y/N): ",
            "response",
            "Please type in 'Y' for Yes or 'N' for No ",
            lambda x: x in ["Y", "N"],
            func=str.upper,
        )
        == ans.upper()
    )


def read_database(filename: str, data_type):
    try:
        with open(filename, "r") as f:
            return [data_type(*line.split(DELIMITER)) for line in f.read().split("\n")[:-1]]
    except FileNotFoundError:
        with open(filename, "w") as f:
            return []


def print_table(col_list: list[str], *row_list: list[str]):
    """
    This function is responsible to print out data in a table-like format.
    This function takes in a list of string that serves as its header. and a
    variable amount of list as its rows

    P.S: The Number of element in each row_list MUST match the col_list, or else
         "Data not found" would be displayed at its place.
    """
    no_col = len(col_list)
    no_vertical_line = no_col + 2
    col_len = INDEX_NUM_LEN + DATA_LEN * no_col + no_vertical_line

    print("-" * col_len)
    print(f"|{INDEX_NAME.center(INDEX_NUM_LEN)}|", end="")
    for col_name in col_list:
        print(f"{col_name.center(DATA_LEN)}|", end="")
    print(end="\n")
    print("-" * col_len)

    no_data_row = len(max(row_list, key=lambda x: len(x)))
    for i in range(no_data_row):
        print(f"|{(str(i+1) + '.').center(INDEX_NUM_LEN)}|", end="")

        try:
            for data_list in row_list:
                print(f"{data_list[i].center(DATA_LEN)}|", end="")
        except IndexError:
            print(f"{'data not found'.center(DATA_LEN)}", end="")

        print(end="\n")
    print("-" * col_len)
