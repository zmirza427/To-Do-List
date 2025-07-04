import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.messagebox import askyesno
import json
import os
from datetime import datetime, timedelta
import threading
import time

class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Advanced To-Do List Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Data management
        self.filename = "todos_gui.json"
        self.todos = self.load_todos()
        self.running = True
        self.reminder_thread = None
        
        # Color scheme
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
        self.setup_styles()
        self.create_widgets()
        self.refresh_task_list()
        self.start_reminder_system()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure custom styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Priority.High.TLabel', foreground='#e74c3c', font=('Arial', 10, 'bold'))
        style.configure('Priority.Medium.TLabel', foreground='#f39c12', font=('Arial', 10, 'bold'))
        style.configure('Priority.Low.TLabel', foreground='#27ae60', font=('Arial', 10, 'bold'))
        style.configure('Custom.Treeview', font=('Arial', 10))
        style.configure('Custom.Treeview.Heading', font=('Arial', 11, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main title
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, text="📝 Advanced To-Do List Manager", 
                               style='Title.TLabel')
        title_label.pack()
        
        # Create main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel for adding tasks
        left_panel = tk.LabelFrame(main_container, text="Add New Task", 
                                  font=('Arial', 11, 'bold'), bg='#f0f0f0')
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        
        self.create_add_task_section(left_panel)
        
        # Right panel for task list and controls
        right_panel = tk.Frame(main_container, bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.create_task_list_section(right_panel)
        self.create_control_buttons(right_panel)
        
        # Status bar
        self.create_status_bar()
    
    def create_add_task_section(self, parent):
        """Create the add task section."""
        # Task description
        tk.Label(parent, text="Task Description:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=5, pady=(5, 0))
        
        self.task_entry = tk.Text(parent, height=3, width=30, wrap='word',
                                 font=('Arial', 10))
        self.task_entry.pack(padx=5, pady=5, fill='x')
        
        # Priority selection
        tk.Label(parent, text="Priority:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w', padx=5)
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_frame = tk.Frame(parent, bg='#f0f0f0')
        priority_frame.pack(padx=5, pady=5, fill='x')
        
        for priority in ["High", "Medium", "Low"]:
            tk.Radiobutton(priority_frame, text=priority, variable=self.priority_var,
                          value=priority, bg='#f0f0f0', font=('Arial', 9)).pack(anchor='w')
        
        # Deadline section
        deadline_frame = tk.LabelFrame(parent, text="Deadline (Optional)", 
                                      font=('Arial', 10, 'bold'), bg='#f0f0f0')
        deadline_frame.pack(padx=5, pady=5, fill='x')
        
        # Date selection
        date_frame = tk.Frame(deadline_frame, bg='#f0f0f0')
        date_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(date_frame, text="Date:", bg='#f0f0f0').pack(side='left')
        self.date_entry = tk.Entry(date_frame, width=12, font=('Arial', 9))
        self.date_entry.pack(side='left', padx=(5, 0))
        self.date_entry.insert(0, "YYYY-MM-DD")
        
        # Time selection
        time_frame = tk.Frame(deadline_frame, bg='#f0f0f0')
        time_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(time_frame, text="Time:", bg='#f0f0f0').pack(side='left')
        self.time_entry = tk.Entry(time_frame, width=12, font=('Arial', 9))
        self.time_entry.pack(side='left', padx=(5, 0))
        self.time_entry.insert(0, "HH:MM (24h)")
        
        # Quick deadline buttons
        quick_frame = tk.Frame(deadline_frame, bg='#f0f0f0')
        quick_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Button(quick_frame, text="Today", command=lambda: self.set_quick_deadline("today"),
                 font=('Arial', 8), bg='#ecf0f1').pack(side='left', padx=1)
        tk.Button(quick_frame, text="Tomorrow", command=lambda: self.set_quick_deadline("tomorrow"),
                 font=('Arial', 8), bg='#ecf0f1').pack(side='left', padx=1)
        tk.Button(quick_frame, text="1 Week", command=lambda: self.set_quick_deadline("week"),
                 font=('Arial', 8), bg='#ecf0f1').pack(side='left', padx=1)
        
        # Add task button
        add_button = tk.Button(parent, text="➕ Add Task", command=self.add_task,
                              font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                              relief='flat', padx=20, pady=8)
        add_button.pack(pady=10)
        
        # Clear form button
        clear_button = tk.Button(parent, text="🗑️ Clear Form", command=self.clear_form,
                               font=('Arial', 10), bg='#95a5a6', fg='white',
                               relief='flat', padx=20, pady=5)
        clear_button.pack(pady=5)
    
    def create_task_list_section(self, parent):
        """Create the task list section."""
        # Filter frame
        filter_frame = tk.Frame(parent, bg='#f0f0f0')
        filter_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(filter_frame, text="Filter:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(side='left')
        
        self.filter_var = tk.StringVar(value="All Tasks")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                   values=["All Tasks", "Pending", "Completed", "Overdue", 
                                          "Due Today", "Due This Week"],
                                   state="readonly", font=('Arial', 9), width=15)
        filter_combo.pack(side='left', padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        # Search frame
        search_frame = tk.Frame(filter_frame, bg='#f0f0f0')
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(side='left')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=('Arial', 9), width=15)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_task_list())
        
        # Task list with scrollbar
        list_frame = tk.Frame(parent, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True)
        
        # Create Treeview
        columns = ('ID', 'Task', 'Priority', 'Deadline', 'Status', 'Time Left')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings',
                                     style='Custom.Treeview', height=15)
        
        # Configure columns
        self.task_tree.heading('ID', text='ID')
        self.task_tree.heading('Task', text='Task Description')
        self.task_tree.heading('Priority', text='Priority')
        self.task_tree.heading('Deadline', text='Deadline')
        self.task_tree.heading('Status', text='Status')
        self.task_tree.heading('Time Left', text='Time Remaining')
        
        self.task_tree.column('ID', width=40, minwidth=40)
        self.task_tree.column('Task', width=200, minwidth=150)
        self.task_tree.column('Priority', width=80, minwidth=60)
        self.task_tree.column('Deadline', width=120, minwidth=100)
        self.task_tree.column('Status', width=80, minwidth=60)
        self.task_tree.column('Time Left', width=120, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.task_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.task_tree.xview)
        
        self.task_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and treeview
        self.task_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind double-click to edit
        self.task_tree.bind('<Double-1>', self.edit_task)
    
    def create_control_buttons(self, parent):
        """Create control buttons."""
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=10)
        
        # Left side buttons
        left_buttons = tk.Frame(button_frame, bg='#f0f0f0')
        left_buttons.pack(side='left')
        
        complete_btn = tk.Button(left_buttons, text="✅ Complete Task", 
                               command=self.complete_task,
                               font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                               relief='flat', padx=15, pady=5)
        complete_btn.pack(side='left', padx=2)
        
        edit_btn = tk.Button(left_buttons, text="✏️ Edit Task", 
                           command=self.edit_task,
                           font=('Arial', 10, 'bold'), bg='#f39c12', fg='white',
                           relief='flat', padx=15, pady=5)
        edit_btn.pack(side='left', padx=2)
        
        delete_btn = tk.Button(left_buttons, text="🗑️ Delete Task", 
                             command=self.delete_task,
                             font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                             relief='flat', padx=15, pady=5)
        delete_btn.pack(side='left', padx=2)
        
        # Right side buttons
        right_buttons = tk.Frame(button_frame, bg='#f0f0f0')
        right_buttons.pack(side='right')
        
        deadline_btn = tk.Button(right_buttons, text="📅 Set Deadline", 
                               command=self.set_deadline_dialog,
                               font=('Arial', 10, 'bold'), bg='#9b59b6', fg='white',
                               relief='flat', padx=15, pady=5)
        deadline_btn.pack(side='left', padx=2)
        
        refresh_btn = tk.Button(right_buttons, text="🔄 Refresh", 
                              command=self.refresh_task_list,
                              font=('Arial', 10, 'bold'), bg='#34495e', fg='white',
                              relief='flat', padx=15, pady=5)
        refresh_btn.pack(side='left', padx=2)
    
    def create_status_bar(self):
        """Create status bar at the bottom."""
        self.status_frame = tk.Frame(self.root, bg='#2c3e50', relief='sunken', bd=1)
        self.status_frame.pack(side='bottom', fill='x')
        
        self.status_label = tk.Label(self.status_frame, text="Ready", 
                                   bg='#2c3e50', fg='white', font=('Arial', 9),
                                   anchor='w')
        self.status_label.pack(side='left', padx=5, pady=2)
        
        # Task count label
        self.count_label = tk.Label(self.status_frame, text="", 
                                  bg='#2c3e50', fg='white', font=('Arial', 9),
                                  anchor='e')
        self.count_label.pack(side='right', padx=5, pady=2)
        
        # Reminder indicator
        self.reminder_label = tk.Label(self.status_frame, text="🔔 Reminders Active", 
                                     bg='#2c3e50', fg='#f39c12', font=('Arial', 9))
        self.reminder_label.pack(side='right', padx=10, pady=2)
    
    def load_todos(self):
        """Load todos from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_todos(self):
        """Save todos to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.todos, f, indent=2)
        except IOError:
            messagebox.showerror("Error", "Could not save tasks to file.")
    
    def get_next_id(self):
        """Get the next available ID."""
        if not self.todos:
            return 1
        return max(task.get('id', 0) for task in self.todos) + 1
    
    def set_quick_deadline(self, period):
        """Set quick deadline in the form."""
        now = datetime.now()
        if period == "today":
            deadline = now.replace(hour=23, minute=59, second=0, microsecond=0)
        elif period == "tomorrow":
            deadline = (now + timedelta(days=1)).replace(hour=23, minute=59, second=0, microsecond=0)
        elif period == "week":
            deadline = (now + timedelta(days=7)).replace(hour=23, minute=59, second=0, microsecond=0)
        
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, deadline.strftime("%Y-%m-%d"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, deadline.strftime("%H:%M"))
    
    def clear_form(self):
        """Clear the add task form."""
        self.task_entry.delete(1.0, tk.END)
        self.priority_var.set("Medium")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "HH:MM (24h)")
        self.update_status("Form cleared")
    
    def parse_deadline(self, date_str, time_str):
        """Parse deadline from date and time strings."""
        if (not date_str or date_str == "YYYY-MM-DD" or 
            not time_str or time_str == "HH:MM (24h)"):
            return None
        
        try:
            if time_str and time_str != "HH:MM (24h)":
                datetime_str = f"{date_str} {time_str}"
                return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            else:
                return datetime.strptime(date_str, "%Y-%m-%d").replace(hour=23, minute=59)
        except ValueError:
            return None
    
    def add_task(self):
        """Add a new task."""
        description = self.task_entry.get(1.0, tk.END).strip()
        if not description:
            messagebox.showwarning("Warning", "Please enter a task description.")
            return
        
        priority = self.priority_var.get().lower()
        deadline = self.parse_deadline(self.date_entry.get(), self.time_entry.get())
        
        task = {
            "id": self.get_next_id(),
            "description": description,
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "priority": priority,
            "deadline": deadline.strftime("%Y-%m-%d %H:%M:%S") if deadline else None,
            "reminded": False
        }
        
        self.todos.append(task)
        self.save_todos()
        self.clear_form()
        self.refresh_task_list()
        self.update_status(f"Added task: {description[:30]}...")
    
    def get_selected_task(self):
        """Get the currently selected task."""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task.")
            return None
        
        item = self.task_tree.item(selection[0])
        task_id = int(item['values'][0])
        
        for task in self.todos:
            if task['id'] == task_id:
                return task
        return None
    
    def complete_task(self):
        """Mark selected task as completed."""
        task = self.get_selected_task()
        if not task:
            return
        
        if task['completed']:
            messagebox.showinfo("Info", "Task is already completed.")
            return
        
        task['completed'] = True
        task['completed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_todos()
        self.refresh_task_list()
        self.update_status(f"Completed task: {task['description'][:30]}...")
    
    def delete_task(self):
        """Delete selected task."""
        task = self.get_selected_task()
        if not task:
            return
        
        if askyesno("Confirm Delete", f"Are you sure you want to delete:\n'{task['description']}'?"):
            self.todos.remove(task)
            self.save_todos()
            self.refresh_task_list()
            self.update_status(f"Deleted task: {task['description'][:30]}...")
    
    def edit_task(self, event=None):
        """Edit selected task."""
        task = self.get_selected_task()
        if not task:
            return
        
        # Create edit dialog
        dialog = EditTaskDialog(self.root, task)
        if dialog.result:
            updated_task = dialog.result
            # Update the task in the list
            for i, t in enumerate(self.todos):
                if t['id'] == task['id']:
                    self.todos[i] = updated_task
                    break
            
            self.save_todos()
            self.refresh_task_list()
            self.update_status(f"Updated task: {updated_task['description'][:30]}...")
    
    def set_deadline_dialog(self):
        """Show deadline setting dialog."""
        task = self.get_selected_task()
        if not task:
            return
        
        dialog = DeadlineDialog(self.root, task.get('deadline'))
        if dialog.result:
            if dialog.result == "remove":
                task['deadline'] = None
            else:
                task['deadline'] = dialog.result
            
            task['reminded'] = False  # Reset reminder flag
            self.save_todos()
            self.refresh_task_list()
            self.update_status("Deadline updated")

    def get_time_remaining(self, deadline_str):
        """Calculate time remaining until deadline."""
        if not deadline_str:
            return ""
        
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = deadline - now
        
        if diff.total_seconds() < 0:
            days_overdue = abs(diff.days)
            return f"OVERDUE {days_overdue}d"
        elif diff.days > 0:
            return f"{diff.days}d left"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}h left"
        else:
            minutes = diff.seconds // 60
            return f"{minutes}m left"
    
    def filter_tasks(self, tasks):
        """Filter tasks based on current filter and search."""
        filter_type = self.filter_var.get()
        search_query = self.search_var.get().lower()
        
        # Apply search filter
        if search_query:
            tasks = [t for t in tasks if search_query in t['description'].lower()]
        
        # Apply type filter
        now = datetime.now()
        if filter_type == "Pending":
            tasks = [t for t in tasks if not t['completed']]
        elif filter_type == "Completed":
            tasks = [t for t in tasks if t['completed']]
        elif filter_type == "Overdue":
            tasks = [t for t in tasks if not t['completed'] and t.get('deadline') and 
                    datetime.strptime(t['deadline'], "%Y-%m-%d %H:%M:%S") < now]
        elif filter_type == "Due Today":
            today = now.date()
            tasks = [t for t in tasks if not t['completed'] and t.get('deadline') and 
                    datetime.strptime(t['deadline'], "%Y-%m-%d %H:%M:%S").date() == today]
        elif filter_type == "Due This Week":
            week_end = now + timedelta(days=7)
            tasks = [t for t in tasks if not t['completed'] and t.get('deadline') and 
                    datetime.strptime(t['deadline'], "%Y-%m-%d %H:%M:%S") <= week_end]
        
        return tasks
    
    def refresh_task_list(self):
        """Refresh the task list display."""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Filter tasks
        filtered_tasks = self.filter_tasks(self.todos)
        
        # Sort tasks (pending first, then by deadline)
        def sort_key(task):
            if task['completed']:
                return (2, task.get('completed_date', ''))
            if not task.get('deadline'):
                return (1, datetime.max)
            deadline = datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M:%S")
            if deadline < datetime.now():
                return (0, deadline)  # Overdue first
            return (1, deadline)
        
        filtered_tasks.sort(key=lambda t: t['id'])
        
        # Populate tree
        for task in filtered_tasks:
            task_id = task['id']
            description = task['description']
            priority = task['priority'].title()
            deadline = task.get('deadline', '')
            if deadline:
                deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S").strftime("%m/%d %H:%M")
            
            status = "✅ Done" if task['completed'] else "⏳ Pending"
            time_left = "" if task['completed'] else self.get_time_remaining(task.get('deadline'))
            
            # Insert item
            item = self.task_tree.insert('', 'end', values=(
                task_id, description, priority, deadline, status, time_left
            ))
            
            # Color coding
            if task['completed']:
                self.task_tree.set(item, 'Task', f"✅ {description}")
            elif task.get('deadline') and datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M:%S") < datetime.now():
                self.task_tree.set(item, 'Task', f"⚠️ {description}")
            elif task['priority'] == 'high':
                self.task_tree.set(item, 'Task', f"🔴 {description}")
            elif task['priority'] == 'medium':
                self.task_tree.set(item, 'Task', f"🟡 {description}")
            else:
                self.task_tree.set(item, 'Task', f"🟢 {description}")
        
        # Update status
        self.update_task_count()
    
    def update_task_count(self):
        """Update task count in status bar."""
        total = len(self.todos)
        pending = len([t for t in self.todos if not t['completed']])
        completed = len([t for t in self.todos if t['completed']])
        overdue = len([t for t in self.todos if not t['completed'] and t.get('deadline') and 
                      datetime.strptime(t['deadline'], "%Y-%m-%d %H:%M:%S") < datetime.now()])
        
        count_text = f"Total: {total} | Pending: {pending} | Completed: {completed}"
        if overdue > 0:
            count_text += f" | ⚠️ Overdue: {overdue}"
        
        self.count_label.config(text=count_text)
    
    def update_status(self, message):
        """Update status bar message."""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))
    
    def check_reminders(self):
        """Check for tasks that need reminders."""
        now = datetime.now()
        reminders = []
        
        for task in self.todos:
            if (not task['completed'] and 
                task.get('deadline') and 
                not task.get('reminded', False)):
                
                deadline = datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M:%S")
                time_diff = deadline - now
                
                # Send reminder if deadline is within 2 hours or overdue
                if time_diff.total_seconds() <= 7200:  # 2 hours
                    reminders.append(task)
                    task['reminded'] = True
        
        if reminders:
            self.save_todos()
            self.show_reminders(reminders)
        
        return reminders
    
    def show_reminders(self, reminders):
        """Show reminder popup."""
        reminder_text = "🔔 DEADLINE REMINDERS:\n\n"
        for task in reminders:
            time_info = self.get_time_remaining(task['deadline'])
            reminder_text += f"• {task['description']}\n  {time_info}\n\n"
        
        messagebox.showwarning("Deadline Reminders", reminder_text)
        self.refresh_task_list()
    
    def start_reminder_system(self):
        """Start the background reminder system."""
        def reminder_loop():
            while self.running:
                try:
                    self.check_reminders()
                    # Check every 10 minutes
                    for _ in range(600):
                        if not self.running:
                            break
                        time.sleep(1)
                except Exception as e:
                    print(f"Reminder system error: {e}")
                    time.sleep(60)
        
        self.reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
        self.reminder_thread.start()
    
    def on_closing(self):
        """Handle application closing."""
        self.running = False
        if self.reminder_thread:
            self.reminder_thread.join(timeout=1)
        self.root.destroy()


