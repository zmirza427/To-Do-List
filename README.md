📝 Advanced To-Do List Manager
A comprehensive Python GUI application for task management built with tkinter. This feature-rich to-do list manager helps you organize tasks with priorities, deadlines, and smart notifications.
✨ Features
Core Functionality

Task Management: Add, edit, delete, and complete tasks with detailed descriptions
Priority Levels: Organize tasks by High, Medium, or Low priority
Deadline Tracking: Set specific deadlines with date and time
Status Tracking: Monitor pending vs completed tasks

Smart Organization

Advanced Filtering: Filter by All Tasks, Pending, Completed, Overdue, Due Today, Due This Week
Search Functionality: Quickly find tasks by description
Automatic Sorting: Tasks organized by priority and deadline
Time Remaining: Visual countdown to deadlines

Notifications & Reminders

Overdue Alerts: Automatic detection of overdue tasks
Deadline Reminders: Pop-up notifications for approaching deadlines
Background Monitoring: Continuous reminder system running in background
Visual Indicators: Color-coded task status and priority levels

User Interface

Clean Design: Modern, intuitive interface with custom styling
Quick Actions: One-click buttons for common operations
Bulk Operations: Edit multiple aspects of tasks efficiently
Status Bar: Real-time task counts and system status

🚀 Installation
Prerequisites

Python 3.6 or higher
tkinter (usually included with Python)

Run the application:

bashpython todo_gui.py
📖 Usage
Adding Tasks

Enter task description in the text area
Select priority level (High/Medium/Low)
Optionally set a deadline using:

Manual date/time entry
Quick deadline buttons (Today, Tomorrow, 1 Week)


Click "Add Task"

Managing Tasks

Complete: Select a task and click "Complete Task"
Edit: Double-click a task or use "Edit Task" button
Delete: Select a task and click "Delete Task"
Set Deadline: Use "Set Deadline" button for existing tasks

Filtering and Search

Use the filter dropdown to view specific task categories
Use the search bar to find tasks by description
Tasks are automatically sorted by status and deadline

Reminders

The application automatically checks for upcoming deadlines
Reminders appear 2 hours before deadline
Overdue tasks are highlighted in red

🎯 Quick Start Example

Add a high-priority task:

Description: "Complete project presentation"
Priority: High
Deadline: Tomorrow at 9:00 AM


Filter tasks:

Select "Due Today" to see today's tasks
Use search to find specific tasks


Complete tasks:

Select completed tasks and mark as done
View completed tasks using the "Completed" filter



💾 Data Storage

Tasks are automatically saved to todos_gui.json
Data persists between application sessions
JSON format allows easy data portability

🎨 Interface Overview

Left Panel: Task creation form with priority and deadline options
Right Panel: Task list with filtering, search, and management controls
Status Bar: Real-time task counts and system status
Color Coding: Visual priority and status indicators

🛠️ Technical Details
Built With

Python: Core programming language
tkinter: GUI framework
JSON: Data storage format
Threading: Background reminder system

Key Components

TodoGUI: Main application class
EditTaskDialog: Task editing interface
DeadlineDialog: Deadline management interface
Background reminder system with threading

🔧 Customization
Styling

Colors can be modified in the colors dictionary
Custom styles defined in setup_styles() method
Font sizes and families easily adjustable

Reminder Settings

Reminder timing can be changed in check_reminders() method
Currently set to 2 hours before deadline
Background check interval: 10 minutes

📝 File Structure
advanced-todo-manager/
├── todo_gui.py           # Main application file
├── todos_gui.json        # Data storage (created automatically)
└── README.md            # This file

🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

📋 Future Enhancements

 Task categories and tags
 Recurring tasks
 Export/import functionality
 Dark mode theme
 Calendar integration
 Task notes and attachments
 Productivity statistics

🐛 Known Issues

Reminder system requires application to be running
Large task lists may affect performance
No network synchronization

📄 License
This project is open source and available under the MIT License.
👨‍💻 Author
Created with ❤️ by M Zaeem Mughal

⭐ Star this repository if you find it helpful!
