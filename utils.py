from settings import *


def print_message(*msg: str, formatting=str.center):
    max_msg_len = len(max(msg, key=lambda msg: len(msg)))
    msg_len = max_msg_len + MSG_PADDING

    formatted_msg = "\n" + "-" * (msg_len + PILLAR_LEN * 2) + "\n"
    if formatting is str.center:
        for m in msg:
            formatted_msg += PILLAR + formatting(m, msg_len) + PILLAR + "\n"
    else:
        for m in msg:
            half_len = MSG_PADDING // 2
            formatted_msg += PILLAR + " " * half_len + formatting(m, msg_len - half_len) + PILLAR + "\n"

    formatted_msg += "-" * (msg_len + PILLAR_LEN * 2) + "\n"
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


def prompt_user_to_confirm(msg: str = "", ans: str = "Y"):
    """
    This is a convenience function used to prompt user to confirm their decision during
    deleteing data or exiting the simulation.

    Optional Argument:
    1. msg: additional message that helps to clarify what the user is trying to do
    """
    return prompt_input(f"{msg} (Y/N): ", "response", lambda x: x in ["Y", "N"], func=str.upper) == ans.upper()


def read_database(filename: str, data_type):
    try:
        with open(filename, "r") as f:
            return [data_type(*line.split(",")) for line in f.read().split("\n")[:-1]]
    except FileNotFoundError:
        with open(filename, "w") as f:
            return []


def print_table(col_list: list[str], *row_list: list[str]):
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
