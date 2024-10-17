# Loo-Locator

Basis of this project is to:

    1. Create a web application for students attending UNCC
    2. Enable Users to rate and review bathrooms through created web application
    3. Promote high rated bathrooms for others to see

To accomplish these goals:

    1. Integrate Google Maps API to have map functionality
    2. Enable a dropped pin feature for students to mark and rate bathrooms on campus for others to see
    3. Use database CRUD operations for efficient database operations
    4. Create user interface that promotes users to continue interacting with the application


Accomplishments as a team thus far:

    1. User stories
    2. Github setup
    3. Tasks for each developer

---

# Application Development Setup

## Prerequisites
**python** 3.13.0\
**pip** 24.2\
**pipenv** 2023.9.8\
**virtalenv** 20.24.5\
*so long as you are within the same major version, any other version should be fine*

1. Run `pipenv install` in the Loo-Locator/ dir to spawn a virtualenv and install all dependencies
within it.

2. If needed, use `pipenv shell` while in the Loo-Locator dir to activate the virtual environment.
Use `pipenv exit` to exit.

**NOTE**: If VSCode shows errors or is not recognizing a dependency, select the correct Pyton
interpeter. To do this, press Ctrl-Shift-P (Cmd-Shift-P on Mac) and search: Pyton: Select
Interpreter. Select the one that looks like:
    
    > Python 3.13.0 ('Loo-Locator--{random-letters}': Pipenv)

In general, pipenv is a little weird when used with VSCode terminals because the actual VSCode
instance does not care when you run `pipenv shell` or `pipenv install` in the VSCode
terminal- it will continue to use global packages, while the terminal will correctly use the
virtualenv, until you switch interpreters as described above. However, if you do this you might end
up attempting to spawn a virtualenv within a virtualenv. This can cause some issues when trying to
do something like install new dependecies.

The easiest solution is to switch the interprter in VSCode to get syntax highlighting, and
develop there, but run all your commands in a seperate terminal.

3. Once dependencies are installed, update the connection URI in app.py. This should be your
credentias to wherever your SQL connection is. If you are using a default MySQL Workbench
connection, all that needs to change is the 'password' part of the URI. That needs to be
your root password to MySQL Workbench.

5. Finally, run `python -m flask run` to run application on localhost

Make sure that when you are installing new dependencies they are reflected in the
Pipfile & Pipfile.lock. You can manually add them in the Pipfile, then run `pipenv lock` to update
the lock file.