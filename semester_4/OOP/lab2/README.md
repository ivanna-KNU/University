# Task Manager Application

A PyQt6-based task management application with a clean separation between UI and business logic.

## Features

- Task management (add, edit, complete, delete)
- Task filtering (all, pending, completed, by priority, overdue)
- Task statistics with charts
- Settings management
- Category management

## Requirements

- Python 3.6+
- PyQt6

## Installation

1. Install the required dependencies:

```
pip install -r requirements.txt
```

## Running the Application

To run the application, execute:

```
python main.py
```

## Application Structure

The application follows the Model-View-Controller (MVC) architecture:

- **Models**: Contains the data models (Task, TaskManager)
- **Views**: Contains the UI components (MainWindow, TaskDialog, SettingsDialog, StatisticsDialog)
- **Controllers**: Contains the business logic (TaskController)

## Screenshots

The application has four main screens:
- Main window with task list
- Task add/edit dialog
- Settings dialog
- Statistics dialog with charts 