import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.models.task_manager import TaskManager
from src.views.main_window import MainWindow
from src.controllers.task_controller import TaskController


def main():
    # Create the application
    app = QApplication(sys.argv)
    
    # Create model
    task_manager = TaskManager()
    
    # Add some sample tasks
    from src.models.task import Task, Priority
    from datetime import datetime, timedelta
    
    # Sample task 1: Due today, high priority
    task1 = Task(
        title="Complete Python project",
        description="Finish implementing the task management application",
        due_date=datetime.now(),
        priority=Priority.HIGH
    )
    task_manager.add_task(task1)
    
    # Sample task 2: Due tomorrow, medium priority
    task2 = Task(
        title="Prepare presentation",
        description="Create slides for the project presentation",
        due_date=datetime.now() + timedelta(days=1),
        priority=Priority.MEDIUM
    )
    task_manager.add_task(task2)
    
    # Sample task 3: Due in 3 days, low priority
    task3 = Task(
        title="Research new technologies",
        description="Look into new frameworks for future projects",
        due_date=datetime.now() + timedelta(days=3),
        priority=Priority.LOW
    )
    task_manager.add_task(task3)
    
    # Sample task 4: Overdue, high priority
    task4 = Task(
        title="Submit report",
        description="Send the quarterly report to the manager",
        due_date=datetime.now() - timedelta(days=1),
        priority=Priority.HIGH
    )
    task_manager.add_task(task4)
    
    # Sample task 5: Completed task
    task5 = Task(
        title="Install Python libraries",
        description="Set up the development environment",
        due_date=datetime.now() - timedelta(days=2),
        priority=Priority.MEDIUM,
        completed=True
    )
    task_manager.add_task(task5)
    
    # Create main window
    main_window = MainWindow()
    
    # Create controller
    controller = TaskController(task_manager, main_window)
    
    # Show the main window
    main_window.show()
    
    # Start the event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 