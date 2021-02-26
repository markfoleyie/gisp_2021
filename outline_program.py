"""
Always start with a 'triple quote string'. This ends up in a special variable called '__doc__'. This should contain a
title, description of the program, its inputs and outputs and any other 'metadata' such as author, date, version etc.
"""

# All of the imports should be listed here. Do NOT ever do 'from xyv import *' as this could lead to namespace conflicts.
# If you import something from another module either use its full name - modulename.functionname - or else rename it -
# import ... as ...

from utilities.read_from_file_and_net import get_file_from_net as get_url

# Define any variables here. Note that the convention is that constants are upper-case with underscores

MY_URL = "https://markfoley.info/pa1/gettysburg.txt"

def main():
    """
    Always have a 'main' function. This gives you flexibility in that it's easy to test a program designed for import or
    to run it stand-alone.

    :return: You should describe what the function expects (inputs) and what it returns, if anything.
    """
    # pass # pass is just a placeholder - it does nothing but the function needs to have sonmething.

    the_speech = get_url(MY_URL)
    print(f"The 'Gettysburg Address' downloaded from the Net.\n\n{the_speech}")


if __name__ == '__main__':
    # Always use this construct. If you are running stand=alone, then this is your entry point. If not, then it won't
    # be run but you can still import from the program. Note that main takes no arguments and returns nothing.
    main()