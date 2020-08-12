def ask_input_date():
    while input_date := input("Enter date: "):
        try:
            return datetime.datetime.strptime(input_date, "%d-%m-%Y")
        except ValueError:
            print("Que bicha mas gafa")


 while select_exercise := input("Select user to add exercise to (only ID number please): "):
        try:
            try:
                int(select_exercise)
                dummy_list[int(select_exercise) - 1][0]
                return select_exercise
            except ValueError:
                print(f"Error: Please select only an ID number within the list!")
        except IndexError:
            print("Error: Please select only an ID number within the list!")


def select_exercise_from_muscle_group(exercises):
    # print exercises
    print("")
    for i in range(len(exercises)):
        print(f"{i + 1}) {exercises[i][0]}")
    print("")

    # exercises IDs in a list of strings
    exercise_list = [f"{exercises[i][0]}" for i in range(len(exercises))]

    # list to check if user entered correct ID
    dummy_list = [f"{i + 1}" for i in range(len(exercises))]

    # try except
    # check that input is a number and is within options
    while (select_exercise :=
    input("Select exercise to be added to training (only ID number please): ")) \
            not in dummy_list:
        print("Error: Please select only an ID number within the list!")

    return exercises[int(select_exercise) - 1]  # select proper exercise ID