class EditTaskDialog(simpledialog.Dialog):
    def __init__(self, parent, task):
        self.task = task
        self.result = None
        super().__init__(parent, title="Edit Task")

    def body(self, master):
        tk.Label(master, text="Description:").grid(row=0, column=0, sticky="w")
        self.desc_entry = tk.Text(master, height=3, width=40)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)
        self.desc_entry.insert("1.0", self.task['description'])

        tk.Label(master, text="Priority:").grid(row=1, column=0, sticky="w")
        self.priority_var = tk.StringVar(value=self.task.get('priority', 'medium').capitalize())
        priorities = ["High", "Medium", "Low"]
        self.priority_combo = ttk.Combobox(master, textvariable=self.priority_var, values=priorities, state="readonly")
        self.priority_combo.grid(row=1, column=1, padx=5, pady=5)

        return self.desc_entry

    def apply(self):
        description = self.desc_entry.get("1.0", "end").strip()
        priority = self.priority_var.get().lower()
        updated_task = self.task.copy()
        updated_task['description'] = description
        updated_task['priority'] = priority
        self.result = updated_task
    
class DeadlineDialog(simpledialog.Dialog):
    def __init__(self, parent, current_deadline):
        self.result = None
        self.current_deadline = current_deadline
        super().__init__(parent, title="Set Deadline")

    def body(self, master):
        tk.Label(master, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=0, column=0, sticky="w")
        self.deadline_entry = tk.Entry(master, width=25)
        self.deadline_entry.grid(row=0, column=1, padx=5, pady=5)
        if self.current_deadline:
            # Show only up to minutes for editing
            try:
                dt = datetime.strptime(self.current_deadline, "%Y-%m-%d %H:%M:%S")
                self.deadline_entry.insert(0, dt.strftime("%Y-%m-%d %H:%M"))
            except Exception:
                self.deadline_entry.insert(0, self.current_deadline)
        return self.deadline_entry

    def buttonbox(self):
        box = tk.Frame(self)
        tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(box, text="Remove", width=10, command=self.remove_deadline).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(box, text="Cancel", width=10, command=self.cancel).pack(side=tk.LEFT, padx=5, pady=5)
        box.pack()

    def validate(self):
        value = self.deadline_entry.get().strip()
        if not value:
            return True  # Allow empty (user may want to remove)
        try:
            # Try to parse as "YYYY-MM-DD HH:MM"
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            messagebox.showerror("Invalid format", "Please enter deadline as YYYY-MM-DD HH:MM")
            return False

    def apply(self):
        value = self.deadline_entry.get().strip()
        if not value:
            self.result = None
        else:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
            self.result = dt.strftime("%Y-%m-%d %H:%M:%S")

    def remove_deadline(self):
        self.result = "remove"
        self.ok()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()