from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task:
    def __init__(self, title="", description="", due_date=None, priority=Priority.MEDIUM, completed=False):
        self.id = None  # Will be set when added to the task list
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def complete(self):
        self.completed = True
        self.updated_at = datetime.now()
    
    def update(self, title=None, description=None, due_date=None, priority=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date
        if priority is not None:
            self.priority = priority
        self.updated_at = datetime.now()
    
    def __str__(self):
        return f"{self.title} - {self.priority.name} - {'Completed' if self.completed else 'Pending'}" 