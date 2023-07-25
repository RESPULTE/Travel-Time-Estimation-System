def prompt_input(prompt: str, checker, *, func=None, skip=False):
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
    while True:
        chosen = input(prompt)

        if skip and chosen == "":
            return None

        if func != None:
            try:
                chosen = func(chosen)
            except Exception:
                print(f"'{chosen}' is not a valid \n")
                continue

        if not checker(chosen):
            print(f"'{chosen}' is not a valid \n")
            continue

        return chosen


def prompt_user_to_confirm(msg: str = ""):
    """
    This is a convenience function used to prompt user to confirm their decision during
    deleteing data or exiting the simulation.

    Optional Argument:
    1. msg: additional message that helps to clarify what the user is trying to do
    """
    return prompt_input(f"are you sure to {msg}? (Y/N): ", lambda x: x in ["Y", "N"], func=str.upper) == "Y"
