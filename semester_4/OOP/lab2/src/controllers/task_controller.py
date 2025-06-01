from PyQt6.QtWidgets import QMessageBox, QDialog
from datetime import datetime


class TaskController:
    def __init__(self, task_manager, main_window):
        self.task_manager = task_manager
        self.main_window = main_window
        
        # Connect signals from main window to controller methods
        self.main_window.add_task_requested.connect(self.add_task)
        self.main_window.edit_task_requested.connect(self.edit_task)
        self.main_window.complete_task_requested.connect(self.complete_task)
        self.main_window.delete_task_requested.connect(self.delete_task)
        self.main_window.filter_changed.connect(self.filter_tasks)
        self.main_window.open_settings_requested.connect(self.open_settings)
        self.main_window.open_statistics_requested.connect(self.open_statistics)
        
        # Initial data load
        self.update_task_list()
    
    def update_task_list(self):
        current_filter = self.main_window.filter_combo.currentText()
        self.filter_tasks(current_filter)
    
    def filter_tasks(self, filter_text):
        tasks = []
        
        if filter_text == "All":
            tasks = self.task_manager.get_all_tasks()
        elif filter_text == "Pending":
            tasks = self.task_manager.get_pending_tasks()
        elif filter_text == "Completed":
            tasks = self.task_manager.get_completed_tasks()
        elif filter_text == "High Priority":
            from src.models.task import Priority
            tasks = self.task_manager.get_tasks_by_priority(Priority.HIGH)
        elif filter_text == "Medium Priority":
            from src.models.task import Priority
            tasks = self.task_manager.get_tasks_by_priority(Priority.MEDIUM)
        elif filter_text == "Low Priority":
            from src.models.task import Priority
            tasks = self.task_manager.get_tasks_by_priority(Priority.LOW)
        elif filter_text == "Overdue":
            tasks = self.task_manager.get_overdue_tasks()
        
        self.main_window.update_tasks(tasks)
        self.main_window.update_status(f"Showing {len(tasks)} tasks")
    
    def add_task(self):
        result = self.main_window.open_task_dialog()
        
        if result == QDialog.DialogCode.Accepted:
            task = self.main_window.task_dialog.get_task()
            if task:
                self.task_manager.add_task(task)
                self.update_task_list()
                self.main_window.update_status("Task added successfully")
    
    def edit_task(self, task_id):
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            return
        
        result = self.main_window.open_task_dialog(task)
        
        if result == QDialog.DialogCode.Accepted:
            self.update_task_list()
            self.main_window.update_status("Task updated successfully")
    
    def complete_task(self, task_id):
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            return
        
        if not task.completed:
            self.task_manager.complete_task(task_id)
            self.update_task_list()
            self.main_window.update_status("Task marked as completed")
    
    def delete_task(self, task_id):
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Deletion",
            f"Are you sure you want to delete the task '{task.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.task_manager.delete_task(task_id)
            self.update_task_list()
            self.main_window.update_status("Task deleted successfully")
    
    def open_settings(self):
        settings = self.task_manager.settings
        categories = self.task_manager.categories
        
        result = self.main_window.open_settings_dialog(settings, categories)
        
        if result == QDialog.DialogCode.Accepted:
            # Update task manager with new settings
            new_settings = self.main_window.settings_dialog.get_settings()
            new_categories = self.main_window.settings_dialog.get_categories()
            
            self.task_manager.settings = new_settings
            self.task_manager.categories = new_categories
            
            self.main_window.update_status("Settings updated successfully")
    
    def open_statistics(self):
        stats = self.task_manager.get_tasks_stats()
        self.main_window.open_statistics_dialog(stats) 