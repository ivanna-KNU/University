from datetime import datetime
from src.models.task import Task, Priority


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.categories = ["Work", "Personal", "Shopping", "Health", "Education"]
        self.settings = {
            "dark_mode": False,
            "show_completed": True,
            "default_priority": Priority.MEDIUM,
            "sort_by": "due_date"
        }
    
    def add_task(self, task):
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        return task.id
    
    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id, **kwargs):
        task = self.get_task_by_id(task_id)
        if task:
            task.update(**kwargs)
            return True
        return False
    
    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def complete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.complete()
            return True
        return False
    
    def get_all_tasks(self):
        return self.tasks.copy()
    
    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]
    
    def get_tasks_by_priority(self, priority):
        return [task for task in self.tasks if task.priority == priority]
    
    def get_overdue_tasks(self):
        today = datetime.now()
        return [task for task in self.tasks 
                if task.due_date and task.due_date < today and not task.completed]
    
    def get_tasks_stats(self):
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        pending = total - completed
        high_priority = len(self.get_tasks_by_priority(Priority.HIGH))
        medium_priority = len(self.get_tasks_by_priority(Priority.MEDIUM))
        low_priority = len(self.get_tasks_by_priority(Priority.LOW))
        overdue = len(self.get_overdue_tasks())
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
            "overdue": overdue,
            "completion_rate": (completed / total) * 100 if total > 0 else 0
        }
    
    def update_setting(self, key, value):
        if key in self.settings:
            self.settings[key] = value
            return True
        return False
    
    def get_setting(self, key):
        return self.settings.get(key)
    
    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)
            return True
        return False
    
    def remove_category(self, category):
        if category in self.categories:
            self.categories.remove(category)
            return True
        return False 