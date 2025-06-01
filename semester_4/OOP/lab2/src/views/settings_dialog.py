from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                          QCheckBox, QComboBox, QPushButton, QListWidget, 
                          QLineEdit, QFormLayout, QTabWidget, QWidget,
                          QGroupBox, QDialogButtonBox)
from PyQt6.QtCore import Qt
from src.models.task import Priority


class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None, categories=None):
        super().__init__(parent)
        
        self.settings = settings or {}
        self.categories = categories or []
        self.result_settings = self.settings.copy()
        self.result_categories = self.categories.copy()
        
        self.setWindowTitle("Settings")
        self.setMinimumSize(500, 400)
        
        self._create_layout()
    
    def _create_layout(self):
        layout = QVBoxLayout(self)
        
        # Create tabs
        tab_widget = QTabWidget()
        
        # General settings tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # Appearance group
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout(appearance_group)
        
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setChecked(self.settings.get("dark_mode", False))
        appearance_layout.addWidget(self.dark_mode_checkbox)
        
        general_layout.addWidget(appearance_group)
        
        # Task settings group
        task_group = QGroupBox("Tasks")
        task_layout = QFormLayout(task_group)
        
        self.show_completed_checkbox = QCheckBox()
        self.show_completed_checkbox.setChecked(self.settings.get("show_completed", True))
        task_layout.addRow("Show completed tasks:", self.show_completed_checkbox)
        
        self.default_priority_combo = QComboBox()
        self.default_priority_combo.addItems([p.name for p in Priority])
        current_priority = self.settings.get("default_priority", Priority.MEDIUM)
        self.default_priority_combo.setCurrentText(current_priority.name)
        task_layout.addRow("Default priority:", self.default_priority_combo)
        
        self.sort_by_combo = QComboBox()
        self.sort_by_combo.addItems(["due_date", "priority", "title", "created_at"])
        self.sort_by_combo.setCurrentText(self.settings.get("sort_by", "due_date"))
        task_layout.addRow("Sort tasks by:", self.sort_by_combo)
        
        general_layout.addWidget(task_group)
        
        # Categories tab
        categories_tab = QWidget()
        categories_layout = QVBoxLayout(categories_tab)
        
        categories_label = QLabel("Manage task categories:")
        categories_layout.addWidget(categories_label)
        
        self.categories_list = QListWidget()
        self.categories_list.addItems(self.categories)
        categories_layout.addWidget(self.categories_list)
        
        categories_buttons_layout = QHBoxLayout()
        
        self.new_category_edit = QLineEdit()
        categories_buttons_layout.addWidget(self.new_category_edit)
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self._on_add_category)
        categories_buttons_layout.addWidget(add_button)
        
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self._on_remove_category)
        categories_buttons_layout.addWidget(remove_button)
        
        categories_layout.addLayout(categories_buttons_layout)
        
        # Add tabs to widget
        tab_widget.addTab(general_tab, "General")
        tab_widget.addTab(categories_tab, "Categories")
        
        layout.addWidget(tab_widget)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def _on_add_category(self):
        category = self.new_category_edit.text().strip()
        if category and category not in self.result_categories:
            self.result_categories.append(category)
            self.categories_list.addItem(category)
            self.new_category_edit.clear()
    
    def _on_remove_category(self):
        selected_items = self.categories_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            category = item.text()
            self.categories_list.takeItem(self.categories_list.row(item))
            self.result_categories.remove(category)
    
    def _on_accept(self):
        # Update settings
        self.result_settings["dark_mode"] = self.dark_mode_checkbox.isChecked()
        self.result_settings["show_completed"] = self.show_completed_checkbox.isChecked()
        
        priority_name = self.default_priority_combo.currentText()
        self.result_settings["default_priority"] = Priority[priority_name]
        
        self.result_settings["sort_by"] = self.sort_by_combo.currentText()
        
        self.accept()
    
    def get_settings(self):
        return self.result_settings
    
    def get_categories(self):
        return self.result_categories 