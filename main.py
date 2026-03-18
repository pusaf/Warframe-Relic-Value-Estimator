from estimator import *
from relic_validator import *
from formatter import *
import os


def main():
    print("\n")
    print("This tool is made to help you determine how much platinum your relic is worth.")
    print("It will return the expected platinum value of your relic based on current top sell orders on warframe.market.")
    print("To use, input your relic name when prompted. If you want to close the program, just type \"stop\"(not case sensitive).")
    print("The tool relies on having a list of all relics in the game currently and their status. If the game has been recently updated to add/modify relics, enter \"refresh\" to update the list.")
    print("\n")

    while True:
        if not os.path.isfile("relic_list.txt"):
            update_relic_list()

        user_input = input("Input relic name (stop to exit):  ")
        
        verified = verify_relic(user_input)
        if verified == False:
            if user_input.replace(" ","").lower() == "stop":
                break
            elif user_input.replace(" ","").lower() == "refresh":
                update_relic_list()
                print("Relic list has been updated.\n")
            else:
                print("Invalid input. Try again\n")
        elif verified == -1:
            update_relic_list()
            print("The relic list file either did not exist or was not in the right format. It has been updated for you.")
        else:
            print(build_string_format(verified[0], verified[1], expected_value(verified[0])))


if __name__ == '__main__':
    main()