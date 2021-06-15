# This program is developed by Faycal Kilai, initial version at 15-june-2021. The license is provided in a separate file in the main directory.


def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def error_function(l):
    if l == -1:
        print("Error -1: Reference and Image arrays are not of the same size")
        return -1
    elif l == -2:
        print("Error -2: Reference Array or Image Arrays are not squares")
        return -2
    elif l == -3:
        print("Error -3: Reference Array or Image Array is not larger than 1.")
        return -3
    elif l == -4:
        print("Error -4: Duplicate elements exist, make sure each element is unique.")
        return -4
    elif l == -5:
        print(
            "Error -5: Blank space is missing, make sure that the blank space is labelled 0 in your input."
        )
        return -5
    elif l == -6:
        print(
            "The reference and image sets have different symbols. They must have the same symbols, but can be in different arrangement."
        )
        return -6


# Called directly. Arguments are reference (the starting sliding puzzle arrangement from row 1 to row n encompassing column 1 to column n. Only acceptable for square sliding puzzles), image (the desired result of the sliding puzzle, same conditions as earlier but you choose how you want to check if solvable), debug (enable or disable debug messages)
# Returns converted reference and converted image.
def convert_input(reference, image, debug):
    if len(reference) > 1 and len(image) > 1:
        reference = reference.split(",")  # Split at each comma
        reference = list(map(int, reference))  # Map the string to integer
        image = image.split(",")  # Split at each comma
        image = list(map(int, image))  # Map the string to integer
    else:
        error_function(-3)
    if not len(reference) == len(image):
        error_function(-1)
    elif (0 not in reference) or (0 not in image):
        error_function(-5)
    elif (not len(reference) == len(set(reference))) or (
        not len(image) == len(set(image))
    ):
        error_function(-4)
    elif not set(reference) == set(image):
        error_function(-6)
    else:
        if len(reference) == isqrt(len(reference)) * isqrt(len(reference)):
            if debug == 1:
                print(
                    "Converted input of reference to %s and image to %s"
                    % (reference, image)
                )
            return reference, image
        else:
            error_function(-2)


# Called directly (as long as using the same list form as that of convert_input function). Arguments are S_reference (reference of same form as that outputted by convert_input), S_image (image of same form as that outputted by convert_input), debug (argument to enable or disable debug mode)
# Returns find_solutions, minimum_moves.
def deduce_cycles(reference, image, debug):
    n = isqrt(len(reference))
    k = isqrt(len(image))
    list_of_all_cycles = []
    minimum_moves = 0
    if len(reference) == n * n and len(image) == k * k:
        S_copy = reference.copy()
        M_copy = image.copy()
        # Good up to this point
        while not len(S_copy) == 0:
            cycle = []
            cycle.append(S_copy[0])
            if S_copy[0] == M_copy[0]:
                del S_copy[0]
                del M_copy[0]
                list_of_all_cycles.append(cycle)
            else:
                x = M_copy[0]
                while S_copy[0] != x and S_copy[0] != None:
                    cycle.append(x)
                    mapped_from = S_copy.index(x)
                    mapped_to = M_copy[mapped_from]
                    x = mapped_to
                for i in range(0, len(cycle)):
                    S_copy.remove(cycle[i])
                    M_copy.remove(cycle[i])
                list_of_all_cycles.append(cycle)

        # The code below currently finds the number of swaps done for every cycle that is larger than size 1. It doesn't give us the exact number of swaps, but it does give us an excellent lower boundary. Note this is only relevant when a solution actually exists.
        for i in range(0, len(list_of_all_cycles)):
            if len(list_of_all_cycles[i]) > 1:
                minimum_moves += len(list_of_all_cycles[i])
            else:
                pass
                minimum_moves += len(
                    list_of_all_cycles[i]
                )  # Temporary solution to remove counting the blank space from its corresponding cycle as an additional swap to itself.
                # Returns whether the solution is possible, the parity of permutation type required for a solution to be possible, the permutation type of the image as a tuple. Furthermore, returns the minimum moves required in order to solve the puzzle (which is only relevant when its solvable).
        return (
            find_solutions(reference, image, list_of_all_cycles, debug),
            minimum_moves,
        )
    else:
        return -2


