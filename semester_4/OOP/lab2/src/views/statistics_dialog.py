from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                          QGroupBox, QGridLayout, QDialogButtonBox, QTabWidget,
                          QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis


class StatisticsDialog(QDialog):
    def __init__(self, parent=None, stats=None):
        super().__init__(parent)
        
        self.stats = stats or {}
        
        self.setWindowTitle("Task Statistics")
        self.setMinimumSize(600, 500)
        
        self._create_layout()
    
    def _create_layout(self):
        layout = QVBoxLayout(self)
        
        # Create tabs
        tab_widget = QTabWidget()
        
        # Overview tab
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        
        # Task counts group
        counts_group = QGroupBox("Task Counts")
        counts_layout = QGridLayout(counts_group)
        
        # Total tasks
        counts_layout.addWidget(QLabel("Total tasks:"), 0, 0)
        counts_layout.addWidget(QLabel(str(self.stats.get("total", 0))), 0, 1)
        
        # Completed tasks
        counts_layout.addWidget(QLabel("Completed:"), 1, 0)
        counts_layout.addWidget(QLabel(str(self.stats.get("completed", 0))), 1, 1)
        
        # Pending tasks
        counts_layout.addWidget(QLabel("Pending:"), 2, 0)
        counts_layout.addWidget(QLabel(str(self.stats.get("pending", 0))), 2, 1)
        
        # Overdue tasks
        counts_layout.addWidget(QLabel("Overdue:"), 3, 0)
        counts_layout.addWidget(QLabel(str(self.stats.get("overdue", 0))), 3, 1)
        
        overview_layout.addWidget(counts_group)
        
        # Priority counts group
        priority_group = QGroupBox("Tasks by Priority")
        priority_layout = QGridLayout(priority_group)
        
        priority_layout.addWidget(QLabel("High Priority:"), 0, 0)
        priority_layout.addWidget(QLabel(str(self.stats.get("high_priority", 0))), 0, 1)
        
        priority_layout.addWidget(QLabel("Medium Priority:"), 1, 0)
        priority_layout.addWidget(QLabel(str(self.stats.get("medium_priority", 0))), 1, 1)
        
        priority_layout.addWidget(QLabel("Low Priority:"), 2, 0)
        priority_layout.addWidget(QLabel(str(self.stats.get("low_priority", 0))), 2, 1)
        
        overview_layout.addWidget(priority_group)
        
        # Completion rate
        completion_group = QGroupBox("Completion Rate")
        completion_layout = QVBoxLayout(completion_group)
        
        rate = self.stats.get("completion_rate", 0)
        rate_label = QLabel(f"{rate:.1f}%")
        rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rate_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        completion_layout.addWidget(rate_label)
        
        overview_layout.addWidget(completion_group)
        
        # Charts tab
        charts_tab = QWidget()
        charts_layout = QVBoxLayout(charts_tab)
        
        # Status pie chart
        pie_chart = QChart()
        pie_chart.setTitle("Tasks by Status")
        
        series = QPieSeries()
        
        # Add slices
        completed = self.stats.get("completed", 0)
        pending = self.stats.get("pending", 0)
        
        if completed > 0:
            completed_slice = series.append("Completed", completed)
            completed_slice.setBrush(QColor("#4CAF50"))  # Green
        
        if pending > 0:
            pending_slice = series.append("Pending", pending)
            pending_slice.setBrush(QColor("#2196F3"))  # Blue

        if pending > 0 and self.stats.get("overdue", 0) > 0:
            # Show overdue as part of pending
            overdue = self.stats.get("overdue", 0)
            if overdue > 0:
                overdue_slice = series.append("Overdue", overdue)
                overdue_slice.setBrush(QColor("#F44336"))  # Red
                
        pie_chart.addSeries(series)
        pie_chart.legend().setVisible(True)
        
        chart_view = QChartView(pie_chart)
        chart_view.setRenderHint(chart_view.RenderHint.Antialiasing)
        charts_layout.addWidget(chart_view)
        
        # Priority bar chart
        bar_chart = QChart()
        bar_chart.setTitle("Tasks by Priority")
        
        bar_set = QBarSet("Number of Tasks")
        bar_set.append([
            self.stats.get("high_priority", 0),
            self.stats.get("medium_priority", 0),
            self.stats.get("low_priority", 0)
        ])
        
        bar_series = QBarSeries()
        bar_series.append(bar_set)
        
        bar_chart.addSeries(bar_series)
        
        categories = ["High", "Medium", "Low"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        bar_chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        bar_series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        max_value = max([
            self.stats.get("high_priority", 0),
            self.stats.get("medium_priority", 0),
            self.stats.get("low_priority", 0)
        ])
        axis_y.setRange(0, max(1, max_value + 1))  # Avoid range 0-0
        bar_chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        bar_series.attachAxis(axis_y)
        
        bar_chart.legend().setVisible(False)
        
        bar_chart_view = QChartView(bar_chart)
        bar_chart_view.setRenderHint(bar_chart_view.RenderHint.Antialiasing)
        charts_layout.addWidget(bar_chart_view)
        
        # Add tabs to widget
        tab_widget.addTab(overview_tab, "Overview")
        tab_widget.addTab(charts_tab, "Charts")
        
        layout.addWidget(tab_widget)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box) 