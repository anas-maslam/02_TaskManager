import datetime
import json
import os.path
import getpass
import hashlib


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __str__(self):
        return f"{self.name} - {self.email}"

    def login(self, email, password):
        if not os.path.exists("user.json"):
            return ""
        with open("user.json", "r") as file:
            users = json.load(file)
            for user in users:
                if user["email"] == email and user["password"] == password:
                    return user["email"]
        return ""

    def add_user(self, name, email, password):
        user = User(name, email, password)
        return user

    def delete_user(self, email):
        with open("user.json", "r") as file:
            users = json.load(file)
        if self.email == email:
            del self.email
        else:
            print("Invalid email")

    def view_user(self):
        return self.name, self.email

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    def append_user_json_file(self, name, email, password):
        users = []
        if os.path.exists("user.json"):
            with open("user.json", "r") as file:
                users = json.load(file)
        user = self.add_user(name, email, password)
        users.append(user.to_dict())
        with open("user.json", "w") as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def print_all_users():
        with open("user.json", "r") as file:
            users = json.load(file)
            for user in users:
                print(user)


class Tasks:
    def __init__(self, sno, completed="No", description="", date=None):
        self.sno = sno
        self.completed = completed
        self.description = description
        self.date = date or datetime.date.today()

    def __str__(self):
        return f"{self.sno} - Task: {self.description} :: Completed Status: {self.completed} on {self.date}"

    def to_dict(self):
        return {
            "sno": self.sno,
            "description": self.description,
            "completed": self.completed,
            "date": self.date.strftime("%Y-%m-%d")  # Convert date to string
        }


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_tasks(self, sno, completed="No", description="", date=None):
        if not completed:
            print("Invalid completed status")
            return
        if not description:
            print("Description is required")
            return
        task = Tasks(sno, completed, description, date)
        return task
    
    def delete_task(self, email, sno):
        if email in self.tasks:
            tasks_for_email = self.tasks[email]  # Accessing the list using the __getitem__ method

            for task in tasks_for_email:
                if int(task["sno"]) == sno:
                    print(f"Deleting task {sno} for {email}.")
                    # Remove the task from the list of tasks
                    self.tasks[email] = [t for t in tasks_for_email if t["sno"] != sno]
                    self.save_tasks()
                    return True
        return False

    def view_tasks(self, email):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                try:
                    existing_tasks = json.load(file)
                    self.tasks = existing_tasks
                except json.JSONDecodeError:
                    existing_tasks = {}
                    self.tasks = {}
        else:
            existing_tasks = {}
            self.tasks = {}

        if not email in existing_tasks:
            print("No tasks found for this user.")
        else:
            print("Tasks for:", email)
            for task in existing_tasks[email]:
                print(task)

        # if not email in self.tasks:
        #     self.tasks[email] = []
        # else:
        #     # Load expenses for the given email if they exist in the JSON
        #     if email in existing_tasks:
        #         self.tasks[email] = [
        #             Tasks(
        #                 expense["sno"],
        #                 expense["description"],
        #                 expense["completed"],
        #                 datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date()
        #             ) for expense in existing_tasks[email]
        #         ]
        #     else:
        #         # If there are no expenses for this email, you can initialize it
        #         self.tasks[email] = []  # Ensure it's initialized
        #
        #     # Display the user's expenses
        #     if not self.tasks[email]:
        #         print("No tasks found for this user.")
        #     else:
        #         print("Tasks for:", email)
        #         for task in self.tasks[email]:
        #             print(task)

    def search_tasks(self, email, keyword):
        return [task for task in self.tasks[email] if keyword.lower() in task.description.lower()]

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                try:
                    self.tasks = json.load(file)
                except json.JSONDecodeError:
                    self.tasks = {}
        else:
            self.tasks = {}

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=4)

    def update_task_status(self, email, sno, completed):
        # Load existing tasks
        self.load_tasks()

        # Check if the email exists in the tasks
        if email in self.tasks:
            for task in self.tasks[email]:
                if task["sno"] == sno:
                    task["completed"] = completed
                    print(f"Updated task {sno} status to '{completed}' for {email}.")
                    break
            else:
                print(f"Task with sno {sno} not found for {email}.")
        else:
            print(f"No tasks found for {email}.")

        # Save the updated tasks back to the file
        self.save_tasks()

    def update_task_status_json_file(self, email, sno, status):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                try:
                    existing_tasks = json.load(file)
                except json.JSONDecodeError:
                    existing_tasks = {}
        else:
            existing_tasks = {}
        if not email in existing_tasks:
            existing_tasks[email] = []

        for task in existing_tasks[email]:
            if task["sno"] == sno:
                task.completed = status
                break

        # existing_tasks[email].append([task.to_dict() for task in self.tasks[email]])
        with open("tasks.json", "w") as file:
            json.dump(existing_tasks, file, indent=4)

    def write_tasks_json_file(self, email, task):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                try:
                    existing_tasks = json.load(file)
                except json.JSONDecodeError:
                    existing_tasks = {}
        else:
            existing_tasks = {}
        if not email in existing_tasks:
            existing_tasks[email] = []

        # existing_tasks[email].extend([expense.to_dict() for expense in self.expenses[email]])
        existing_tasks[email].extend([task.to_dict()])
        # existing_tasks[email].append([expense.to_dict() for expense in self.expenses[email]])
        with open("tasks.json", "w") as file:
            json.dump(existing_tasks, file, indent=4)

    def read_all_tasks_json_file(self, email):
        with open("task.json", "r") as file:
            tasks = json.load(file)
            return [Tasks(task["description"], task["completed"], datetime.datetime.strptime(task["date"], "%Y-%m-%d").date()) for task in tasks[email]]

    def load_all_task(self, email):
        if os.path.exists("task.json"):
            with open("task.json", "r") as file:
                try:
                    existing_tasks = json.load(file)
                except json.JSONDecodeError:
                    existing_tasks = {}
        else:
            existing_tasks = {}
        if not email in self.tasks:
            self.tasks[email] = []
        else:
            self.tasks[email] = [Tasks(task["sno"], task["description"], task["completed"], datetime.datetime.strptime(task["date"], "%Y-%m-%d").date()) for task in existing_tasks[email]]


