import os
import psycopg2

from dotenv import load_dotenv

# load environment variable
load_dotenv()

# FUNCTIONS ARE EXECUTED IN app.py
# variables to create tables
CREATE_TABLE_USERS = """ CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username TEXT
);"""
# the column training_type shows if the exercise is push, pull, legs, etc.
CREATE_TABLE_EXERCISES = """ CREATE TABLE IF NOT EXISTS exercises(
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    exercise_name TEXT,
    training_type TEXT, 
    FOREIGN KEY(user_id) REFERENCES users(id)
);"""
# the column workout_type shows if the workout was for body building, power lifting, functional, etc.
CREATE_TABLE_TRAININGS = """ CREATE TABLE IF NOT EXISTS trainings(
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    exercise_id INTEGER,
    date INTEGER NOT NULL,
    sets INTEGER NOT NULL,
    reps TEXT NOT NULL,
    intensity_kg TEXT NOT NULL,
    workout_type TEXT,
    body_weight_kg REAL,
    observations TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(exercise_id) REFERENCES exercises(id)
);"""

# variables to add entries
ADD_USER = "INSERT INTO users (username) VALUES (%s);"
ADD_EXERCISE = "INSERT INTO exercises (user_id, exercise_name, training_type) VALUES (%s, %s, %s)"
ADD_TRAINING = """INSERT INTO trainings(
user_id, exercise_id, date, sets, reps, intensity_kg, workout_type, body_weight_kg, observations
) 
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

# variables to select and show data from database
SELECT_ALL_USERS = "SELECT * FROM users;"
SELECT_SPECIFIC_USER = "SELECT username FROM users WHERE id=%s;"
SELECT_ALL_EXERCISES_FROM_USER = "SELECT id, exercise_name FROM exercises WHERE user_id=%s;"
SELECT_ALL_TRAININGS_FROM_USER = """
SELECT trainings.date, exercises.training_type, 
    exercises.exercise_name, trainings.sets, 
    trainings.reps, trainings.intensity_kg, 
    trainings.workout_type, trainings.body_weight_kg, 
    trainings.observations
FROM exercises 
JOIN trainings ON exercises.id = trainings.exercise_id
WHERE exercises.user_id = %s
ORDER BY trainings.date ASC
;"""
SELECT_SPECIFIC_TRAINING_FROM_USER = """
SELECT trainings.date, exercises.training_type, 
    exercises.exercise_name, trainings.sets, 
    trainings.reps, trainings.intensity_kg, 
    trainings.workout_type, trainings.body_weight_kg, 
    trainings.observations
FROM exercises 
JOIN trainings ON exercises.id = trainings.exercise_id
WHERE exercises.user_id = %s 
    AND trainings.date = %s
ORDER BY trainings.date ASC
;"""
SELECT_TRAINING_PERIOD_FROM_USER = """
SELECT trainings.date, exercises.training_type, 
    exercises.exercise_name, trainings.sets, 
    trainings.reps, trainings.intensity_kg, 
    trainings.workout_type, trainings.body_weight_kg, 
    trainings.observations
FROM exercises 
JOIN trainings ON exercises.id = trainings.exercise_id
WHERE exercises.user_id = %s 
    AND (trainings.date >= %s AND trainings.date <= %s)
ORDER BY trainings.date ASC
;"""
SELECT_MUSCLE_GROUPS_FROM_USER = """
SELECT DISTINCT training_type FROM exercises
WHERE user_id = %s
ORDER BY training_type
;"""
SELECT_MUSCLE_GROUP_FOR_VOLUME_FROM_USER = """
SELECT trainings.reps, trainings.intensity_kg, trainings.date
FROM exercises 
JOIN trainings ON exercises.id = trainings.exercise_id
WHERE exercises.user_id = %s 
    AND exercises.training_type = %s
