from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                          QLineEdit, QTextEdit, QDateEdit, QComboBox,
                          QPushButton, QFormLayout, QDialogButtonBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from src.models.task import Task, Priority


class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.result_task = None
        
        self.setWindowTitle("Add Task" if task is None else "Edit Task")
        self.setMinimumWidth(400)
        
        self._apply_styles()
        self._create_form()
        self._create_buttons()
        
        # Fill form if editing existing task
        if task:
            self._populate_form()
    
    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #e8eef7;
            }
            QLineEdit, QTextEdit, QDateEdit, QComboBox {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                selection-background-color: #d0e0f7;
                min-height: 24px;
                color: #000000;
            }
            QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus {
                border: 1px solid #2979ff;
            }
            QLabel {
                font-weight: bold;
                color: #000000;
                padding-right: 8px;
            }
            QDialogButtonBox QPushButton {
                background-color: #2979ff;
                color: white;
                border: 1px solid #1565c0;
                padding: 8px 16px;
                border-radius: 6px;
                min-width: 100px;
                font-weight: bold;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #2962ff;
            }
            QDialogButtonBox QPushButton:pressed {
                background-color: #1565c0;
            }
            QDialogButtonBox QPushButton[text="Cancel"] {
                background-color: #e0e0e0;
                color: #000000;
                border: 1px solid #c0c0c0;
            }
            QDialogButtonBox QPushButton[text="Cancel"]:hover {
                background-color: #d0d0d0;
            }
        """)
    
    def _create_form(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(16)
        self.layout.setContentsMargins(24, 24, 24, 24)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(16)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        
        # Title with placeholder
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter task title")
        self.title_edit.setMinimumHeight(36)
        title_label = QLabel("Title:")
        title_label.setFont(QFont("", 11))
        form_layout.addRow(title_label, self.title_edit)
        
        # Description with placeholder
        self.description_edit = QTextEdit()
        self.description_edit.setAcceptRichText(False)
        self.description_edit.setMinimumHeight(120)
        self.description_edit.setPlaceholderText("Enter task description")
        description_label = QLabel("Description:")
        description_label.setFont(QFont("", 11))
        form_layout.addRow(description_label, self.description_edit)
        
        # Due Date
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDate(QDate.currentDate())
        self.due_date_edit.setMinimumHeight(36)
        due_date_label = QLabel("Due Date:")
        due_date_label.setFont(QFont("", 11))
        form_layout.addRow(due_date_label, self.due_date_edit)
        
        # Priority with color indicators
        self.priority_combo = QComboBox()
        self.priority_combo.setMinimumHeight(36)
        
        # Add priority items with color indicators
        self.priority_combo.addItem(Priority.HIGH.name)
        self.priority_combo.addItem(Priority.MEDIUM.name)
        self.priority_combo.addItem(Priority.LOW.name)
        
        # Set item colors and default value
        self.priority_combo.setItemData(0, QColor("#c62828"), Qt.ItemDataRole.BackgroundRole)
        self.priority_combo.setItemData(0, QColor("white"), Qt.ItemDataRole.ForegroundRole)
        self.priority_combo.setItemData(1, QColor("#ef6c00"), Qt.ItemDataRole.BackgroundRole)
        self.priority_combo.setItemData(1, QColor("white"), Qt.ItemDataRole.ForegroundRole)
        self.priority_combo.setItemData(2, QColor("#0277bd"), Qt.ItemDataRole.BackgroundRole)
        self.priority_combo.setItemData(2, QColor("white"), Qt.ItemDataRole.ForegroundRole)
        
        self.priority_combo.setCurrentText(Priority.MEDIUM.name)
        priority_label = QLabel("Priority:")
        priority_label.setFont(QFont("", 11))
        form_layout.addRow(priority_label, self.priority_combo)
        
        self.layout.addLayout(form_layout)
    
    def _create_buttons(self):
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        
        # Add spacing before buttons
        self.layout.addSpacing(16)
        self.layout.addWidget(button_box)
    
    def _populate_form(self):
        self.title_edit.setText(self.task.title)
        self.description_edit.setPlainText(self.task.description)
        
        if self.task.due_date:
            self.due_date_edit.setDate(QDate(self.task.due_date.year, 
                                            self.task.due_date.month, 
                                            self.task.due_date.day))
        
        self.priority_combo.setCurrentText(self.task.priority.name)
    
    def _on_accept(self):
        # Validate input
        if not self.title_edit.text().strip():
            return
        
        title = self.title_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        
        due_date_qdate = self.due_date_edit.date()
        due_date = datetime(due_date_qdate.year(), due_date_qdate.month(), due_date_qdate.day())
        
        priority_name = self.priority_combo.currentText()
        priority = Priority[priority_name]
        
        if self.task:
            # Update existing task
            self.task.update(title=title, description=description, 
                            due_date=due_date, priority=priority)
            self.result_task = self.task
        else:
            # Create new task
            self.result_task = Task(title=title, description=description, 
                                  due_date=due_date, priority=priority)
        
        self.accept()
    
    def get_task(self):
        return self.result_task 