def manage_tasks():
    while True:
        print("\n******** Task Manager Menu ********")
        print("1. Login")
        print("2. Register")
        print("3. View Users")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            email = input("Enter email: ")
            password = getpass.getpass("Enter password: ")
            passHash = hashlib.sha256(password.encode()).hexdigest()

            user = User("", email, passHash)
            authenticated_username = user.login(email, passHash)
            if authenticated_username != "":
                print(f"Welcome \"{authenticated_username}\": Login successful...")
                break
            else:
                print("Login failed. Please try again.\n")

        if choice == "2":
            name = input("Enter name: ")
            email = input("Enter email: ")
            password = getpass.getpass("Enter password: ")
            passHash = hashlib.sha256(password.encode()).hexdigest()

            user = User(name, email, passHash)
            user.append_user_json_file(name, email, passHash)

        if choice == "3":
            User.print_all_users()

        if choice == "4":
            break

    tracker = TaskManager()
    tracker.load_all_task(email)

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. View Tasks")
        print("4. Change Task Status")
        print("5. Exit\n")
        choice = input("Enter your choice: ")

        if choice == "1":
            def get_max_sno_json_file(email):
                if not os.path.exists("tasks.json"):
                    return 0
                with open("tasks.json", "r") as file:
                    tasks = json.load(file)
                    if not email in tasks:
                        return 0
                    return max(task["sno"] for task in tasks[email])

            sno = get_max_sno_json_file(email) + 1
            description = input("Enter Task description: ")
            completed = input("Enter Task Completion Status (Yes/No): ")
            date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date() if date_input else None
            expense = tracker.add_tasks(sno, completed, description, date)
            tracker.write_tasks_json_file(email, expense)

        elif choice == "2":
            tracker.view_tasks(email)
            sno = int(input("\n\nEnter expense SNo to delete: "))
            is_task_deleted = tracker.delete_task(email, sno)
            if is_task_deleted:
                print(f"Task {sno} deleted successfully.")

        elif choice == "3":
            tracker.view_tasks(email)

        elif choice == "4":
            tracker.view_tasks(email)
            sno = int(input("\n\nEnter Sno of task you want to change: "))
            status = input("\n\nEnter tas Status (Yes/No): ")

            tracker.update_task_status(email, sno, status)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    manage_tasks()