# Called by deduce_cycles. Arguments are reference, image, list_of_all_cycles (number of not 1-cycles in the permutation of the image), debug (argument to enable or disable debug mode)
def find_solutions(reference, image, list_of_all_cycles, debug):
    # Create rectangular arrays from those lists
    n = int(isqrt(len(reference)))
    reference_rectangular = [
        reference[i * n : (i + 1) * n] for i in range((len(reference) + n - 1) // n)
    ]

    k = int(isqrt(len(image)))
    image_rectangular = [
        image[i * k : (i + 1) * k] for i in range((len(image) + k - 1) // k)
    ]

    # Deduce whether the image is an even or odd permutation
    num_even_cycles = 0

    for i in range(0, len(list_of_all_cycles)):
        if len(list_of_all_cycles[i]) % 2 == 0:
            num_even_cycles += 1
        else:
            pass

    if num_even_cycles % 2 == 0:
        image_permutation_type = 0  # Even permutation
    else:
        image_permutation_type = 1  # Odd permutation

    # Find blank space coordinate of reference
    naive_count = 0
    while naive_count < len(reference_rectangular):
        list_position = 0 in reference_rectangular[naive_count]
        if list_position == True:
            reference_inner_list_element_row_position = (
                naive_count  # Starting the count from 0, so we offset by 1
            ) + 1
            reference_inner_list_element_column_position = (
                reference_rectangular[naive_count].index(0) + 1
            )  # Addition of 1 to offset starting from position 0

            naive_count = len(reference_rectangular)
        else:
            naive_count += 1

    # Find blank space coordinate of image
    naive_count = 0
    while naive_count < len(image_rectangular):
        list_position = 0 in image_rectangular[naive_count]
        if list_position == True:
            image_inner_list_element_row_position = (
                naive_count  # Starting the count from 0, so we offset by 1
            ) + 1
            image_inner_list_element_column_position = (
                image_rectangular[naive_count].index(0) + 1
            )  # Addition of 1 to offset starting from position 0

            naive_count = len(image_rectangular)
        else:
            naive_count += 1

    # Find the difference between the two blank spaces, if the difference is even then the image permutation needs to be even, otherwise it needs to be odd for a solution to exist.

    if (
        reference_inner_list_element_row_position
        >= image_inner_list_element_row_position
    ):
        row_difference = (
            reference_inner_list_element_row_position
            - image_inner_list_element_row_position
        )
    else:
        row_difference = (
            image_inner_list_element_row_position
            - reference_inner_list_element_row_position
        )
    if (
        reference_inner_list_element_column_position
        >= image_inner_list_element_column_position
    ):
        column_difference = (
            reference_inner_list_element_column_position
            - image_inner_list_element_column_position
        )
    else:
        column_difference = (
            image_inner_list_element_column_position
            - reference_inner_list_element_column_position
        )

    # Sum the differences as per the constraint laid above.

    num_of_blank_space_swaps = row_difference + column_difference
    if num_of_blank_space_swaps % 2 == 0:
        permutation_type_required = 0  # even permutation required
    else:
        permutation_type_required = 1  # odd permutation required

    # If the required permutation type is a match with the image's permutation type, then a solution exists.

    if permutation_type_required == image_permutation_type:
        solution_exists = 1
    else:
        solution_exists = 0
    # For debug purposses
    if debug == 1:
        print(
            "The reference and image arrays are respectively: %s and %s. Their corresponding rectangular arrays are %s and %s in that arrangement."
            % (reference, image, reference_rectangular, image_rectangular)
        )
        print(
            "Blank space of reference is at row %s and column %s"
            % (
                reference_inner_list_element_row_position,
                reference_inner_list_element_column_position,
            ),
        )
        print(
            "Blank space of image is at row %s and column %s"
            % (
                image_inner_list_element_row_position,
                image_inner_list_element_column_position,
            ),
        )
        print(
            "The row difference of the reference and image blank spaces is %d, and the column difference of the reference and image blank space is %d, hence the sum of the row and column differences we've mentioned earlier is %d"
            % (row_difference, column_difference, num_of_blank_space_swaps)
        )
    else:
        pass
    return (
        solution_exists,
        permutation_type_required,
        image_permutation_type,
    )  # Returns whether a solution exists (1 if it does, 0 if there is no solution), the parity of reference and image permutation type required, and the image permutation type.
