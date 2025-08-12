import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class ReminderTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager with Reminder")
        self.root.geometry("480x580")
        self.root.configure(bg="#f4f6f7")

        self.tasks = []
        self.data_file = "tasks.json"
        self.load_tasks()

        # ====== Clock ======
        self.clock_label = tk.Label(root, font=("Arial", 12, "bold"), bg="#f4f6f7", fg="#2c3e50")
        self.clock_label.pack(pady=5)
        self.update_clock()

        # ====== Title ======
        tk.Label(root, text=" Task Manager with Reminders", font=("Arial", 16, "bold"),
                 bg="#f4f6f7", fg="#2c3e50").pack(pady=10)

        # ====== Input Frame ======
        input_frame = tk.Frame(root, bg="#f4f6f7")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Task:", bg="#f4f6f7").grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(input_frame, width=28)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Priority:", bg="#f4f6f7").grid(row=1, column=0, sticky="w")
        self.priority_var = tk.StringVar(value="Medium")
        tk.OptionMenu(input_frame, self.priority_var, "High", "Medium", "Low").grid(row=1, column=1, sticky="w")

        tk.Label(input_frame, text="Reminder Time (HH:MM):", bg="#f4f6f7").grid(row=2, column=0, sticky="w")
        self.reminder_entry = tk.Entry(input_frame, width=10)
        self.reminder_entry.insert(0, "HH:MM")
        self.reminder_entry.grid(row=2, column=1, sticky="w")

        tk.Button(input_frame, text=" Add Task", command=self.add_task,
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"), relief="flat").grid(row=3, columnspan=2, pady=5)

        # ====== Task List ======
        self.task_listbox = tk.Listbox(root, width=50, height=12, font=("Arial", 10),
                                       selectbackground="#a29bfe", selectforeground="black")
        self.task_listbox.pack(pady=5)

        # ====== Buttons ======
        btn_frame = tk.Frame(root, bg="#f4f6f7")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text=" Complete", command=self.complete_task,
                  bg="#2980b9", fg="white", width=10, relief="flat").grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text=" Delete", command=self.delete_task,
                  bg="#c0392b", fg="white", width=10, relief="flat").grid(row=0, column=1, padx=5)

        tk.Button(root, text=" Save Tasks", command=self.save_tasks,
                  bg="#8e44ad", fg="white", width=15, relief="flat").pack(pady=3)

        tk.Button(root, text=" Load Tasks", command=self.load_tasks,
                  bg="#16a085", fg="white", width=15, relief="flat").pack(pady=3)

    # ====== Clock & Reminder Check ======
    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        self.clock_label.config(text=now)

        # Check reminders
        current_time = datetime.now().strftime("%H:%M")
        for task in self.tasks:
            if task.get("reminder") == current_time and task.get("status") == "Pending":
                messagebox.showinfo(" Reminder", f"Time for task: {task['description']}")
                task["reminder"] = ""  # Clear so it doesn’t repeat

        self.root.after(1000, self.update_clock)

    # ====== Core Functions ======
    def add_task(self):
        task = self.task_entry.get().strip()
        reminder_time = self.reminder_entry.get().strip()

        if not task:
            messagebox.showwarning("Warning", "Enter a task!")
            return

        if reminder_time and reminder_time != "HH:MM":
            try:
                datetime.strptime(reminder_time, "%H:%M")
            except ValueError:
                messagebox.showerror("Error", "Reminder time must be in HH:MM format!")
                return
        else:
            reminder_time = ""

        self.tasks.append({
            "description": task,
            "priority": self.priority_var.get(),
            "status": "Pending",
            "reminder": reminder_time,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        self.task_entry.delete(0, tk.END)
        self.reminder_entry.delete(0, tk.END)
        self.reminder_entry.insert(0, "HH:MM")
        self.refresh_list()

    def complete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a task!")
            return
        self.tasks[selection[0]]["status"] = "Completed"
        self.refresh_list()

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a task!")
            return
        del self.tasks[selection[0]]
        self.refresh_list()

    def refresh_list(self):
        self.task_listbox.delete(0, tk.END)
        for t in self.tasks:
            emoji = "✅" if t["status"] == "Completed" else "🕒"
            reminder_info = f" - {t['reminder']}" if t["reminder"] else ""
            display = f"{emoji} {t['description']} ({t['priority']}){reminder_info}"
            self.task_listbox.insert(tk.END, display)

    def save_tasks(self):
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, indent=2)
        messagebox.showinfo("Success", "Tasks saved!")

    def load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.tasks = json.load(f)
            self.refresh_list()


# ====== Run App ======
if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderTaskManager(root)
    root.mainloop()
