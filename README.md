# Contact-List-Console-In-Python-With-Database
A contact list, running in the console, that reads and writes to a locally hosted database.

The user is allowed to add contacts, delete contacts, edit contacts, and list the contact database.

Written in Python, and tested with PostgreSQL via pgAdmin 4.

The program checks user input for correct formatting, and gives prompts to the user in relation to said formatting.  The error checking logic is stored in independent functions, which are called both during the add contact action and edit contact action.

As currently written, the program must run on a Windows based system because it imports the msvcrt library for "Press Any Key to Continue" functionality.  You can comment out this include, as well as the "def wait()" and "wait()" function calls in order to run this program on Mac, Linux, or other supporting OS.
