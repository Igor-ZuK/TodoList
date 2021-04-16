# Write your code here
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

# CONFIG
engine = create_engine('sqlite:///todo.db?check_same_thread=False', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class TaskInterface:

    @staticmethod
    def menu():
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")

    @staticmethod
    def add_task():
        print("\nEnter task")
        task_name = input()
        print("Enter deadline")
        task_deadline = input()
        task_deadline = datetime.strptime(task_deadline, "%Y-%m-%d")
        task = Task(task=task_name, deadline=task_deadline)
        session.add(task)
        session.commit()
        print("The task has been added!\n")

    @staticmethod
    def show_all_tasks():
        tasks = session.query(Task).order_by(Task.deadline).all()
        print("\nAll tasks:")
        if len(tasks) != 0:
            for i, task in enumerate(tasks):
                print(f"{i + 1}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}")
        else:
            print("Nothing to do!")
        print("")

    @staticmethod
    def show_today_tasks():
        tasks = session.query(Task).filter(Task.deadline == datetime.today().date()).all()
        today = datetime.today().strftime("%b %d")
        print(f"\nToday {today}:")
        if len(tasks) != 0:
            for i, task in enumerate(tasks):
                print(f"{i + 1}. {task.task}")
        else:
            print("Nothing to do!")
        print("")

    @staticmethod
    def show_week_tasks():
        day = 0
        while day <= 6:
            rows = session.query(Task).filter(Task.deadline == datetime.today().date() + timedelta(days=day)) \
                .order_by(Task.deadline).all()
            date = (datetime.today() + timedelta(days=day)).strftime("%A %b %d")
            print(f"\n{date}:")
            day += 1
            if len(rows) == 0:
                print("Nothing to do!")
            else:
                event = 0
                for row in rows:
                    event += 1
                    print(f"{event}) {row.task}")

    @staticmethod
    def show_missed_tasks():
        tasks = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
        print("\nMissed tasks:")
        if len(tasks) != 0:
            for i, task in enumerate(tasks):
                print(f"{i + 1}. {task.task}. {task.deadline.strftime('%d %b')}")
        else:
            print("Nothing is missed!")
        print("")

    @staticmethod
    def delete_task():
        tasks = session.query(Task).order_by(Task.deadline).all()
        print("\nChoose the number of the task you want to delete:")
        if len(tasks) != 0:
            for i, task in enumerate(tasks):
                print(f"{i + 1}. {task.task}. {task.deadline.strftime('%d %b')}")
            deleted_id = int(input())
            if 0 < deleted_id < len(tasks):
                deleted_task = tasks[deleted_id - 1]
                session.delete(deleted_task)
                session.commit()
            else:
                print("Incorrect input!")
        else:
            print("Nothing to delete!")
        print("")


def main():
    task_interface = TaskInterface()
    while 1:
        task_interface.menu()
        user_choice = input()
        if user_choice == '1':
            task_interface.show_today_tasks()
        elif user_choice == '2':
            task_interface.show_week_tasks()
        elif user_choice == '3':
            task_interface.show_all_tasks()
        elif user_choice == '4':
            task_interface.show_missed_tasks()
        elif user_choice == '5':
            task_interface.add_task()
        elif user_choice == '6':
            task_interface.delete_task()
        elif user_choice == '0':
            print("\nBye!")
            break


if __name__ == '__main__':
    if os.path.exists("todo.db"):
        Base.metadata.create_all(engine)
    main()
