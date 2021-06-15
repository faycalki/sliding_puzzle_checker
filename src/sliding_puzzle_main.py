# sys module to better organize the module directory

from Modules import license_input

#   Purpose and version of program
__purpose__ = "This sliding puzzle solver uses even and odd permutations (and their corresponding proofs) to deduce whether a puzzle is solvable, as well as the minimum lower boundary required amount of swaps needed in order to solve the puzzle."
__version__ = "Program Version: 1.0"

#   License and Author
__author__ = "Faycal Kilali"
__copyright__ = "Copyright (C) 2021 Faycal Kilali"
__license__ = "GNU GENERAL PUBLIC LICENSE"
__license_version__ = "3.0"

#   Display purpose and version, license and version of license.
print(__purpose__, "\n", __version__)
print(__copyright__, "\n", __license__, __license_version__, "\n")

# License disclaimer and extra details input
license_input.reveal_license_options()

import sliding_puzzle_impl

# For reference, image list 0 stands for "blank space" where we can slide the pieces. Ensure that no duplicates of any of the entries exist, and all entries must be positive integers, not negative. Furthermore, the number of entries must be a square number larger than 1.
debug = input("Input 1 if you wish to enable debug mode: ")
print(
    "If you have the following starting arrangement:\n1   2\n3 4 5\n6 7 8\n and you want to see if the following arrangement is possible:\n1 2 3\n  4 5\n6 7 8\nThen you'll need to plug in the starting arrangement as: 1, 0, 2, 3, 4, 5, 6, 7, 8\nand the desired arrangement as: 1, 2, 3, 0, 4, 5, 6, 7, 8.\nWhere 0 marks the empty space in the input of the arrangement. Keep in mind that this program supports ANY square arrangement, so go wild."
)


def invoke():

    reference = input("Starting puzzle arrangement: ")
    image = input("Desired puzzle arrangement: ")
    converted_reference, converted_image = sliding_puzzle_impl.convert_input(
        reference, image, debug
    )
    solution_function_pack, minimum_move = sliding_puzzle_impl.deduce_cycles(
        converted_reference, converted_image, debug
    )

    if solution_function_pack[0] == 1:
        if solution_function_pack[1] == 1:
            print(
                "A solution exists. The parity of permutation types required is odd and the desired arrangement is of an odd permutation.\nAt least %d swaps are required to perform the permutation."
                % solution_function_pack[2]
            )
        else:
            print(
                "A solution exists. The parity of permutation types required is even and the desired arrangement is of an even permutation.\nAt least %d swaps are required to perform the permutation."
                % solution_function_pack[2]
            )
    else:
        if solution_function_pack[1] == 1:
            print(
                "There is no solution to the desired arrangement. The parity of permutation types required is odd and the desired arrangement is of an even permutation."
            )
        else:
            print(
                "There is no solution to the desired arrangement. The parity of permutation types required is even and the desired arrangement is of an odd permutation."
            )
    invoke()


invoke()
