from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                          QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                          QHeaderView, QComboBox, QStatusBar, QToolBar, QMenu,
                          QMenuBar, QDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QColor, QFont
from datetime import datetime

from src.views.task_dialog import TaskDialog
from src.views.settings_dialog import SettingsDialog
from src.views.statistics_dialog import StatisticsDialog
from src.models.task import Priority


class MainWindow(QMainWindow):
    # Define signals for communication with controllers
    task_selected = pyqtSignal(int)
    add_task_requested = pyqtSignal()
    edit_task_requested = pyqtSignal(int)
    complete_task_requested = pyqtSignal(int)
    delete_task_requested = pyqtSignal(int)
    filter_changed = pyqtSignal(str)
    open_settings_requested = pyqtSignal()
    open_statistics_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 600)
        
        # Apply application-wide style
        self._apply_styles()
        
        self._create_menu_bar()
        self._create_toolbar()
        self._create_central_widget()
        self._create_status_bar()
    
    def _apply_styles(self):
        # Main application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e8eef7;
            }
            QTableWidget {
                gridline-color: #c0c0c0;
                background-color: white;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                selection-background-color: #d0e0f7;
                selection-color: #333333;
                alternate-background-color: #f0f5ff;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #e0e0e0;
                color: #1a1a1a;
            }
            QTableWidget::item:selected {
                background-color: #c0d8f0;
                color: #000000;
            }
            QTableWidget QHeaderView::section {
                background-color: #dce6f5;
                padding: 8px;
                border: 1px solid #c0c0c0;
                border-bottom: 2px solid #a0a0a0;
                font-weight: bold;
                color: #000000;
            }
            QPushButton {
                background-color: #2979ff;
                color: white;
                border: 1px solid #1565c0;
                padding: 8px 16px;
                border-radius: 6px;
                min-width: 100px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2962ff;
            }
            QPushButton:pressed {
                background-color: #1565c0;
            }
            QComboBox {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: white;
                min-width: 140px;
            }
            QStatusBar {
                background-color: #dce6f5;
                color: #000000;
                border-top: 1px solid #c0c0c0;
                font-weight: bold;
            }
            QToolBar {
                background-color: #dce6f5;
                border-bottom: 1px solid #c0c0c0;
                spacing: 8px;
                padding: 6px;
            }
            QLabel {
                color: #000000;
                font-weight: bold;
            }
        """)
        
    def _create_menu_bar(self):
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        new_action = QAction("&New Task", self)
        new_action.triggered.connect(self.add_task_requested.emit)
        file_menu.addAction(new_action)
        
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = self.menuBar().addMenu("&Edit")
        
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.open_settings_requested.emit)
        edit_menu.addAction(settings_action)
        
        # View menu
        view_menu = self.menuBar().addMenu("&View")
        
        stats_action = QAction("&Statistics", self)
        stats_action.triggered.connect(self.open_statistics_requested.emit)
        view_menu.addAction(stats_action)
    
    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(toolbar)
        
        add_button = QAction("Add Task", self)
        add_button.triggered.connect(self.add_task_requested.emit)
        toolbar.addAction(add_button)
        
        filter_label = QLabel("Filter: ")
        toolbar.addWidget(filter_label)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Pending", "Completed", "High Priority", "Medium Priority", "Low Priority", "Overdue"])
        self.filter_combo.currentTextChanged.connect(self.filter_changed.emit)
        toolbar.addWidget(self.filter_combo)
    
    def _create_central_widget(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #e8eef7;")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Task table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["ID", "Title", "Due Date", "Priority", "Status"])
        self.task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_table.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.task_table.setAlternatingRowColors(True)
        self.task_table.setShowGrid(False)
        self.task_table.verticalHeader().setDefaultSectionSize(36)  # Increase row height
        self.task_table.setStyleSheet("QTableView::item { border-bottom: 1px solid #e0e0e0; }")
        
        main_layout.addWidget(self.task_table)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self._on_edit_clicked)
        button_layout.addWidget(self.edit_button)
        
        self.complete_button = QPushButton("Complete")
        self.complete_button.setStyleSheet("""
            QPushButton {
                background-color: #43a047;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
            QPushButton:pressed {
                background-color: #2e7d32;
            }
        """)
        self.complete_button.clicked.connect(self._on_complete_clicked)
        button_layout.addWidget(self.complete_button)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e53935;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)
        self.delete_button.clicked.connect(self._on_delete_clicked)
        button_layout.addWidget(self.delete_button)
        
        main_layout.addLayout(button_layout)
    
    def _create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _on_item_double_clicked(self, item):
        row = item.row()
        task_id = int(self.task_table.item(row, 0).text())
        self.edit_task_requested.emit(task_id)
    
    def _on_edit_clicked(self):
        selected_rows = self.task_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            task_id = int(self.task_table.item(row, 0).text())
            self.edit_task_requested.emit(task_id)
    
    def _on_complete_clicked(self):
        selected_rows = self.task_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            task_id = int(self.task_table.item(row, 0).text())
            self.complete_task_requested.emit(task_id)
    
    def _on_delete_clicked(self):
        selected_rows = self.task_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            task_id = int(self.task_table.item(row, 0).text())
            self.delete_task_requested.emit(task_id)
    
    def update_tasks(self, tasks):
        self.task_table.setRowCount(0)
        
        for task in tasks:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            
            # ID column
            id_item = QTableWidgetItem(str(task.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.task_table.setItem(row_position, 0, id_item)
            
            # Title column
            title_item = QTableWidgetItem(task.title)
            if task.completed:
                font = title_item.font()
                font.setStrikeOut(True)
                title_item.setFont(font)
                title_item.setForeground(QColor("#9e9e9e"))  # Gray for completed tasks
            else:
                font = title_item.font()
                font.setBold(True)
                title_item.setFont(font)
            self.task_table.setItem(row_position, 1, title_item)
            
            # Due date column
            due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else "—"
            date_item = QTableWidgetItem(due_date)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Color code overdue tasks
            if not task.completed and task.due_date and task.due_date.date() < datetime.now().date():
                date_item.setForeground(QColor("#e53935"))  # Red for overdue
                date_item.setBackground(QColor("#ffebee"))  # Light red background
                font = date_item.font()
                font.setBold(True)
                date_item.setFont(font)
                
            self.task_table.setItem(row_position, 2, date_item)
            
            # Priority column
            priority_item = QTableWidgetItem(task.priority.name)
            priority_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Color code priorities with backgrounds instead of just text color
            if task.priority == Priority.HIGH:
                priority_item.setForeground(QColor("#ffffff"))
                priority_item.setBackground(QColor("#c62828"))  # Darker red background
            elif task.priority == Priority.MEDIUM:
                priority_item.setForeground(QColor("#ffffff"))
                priority_item.setBackground(QColor("#ef6c00"))  # Darker orange background
            elif task.priority == Priority.LOW:
                priority_item.setForeground(QColor("#ffffff"))
                priority_item.setBackground(QColor("#0277bd"))  # Darker blue background
            
            font = priority_item.font()
            font.setBold(True)
            priority_item.setFont(font)    
            self.task_table.setItem(row_position, 3, priority_item)
            
            # Status column
            status = "Completed" if task.completed else "Pending"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Add background colors for status
            if task.completed:
                status_item.setForeground(QColor("#ffffff"))
                status_item.setBackground(QColor("#2e7d32"))  # Darker green
            else:
                status_item.setForeground(QColor("#ffffff"))
                status_item.setBackground(QColor("#1565c0"))  # Darker blue
            
            font = status_item.font()
            font.setBold(True)
            status_item.setFont(font)
            self.task_table.setItem(row_position, 4, status_item)
        
        self.task_table.resizeColumnsToContents()
        self.task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    
    def update_status(self, message):
        self.status_bar.showMessage(message)

    def open_task_dialog(self, task=None):
        self.task_dialog = TaskDialog(self, task)
        return self.task_dialog.exec()
    
    def open_settings_dialog(self, settings, categories):
        self.settings_dialog = SettingsDialog(self, settings, categories)
        return self.settings_dialog.exec()
    
    def open_statistics_dialog(self, stats):
        self.statistics_dialog = StatisticsDialog(self, stats)
        return self.statistics_dialog.exec() 