ORDER BY trainings.date ASC
;"""
SELECT_MUSCLE_GROUP_FOR_SPECIFIC_VOLUME_FROM_USER = """
SELECT trainings.reps, trainings.intensity_kg, trainings.date
FROM exercises 
JOIN trainings ON exercises.id = trainings.exercise_id
WHERE exercises.user_id = %s
    AND exercises.training_type = %s
    AND trainings.date = %s
ORDER BY trainings.date ASC
;
"""
SELECT_MUSCLE_GROUP_FOR_VOLUME_IN_PERIOD_FROM_USER = """
SELECT trainings.reps, trainings.intensity_kg, trainings.date
FROM exercises 
JOIN trainings ON exercises.id = trainings.exercise_id
WHERE exercises.user_id = %s
    AND exercises.training_type = %s
    AND (trainings.date >= %s AND trainings.date <= %s)
ORDER BY trainings.date ASC
;"""
SELECT_EXERCISES_FROM_MUSCLE_GROUP_FROM_USER = """
SELECT exercise_name FROM exercises
WHERE user_id = %s
	AND training_type = %s
ORDER BY exercise_name
;"""

# database must be created (if it does not exist) and we must connect to it - postgres uses the URL of the database
connection = psycopg2.connect(os.environ["DATABASE_URL"])


# postgres uses cursors for its operations
# function to create tables
def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_USERS)
            cursor.execute(CREATE_TABLE_EXERCISES)
            cursor.execute(CREATE_TABLE_TRAININGS)


# function to insert a new user
def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ADD_USER, (username,))


# function to insert a new exercise in a selected user
def add_exercise(user_id, exercise_name, training_type):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ADD_EXERCISE, (user_id, exercise_name, training_type))


# function to insert a new exercise in a selected user
def add_training(user_id, exercise_id, date, sets, reps, intensity_kg, workout_type, body_weight, observations):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ADD_TRAINING, (user_id, exercise_id, date, sets, reps,
                                          intensity_kg, workout_type, body_weight, observations))


# function to view all users from users table
def get_all_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_USERS)
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view all users from users table
def get_specific_user(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_SPECIFIC_USER, (user_id,))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view all exercises from selected user
def get_all_exercises_from_user(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_EXERCISES_FROM_USER, (user_id,))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view all trainings in the logbook from selected user
def get_all_trainings_from_user(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_TRAININGS_FROM_USER, (user_id,))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view specific training in the logbook from selected user
def get_specific_training_from_user(user_id, date):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_SPECIFIC_TRAINING_FROM_USER, (user_id, date))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view training period in the logbook from selected user
def get_training_period_from_user(user_id, date_initial, date_final):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_TRAINING_PERIOD_FROM_USER, (user_id, date_initial, date_final))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view muscle group from selected user
def get_muscle_group_from_user(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_MUSCLE_GROUPS_FROM_USER, (user_id,))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view muscle group from selected user
def get_muscle_group_for_volume_from_user(user_id, muscle_group):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_MUSCLE_GROUP_FOR_VOLUME_FROM_USER, (user_id, muscle_group))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view muscle group in specific date from selected user
def get_muscle_group_for_specific_volume_from_user(user_id, muscle_group, date):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_MUSCLE_GROUP_FOR_SPECIFIC_VOLUME_FROM_USER, (user_id, muscle_group, date))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view muscle group in time period from selected user
def get_muscle_group_for_volume_in_period_from_user(user_id, muscle_group, date_initial, date_final):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_MUSCLE_GROUP_FOR_VOLUME_IN_PERIOD_FROM_USER,
                           (user_id, muscle_group, date_initial, date_final))
            return cursor.fetchall()  # returns cursor with list of elements selected


# function to view muscle group from selected user
def get_exercises_from_muscle_group_from_user(user_id, muscle_group):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_EXERCISES_FROM_MUSCLE_GROUP_FROM_USER, (user_id, muscle_group))
            return cursor.fetchall()  # returns cursor with list of elements selected
