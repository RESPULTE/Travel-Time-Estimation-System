from settings import *


def print_message(*msg: str, formatting=True):
    """
    This function is responsible for the pretty formatting of messages by
    adding borders and "pillars" for each line of messages

    This function takes in any number of strings due to the "*"
    symbol specified at the argument, and prints each of them out
    line-by-line

    Optional Argument:
    1. formatting: This is a function, usually a built-in string function,
                   to allow for the messages to be formatted in different ways
    """
    max_msg_len = len(max(msg, key=lambda msg: len(msg)))
    msg_len = max_msg_len + MSG_PADDING

    formatted_msg = "\n" + "-" * (msg_len + VERTICAL_BORDER_LEN * 2) + "\n"
    if formatting:
        for m in msg:
            formatted_msg += VERTICAL_BORDER + str.center(m, msg_len) + VERTICAL_BORDER + "\n"
    else:
        half_len = MSG_PADDING // 2
        for m in msg:
            # extra padding are given to avoid the text from sticking directly to the pillars
            formatted_msg += (
                VERTICAL_BORDER + " " * half_len + str.ljust(m, msg_len - half_len) + VERTICAL_BORDER + "\n"
            )

    formatted_msg += "-" * (msg_len + VERTICAL_BORDER_LEN * 2) + "\n"
    print(formatted_msg)


def print_table(col_list: list, *row_list: list):
    """
    This function is responsible to print out data in a table-like format.

    This function takes in a list of string that serves as its header. and a
    variable amount of list as its rows due to the "*" symbol specified at the
    argument

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

        for data_list in row_list:
            print(f"{data_list[i].center(DATA_LEN)}|", end="")

        print(end="\n")
    print("-" * col_len)


def prompt_input(prompt: str, data_type_name: str, guide_msg: str, checker, *, func=None, skipable=False):
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

    2. skipable: is a boolean flag that allows the user to not
               pass in anything to 'skip' this input process.
               This is meant to be used during updating, in which
               user might want some part of the data to remain
               unchanged.

    """

    prompt += SKIPABLE_MSG if skipable else ""

    while True:
        chosen = input(f"{prompt}")

        # an additional variable is used here, as the data inputted
        # might be altered by "func()", which can be hard to
        # understand for users when an error occurs
        to_return = chosen

        if skipable and chosen == "":
            return None

        if func != None:
            try:
                to_return = func(chosen)
            except Exception:
                # This will be executed if ANY error occurs when trying to convert the data inputted by the user
                print_message(f"'{chosen}' is not a valid {data_type_name}", "", guide_msg)

                # "Continue" resets the loop to the very beginning, skipping all the code below this keyword
                continue

        # If the data inputted by the user does not pass the requirement
        if not checker(to_return):
            print_message(f"'{chosen}' is not a valid {data_type_name}", "", guide_msg)
            continue

        return to_return


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
