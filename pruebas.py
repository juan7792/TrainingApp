message_sets = "Enter number of reps per set separated by '-' (e.g. 3 sets of 5 reps: 5-5-5): "

sets = input("Enter number of sets: ")


def check_reps_or_intensity(sets, message):
    while reps_or_intensity_input := input(message):
        try:
            try:
                try:
                    dummy = reps_or_intensity_input.split("-", int(sets))
                    [int(dum) for dum in dummy]
                    dummy[int(sets) - 1]
                    break
                except ValueError:
                    print("Error: wrong input. Follow the format given in the example!")
            except TypeError:
                print("Error: wrong input. Do not introduce letters!")
        except IndexError:
            print("Error: wrong input. Write the numbers for each respective set separated by a '-'!")


check_reps_or_intensity(sets, message_sets)