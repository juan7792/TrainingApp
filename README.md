# TrainingApp
TrainingApp was developed in Python to store and retrieve training logs using SQL (SQLite and PostgreSQL). It allows the user to create an account, store his 
personal training logs in it and view the history of his trainings and training volumes.

## 1) Files
The code is composed by two files: app.py and database.py. The reason for this is to use SQLite and/or PostgreSQL (or any other SQL based language) by just changing the file 
database.py, but keeping the same file app.py for both.

### app.py
In this file, the functions corresponding to operations in Python are written.

### database.py
The SQL queries are written in this file and the functions are called in the app.py file.

### TrainingApp.pdf
The flowchart for the operations of the app are contained in this file.

## 2) Tables

### users
This table contains the usernames added to the database, each identified with an unique ID integer.

### exercises
Tables users and exercises hold a relationship using the user ID. In the table "exercises", the exercises with their attached muscle groups are stored and uniquely identified
with an integer ID.

### trainings
This last table holds a relationship with table "users" and "exercises" using the user ID and exercise ID of the latter tables as foreign keys. The details of each training 
log are stored in the table "trainings" and this table has as a primary key a column with the training ID.

## 3) Branches

### app_sqlite
In this branch, the queries are written to be executed using SQLite with the help of the library sqlite3. A local database (data_training.db) is forehanded with some sample 
entries if you want to try out the app.

### app_postgresql
The code for this branch corresponds to queries to be executed in PostgreSQL using the library psycopg2-binary. The remote database is __not__ forhanded (environmental variable), but the code in app.py is the 
same as in SQLite.

## 4) Main functions

### Menu 1
#### Add user (Table: users)
In the first menu, the user can create his username and log in using the option "Select user" (Menu 1) to do further modifications to his account. The username is then stored in
a table named "users" using SQL queries.

### Menu 2
To access the Menu 2, the user must select his username (or account) in Menu 1 and then the app automatically proceeds to Menu 2.

#### Add exercise (Table: exercises)
The user is asked in this function to first enter the name of the exercise and then the attached muscle group to the exercise. The inputs are then committed by executing SQL queries
and the inputs are stored in the table "exercises". It is necessary to add exercises to one's account, as they will be listed when adding a training is intended.

#### Add training (Table: trainings)
In this function, the existing exercises are listed and the app asks the user to input the ID number of his desired exercise. If a desired exercise is not included in the list, one
of the options of this function allows the user to add an exercise and then return to the "Add training" function. Once an exercise is added, the app asks the user to input the 
date, the number of sets done in this exercise, the number of repetitions on each set, the weight lifted on each set, the type of workout (e.g. bodybuilding, 
powerlifting), the body weight [kg] and any observations made. Finally, the inputs are added to the table "trainings".

#### View training
Already added trainings can be seen here. The user must select to view the entire training history, a specific date or a time period. The data logs are retrieved joining tables 
"exercises" and "trainings" using cursors from the executed queries.

#### View training volume
This function works similar as the "View training" function, but here the training volume is calculated and then is presented on a table and plotted (__if more than one log is
retrieved from the database__) for comparison. Similarly to "View training", the data is retrieved from joining tables "exercises" and "trainings"

#### View muscle groups and exercises
This last function allows the user to check his added muscle groups and the exercises within each muscle group. The data is extracted from table "exercises".

#### __IMPORTANT__
For the inputs, it is necessary to follow the format given in the text that appears after before making an input. Nevertheless, the app should not allow the user to input
something different than he should (and if so, please let me know).

