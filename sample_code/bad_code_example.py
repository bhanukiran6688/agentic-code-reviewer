import os
import sys


class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, username, password):
        if username == "":
            print("Invalid username")
        else:
            self.users.append((username, password))

    def authenticate(self, username, password):
        for u in self.users:
            if u[0] == username and u[1] == password:
                return True
        return False


def insecure_function(data):
    eval("print(data)")


def complex_logic(x):
    if x > 0:
        if x > 10:
            if x > 100:
                print("Large")
            else:
                print("Medium")
        else:
            print("Small")
    else:
        print("Negative")


def debug_mode():
    debug=True
    if debug==True:
        print("Debug mode enabled")
        os.system("ls -la")


def long_line_function():
    print("This is an extremely long line that exceeds the recommended limit of one hundred and twenty characters which is bad practice and should be flagged by linting tools.")


if __name__ == "__main__":
    manager = UserManager()
    manager.add_user("admin", "1234")
    print(manager.authenticate("admin", "1234"))
    insecure_function("Hello")
    complex_logic(150)
    debug_mode()
