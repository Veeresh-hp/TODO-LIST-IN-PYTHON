import tkinter as tk
from tkinter import messagebox
import sqlite3

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("665x400+550+250")
        self.root.resizable(False, False)
        self.root.configure(bg="#B5E5CF")

        # Database Connection
        self.conn = sqlite3.connect("listOfTasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (title TEXT)")

        self.tasks = []
        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        """Sets up the UI components"""
        frame = tk.Frame(self.root, bg="#8EE5EE")
        frame.pack(side="top", expand=True, fill="both")

        tk.Label(frame, text="TO-DO LIST\nEnter Task Title:", font=("Arial", 14, "bold"), bg="#8EE5EE", fg="#FF6103").place(x=20, y=30)
        self.task_entry = tk.Entry(frame, font=("Arial", 14), width=42, bg="white", fg="black")
        self.task_entry.place(x=180, y=30)

        # Buttons
        tk.Button(frame, text="Add", width=15, bg="#D4AC0D", font=("Arial", 14, "bold"), command=self.add_task).place(x=18, y=80)
        tk.Button(frame, text="Remove", width=15, bg="#D4AC0D", font=("Arial", 14, "bold"), command=self.delete_task).place(x=240, y=80)
        tk.Button(frame, text="Delete All", width=15, bg="#D4AC0D", font=("Arial", 14, "bold"), command=self.delete_all_tasks).place(x=460, y=80)

        # Listbox
        self.task_listbox = tk.Listbox(frame, width=70, height=9, font="bold", selectmode='SINGLE', bg="white", fg="black",
                                       selectbackground="#FF8C00", selectforeground="black")
        self.task_listbox.place(x=17, y=140)

        # Exit Button at Bottom
        exit_frame = tk.Frame(self.root, bg="#8EE5EE")
        exit_frame.pack(side="bottom", fill="x", pady=5)
        tk.Button(exit_frame, text="Exit / Close", width=52, bg="#D4AC0D", font=("Arial", 14, "bold"), command=self.close_app).pack(pady=5)

    def add_task(self):
        """Adds a new task to the list and database"""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showerror("Error", "Task cannot be empty!")
            return

        if task_text in self.tasks:
            messagebox.showwarning("Warning", "Task already exists!")
            return

        self.tasks.append(task_text)
        self.cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task_text,))
        self.conn.commit()
        self.update_list()
        self.task_entry.delete(0, tk.END)

    def delete_task(self):
        """Deletes the selected task"""
        try:
            selected_index = self.task_listbox.curselection()
            if not selected_index:
                messagebox.showinfo("Error", "No task selected!")
                return

            task_text = self.task_listbox.get(selected_index)
            self.tasks.remove(task_text)
            self.cursor.execute("DELETE FROM tasks WHERE title = ?", (task_text,))
            self.conn.commit()
            self.update_list()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_all_tasks(self):
        """Deletes all tasks"""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?")
        if confirm:
            self.tasks.clear()
            self.cursor.execute("DELETE FROM tasks")
            self.conn.commit()
            self.update_list()

    def update_list(self):
        """Refreshes the task list in the UI"""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def load_tasks(self):
        """Loads tasks from the database into the list"""
        self.cursor.execute("SELECT title FROM tasks")
        rows = self.cursor.fetchall()
        self.tasks = [row[0] for row in rows]
        self.update_list()

    def close_app(self):
        """Closes the application and commits changes"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
