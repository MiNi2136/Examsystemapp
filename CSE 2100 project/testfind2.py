import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from tkinter import simpledialog

# File to store user data
USER_DATA_FILE = "user_data.json"
USER_DATA_FILE = "exams_data.json"

# Function to initialize user data file if not exists or not properly structured
def initialize_user_data_file():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as file:
            json.dump({"students": {}, "teachers": {}}, file)
    else:
        with open(USER_DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError("Data is not a dictionary")
                if "students" not in data or "teachers" not in data:
                    raise ValueError("Invalid data structure")
            except (json.JSONDecodeError, ValueError):
                with open(USER_DATA_FILE, 'w') as file:
                    json.dump({"students": {}, "teachers": {}}, file)

# Function to load user data
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save user data
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

class ExamSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Local Exam System")
        self.geometry("1280x720")
        self.current_user = None
        self.current_role = None
        self.current_exam = None
        self.background_image = tk.PhotoImage(file=r"C:\Users\User\Desktop\CSE 2100 project\img\checklist-7325314_1280.png")
        self.option_font_size = 12  # Default font size
        self.total_marks = 0  # Total marks of the student
        self.questions = []  # List to store questions
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()

        # Create a canvas to hold the background image
        canvas = tk.Canvas(self, width=1280, height=720)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        
        title_label = tk.Label(self, text="Local Exam System", bg="green", fg="white", font=("arial", 23, "bold"))
        canvas.create_window(640, 100, window=title_label)  # Place in the center top
        
        login_button = tk.Button(self, text="Login", command=self.show_login, bg="green", fg="white", font=("arial", 18, "bold"))
        canvas.create_window(640, 200, window=login_button)  # Place in the center
        
        signup_button = tk.Button(self, text="Sign Up", command=self.show_signup, bg="green", fg="white", font=("arial", 18, "bold"))
        canvas.create_window(640, 300, window=signup_button)  # Place in the center

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        
        tk.Label(self, text="Login", bg="green", fg="white", font=("arial", 25, "bold")).pack(pady=16)
        tk.Label(self, text="Username", bg="white", fg="green", font=("arial", 20, "bold")).pack(pady=5)
        username_entry = tk.Entry(self,width=26, font=("Arial", 18))
        username_entry.pack()
        
        tk.Label(self, text="Password", bg="white", fg="green", font=("arial", 20, "bold")).pack(pady=5)
        password_entry = tk.Entry(self, show='*',width=26, font=("Arial", 18))
        password_entry.pack()
        
        tk.Label(self, text="Role", bg="white", fg="green", font=("arial", 20, "bold")).pack(pady=5)
        role_combobox = ttk.Combobox(self, values=["student", "teacher"],width=24, font=("Arial", 16))
        role_combobox.pack()
        role_combobox.current(0)  # Default to "student"
        
        def login():
            username = username_entry.get()
            password = password_entry.get()
            role = role_combobox.get().lower()
            if self.verify_login(username, password, role):
                self.current_user = username
                self.current_role = role
                messagebox.showinfo("Login", f"Welcome {username}!")
                self.show_dashboard()
            else:
                messagebox.showerror("Login", "Invalid credentials or role.")
        
        tk.Button(self, text="Login", command=login, bg="green", fg="white", font=("arial", 14, "bold")).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_main_menu, bg="green", fg="white",font=("arial", 12, "bold")).pack()

    def show_signup(self):
        self.clear_window()
        
        tk.Label(self, text="Sign Up", bg="green", fg="white", font=("arial", 24, "bold")).pack(pady=10)
        tk.Label(self, text="Full Name", bg="white", fg="green", font=("arial", 18, "bold")).pack()
        fullname_entry = tk.Entry(self,width=26, font=("Arial", 18))
        fullname_entry.pack()
        
        tk.Label(self, text="Username", bg="white", fg="green", font=("arial", 18, "bold")).pack()
        username_entry = tk.Entry(self,width=26, font=("Arial", 18))
        username_entry.pack()
        
        tk.Label(self, text="Password", bg="white", fg="green", font=("arial", 18, "bold")).pack()
        password_entry = tk.Entry(self, show='*',width=26, font=("Arial", 18))
        password_entry.pack()
        
        tk.Label(self, text="Role",bg="white", fg="green", font=("arial", 18, "bold")).pack()
        role_combobox = ttk.Combobox(self, values=["student", "teacher"],width=26, font=("Arial", 16))
        role_combobox.pack()
        role_combobox.current(0)  # Default to "student"
        
        def signup():
            fullname = fullname_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            role = role_combobox.get().lower()
            if role not in ["student", "teacher"]:
                messagebox.showerror("Sign Up", "Role must be 'student' or 'teacher'.")
                return
            if self.add_user(fullname, username, password, role):
                messagebox.showinfo("Sign Up", f"User {username} created successfully!")
                self.show_login()
            else:
                messagebox.showerror("Sign Up", "Username already exists.")
        
        tk.Button(self, text="Sign Up", command=signup, bg="green", fg="white", font=("arial", 14, "bold")).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_main_menu, bg="green", fg="white",font=("arial", 12, "bold")).pack()

    def show_dashboard(self):
        self.clear_window()
        title_label = tk.Label(self, text="Welcome to Our Exam System", bg="green", fg="white", font=("arial", 20, "bold"))
        title_label.pack(pady=10)
        if self.current_role == "teacher":
            self.show_teacher_dashboard()
        elif self.current_role == "student":
            self.show_student_dashboard()

    def show_teacher_dashboard(self):
        self.clear_window()
        
        tk.Label(self, text=f"Welcome {self.current_user}!").pack(pady=10)
        tk.Button(self, text="Create New Exam", command=self.create_exam, bg="green", fg="white", font=("arial", 16, "bold")).pack(pady=5)
        tk.Button(self, text="Edit Existing Exams", command=self.edit_exams, bg="green", fg="white", font=("arial", 16, "bold")).pack(pady=5)
        tk.Button(self, text="View Student Marks", command=self.view_student_marks, bg="green", fg="white", font=("Arial", 16, "bold")).pack(pady=5)
        tk.Button(self, text="Logout", command=self.logout, bg="green", fg="white").pack(pady=5)

    def create_exam(self):
        self.clear_window()

        tk.Label(self, text="Create New Exam").pack(pady=10)

        tk.Label(self, text="Exam Name").pack()
        exam_name_entry = tk.Entry(self)
        exam_name_entry.pack()

        tk.Label(self, text="Duration (minutes)").pack()
        duration_entry = tk.Entry(self)
        duration_entry.pack()

        tk.Label(self, text="Total Questions").pack()
        total_questions_entry = tk.Entry(self)
        total_questions_entry.pack()

        def save_exam():
            exam_name = exam_name_entry.get()
            duration = int(duration_entry.get())
            total_questions = int(total_questions_entry.get())
            self.add_exam(exam_name, duration, total_questions)
            self.current_exam = exam_name
            self.add_questions(exam_name, total_questions)
        
        tk.Button(self, text="Save Exam", command=save_exam, bg="green", fg="white", font=("arial", 10, "bold")).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_teacher_dashboard, bg="green", fg="white").pack()

    def add_questions(self, exam_name, total_questions):
        self.clear_window()
        self.current_question_index = 0
        self.total_questions = total_questions
        self.questions = []  # Store questions

        tk.Label(self, text=f"Add Questions to Exam: {exam_name}").pack(pady=10)
        self.add_question_widgets(exam_name)

    def add_question_widgets(self, exam_name):
        if self.current_question_index < self.total_questions:
            question_frame = tk.Frame(self, bd=2, relief=tk.GROOVE, padx=10, pady=10)
            question_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
            
            question_label = tk.Label(question_frame, text=f"Question {self.current_question_index + 1}:", font=("Arial", 14, "bold"), fg="blue")
            question_label.pack(anchor=tk.W)
            
            question_text = tk.Text(question_frame, height=4, width=100)
            question_text.pack(pady=10)
            
            option_frame = tk.Frame(question_frame, bd=2, relief=tk.GROOVE)
            option_frame.pack(pady=10, padx=10)
            
            options = []
            for i in range(4):
                option_text = tk.Text(option_frame, height=2, width=80)
                option_text.pack(pady=5)
                options.append(option_text)
            
            correct_answer_label = tk.Label(question_frame, text="Correct Answer (1-4):", font=("Arial", 10), fg="black")
            correct_answer_label.pack(pady=5, anchor=tk.W)
            
            correct_answer_entry = tk.Entry(question_frame, width=10)
            correct_answer_entry.pack(pady=5)
            
            def save_question():
                question = question_text.get("1.0", tk.END).strip()
                options_text = [option.get("1.0", tk.END).strip() for option in options]
                correct_answer = int(correct_answer_entry.get())
                
                if correct_answer < 1 or correct_answer > 4:
                    messagebox.showerror("Error", "Correct answer must be between 1 and 4.")
                    return
                
                # Store the question and options in the list
                self.questions.append({
                    "question": question,
                    "options": options_text,
                    "correct_answer": correct_answer
                })
                
                self.current_question_index += 1
                question_frame.destroy()  # Clear the current question frame
                
                # If there are more questions, add the next question
                if self.current_question_index < self.total_questions:
                    self.add_question_widgets(exam_name)
                else:
                    self.show_teacher_dashboard()  # Show dashboard after all questions are added
            
            save_button = tk.Button(question_frame, text="Save Question", command=save_question, bg="green", fg="white")
            save_button.pack(pady=10)

    
    def edit_exams(self):
        self.clear_window()

        tk.Label(self, text="Edit Existing Exams", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_teacher_dashboard, bg="green", fg="white").pack(pady=10)
           
        # Load existing exams
        data = load_user_data()
        exams = data.get("exams", {}) 
        print("Loaded exams:", exams)
        if not exams:
           tk.Label(self, text="No exams found.", font=("Arial", 12)).pack(pady=10)
           tk.Button(self, text="Back", command=self.show_teacher_dashboard, bg="green", fg="white").pack(pady=10)
           return

        exam_listbox = tk.Listbox(self)
        for exam_name in exams.keys():
            print("Adding exam to Listbox:", exam_name) 
            exam_listbox.insert(tk.END, exam_name)
        exam_listbox.pack(pady=30)

        def load_exam_for_editing():
            selected_exam = exam_listbox.get(tk.ACTIVE)
            print("Selected Exam:", selected_exam)  # Debug: Print selected exam
            if selected_exam:
               self.edit_exam_details(selected_exam)

        tk.Button(self, text="Edit Selected Exam", command=load_exam_for_editing, bg="green", fg="white").pack(pady=10)
        tk.Button(self, text="Back", command=self.show_teacher_dashboard, bg="green", fg="white").pack(pady=10)
    def load_exams(self):
    # Example implementation to load from JSON
        user_data = load_user_data()
        return user_data.get("exams", {})
    def edit_exam_details(self, exam_name):
        self.clear_window()

        data = load_user_data()
        exam = data["exams"].get(exam_name, {})

        tk.Label(self, text=f"Editing Exam: {exam_name}", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self, text="Exam Name").pack()
        exam_name_entry = tk.Entry(self)
        exam_name_entry.insert(0, exam_name)
        exam_name_entry.pack(pady=10)

        tk.Label(self, text="Duration (minutes)").pack()
        duration_entry = tk.Entry(self)
        duration_entry.insert(0, str(exam.get("duration", 0)))
        duration_entry.pack(pady=10)

        def save_exam_changes():
           new_exam_name = exam_name_entry.get()
           duration = int(duration_entry.get())
        
        # Update exam details in data
           if new_exam_name != exam_name:
              data["exams"][new_exam_name] = data["exams"].pop(exam_name)
           data["exams"][new_exam_name]["duration"] = duration
        
           save_user_data(data)
           messagebox.showinfo("Success", "Exam updated successfully!")
           self.show_teacher_dashboard()

        tk.Button(self, text="Save Changes", command=save_exam_changes, bg="green", fg="white").pack(pady=10)
        tk.Button(self, text="Edit Questions", command=lambda: self.edit_exam_questions(exam_name), bg="green", fg="white").pack(pady=10)
        tk.Button(self, text="Back", command=self.edit_exams, bg="green", fg="white").pack(pady=10)

    def edit_exam_questions(self, exam_name):
        self.clear_window()
        data = load_user_data()
        exam = data.get("exams", {}).get(exam_name, {})
        questions = exam.get("questions", [])
        questions = exam.get("questions", [])
         

        if not questions:
           tk.Label(self, text="No questions found for this exam.", font=("Arial", 12)).pack(pady=10)
           tk.Button(self, text="Back", command=lambda: self.edit_exam_details(exam_name), bg="green", fg="white").pack(pady=10)
           return

        tk.Label(self, text=f"Editing Questions for Exam: {exam_name}", font=("Arial", 14, "bold")).pack(pady=10)

        self.current_question_index = 0
        self.questions = questions
        self.edit_question_widgets(exam_name)

    def edit_question_widgets(self, exam_name):
        if self.current_question_index < len(self.questions):
           question_frame = tk.Frame(self, bd=2, relief=tk.GROOVE, padx=10, pady=10)
           question_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

           question_data = self.questions[self.current_question_index]

           question_label = tk.Label(question_frame, text=f"Question {self.current_question_index + 1}:", font=("Arial", 14, "bold"), fg="blue")
           question_label.pack(anchor=tk.W)

           question_text = tk.Text(question_frame, height=4, width=100)
           question_text.insert(tk.END, question_data["question"])
           question_text.pack(pady=10)

           option_frame = tk.Frame(question_frame, bd=2, relief=tk.GROOVE)
           option_frame.pack(pady=10, padx=10)

           options = []
           for i in range(4):
               option_text = tk.Text(option_frame, height=2, width=80)
               option_text.insert(tk.END, question_data["options"][i])
               option_text.pack(pady=5)
               options.append(option_text)

           correct_answer_label = tk.Label(question_frame, text="Correct Answer (1-4):", font=("Arial", 12), fg="black")
           correct_answer_label.pack(pady=5, anchor=tk.W)

           correct_answer_entry = tk.Entry(question_frame, width=5)
           correct_answer_entry.insert(0, str(question_data["correct_answer"]))
           correct_answer_entry.pack(pady=5)

           def save_question_changes():
               question = question_text.get("1.0", tk.END).strip()
               options_text = [option.get("1.0", tk.END).strip() for option in options]
               correct_answer = int(correct_answer_entry.get())

               if correct_answer < 1 or correct_answer > 4:
                  messagebox.showerror("Error", "Correct answer must be between 1 and 4.")
                  return

            # Update question data
               self.questions[self.current_question_index] = {
                   "question": question,
                   "options": options_text,
                   "correct_answer": correct_answer
               }
               messagebox.showinfo("Saved", f"Question {self.current_question_index + 1} saved successfully.")

               question_frame.destroy() 
               self.current_question_index += 1
               question_frame.destroy()  # Clear the current question frame

            # If there are more questions, edit the next question
               if self.current_question_index < len(self.questions):
                  self.edit_question_widgets(exam_name)
               else:
                # Save updated questions to the exam data
                  data = load_user_data()
                  data["exams"][exam_name]["questions"] = self.questions
                  save_user_data(data)
                  messagebox.showinfo("Success", "All questions updated successfully!")
                  self.show_teacher_dashboard()

        save_button = tk.Button(question_frame, text="Save Question", command=save_question_changes, bg="green", fg="white")
        save_button.pack(pady=10)
        
 # To be implemented for editing existing exams

    def add_exam(self, exam_name, duration, total_questions):
        data = load_user_data()
    
        if "exams" not in data:
           data["exams"] = {}
    
        data["exams"][exam_name] = {
            "duration": duration,
            "total_questions": total_questions,
            "questions": self.questions  # Store the questions created by the teacher
        }
    
        save_user_data(data)
        messagebox.showinfo("Success", "Exam created successfully!")
        self.show_teacher_dashboard()
  # To be implemented for adding new exams
    def view_student_marks(self):
        self.clear_window()

        data = load_user_data()
    
    # Retrieve exams data
        exams = data.get("exams", {})
        if not exams:
           tk.Label(self, text="No exams found.", font=("Arial", 12)).pack(pady=10)
           tk.Button(self, text="Back", command=self.show_teacher_dashboard, bg="green", fg="white").pack(pady=10)
           return
    
        tk.Label(self, text="View Student Marks", font=("Arial", 16, "bold")).pack(pady=10)
    
    # Create a listbox to select an exam
        exam_listbox = tk.Listbox(self)
        for exam_name in exams.keys():
            exam_listbox.insert(tk.END, exam_name)
        exam_listbox.pack(pady=20)
    
        def load_marks_for_selected_exam():
            selected_exam = exam_listbox.get(tk.ACTIVE)
            if selected_exam:
               self.show_marks_for_exam(selected_exam)
    
        tk.Button(self, text="Show Marks", command=load_marks_for_selected_exam, bg="green", fg="white").pack(pady=10)
        tk.Button(self, text="Back", command=self.show_teacher_dashboard, bg="green", fg="white").pack(pady=10)
    def show_marks_for_exam(self, exam_name):
        self.clear_window()

        data = load_user_data()
    
    # Retrieve student results data
        students = data.get("students", {})
        exam_results = []

        for student, details in students.items():
            results = details.get("results", [])
            for result in results:
                if result["exam_name"] == exam_name:
                   exam_results.append((student, result["score"], result["total_questions"]))

        if not exam_results:
           tk.Label(self, text="No results found for this exam.", font=("Arial", 12)).pack(pady=10)
           tk.Button(self, text="Back", command=self.view_student_marks, bg="green", fg="white").pack(pady=10)
           return
    
        tk.Label(self, text=f"Marks for {exam_name}", font=("Arial", 16, "bold")).pack(pady=12)

    # Create a table to display results
        results_frame = tk.Frame(self)
        results_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Table headers
        tk.Label(results_frame, text="Student Name", font=("Arial", 14, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(results_frame, text="Score", font=("Arial", 14, "bold"), borderwidth=1, relief="solid", width=10).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(results_frame, text="Total Questions", font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=15).grid(row=0, column=2, padx=5, pady=5)

    # Populate the table with results
        for index, (student, score, total_questions) in enumerate(exam_results):
            tk.Label(results_frame, text=student, font=("Arial", 14), borderwidth=1, relief="solid", width=20).grid(row=index + 1, column=0, padx=5, pady=5)
            tk.Label(results_frame, text=f"{score}/{total_questions}", font=("Arial", 12), borderwidth=1, relief="solid", width=10).grid(row=index + 1, column=1, padx=5, pady=5)
            tk.Label(results_frame, text=total_questions, font=("Arial", 12), borderwidth=1, relief="solid", width=15).grid(row=index + 1, column=2, padx=5, pady=5)

        tk.Button(self, text="Back", command=self.view_student_marks, bg="green", fg="white").pack(pady=10)

    def show_student_dashboard(self):
        self.clear_window()
        tk.Label(self, text=f"Welcome {self.current_user}!", bg="green", fg="white", font=("arial", 16, "bold")).pack(pady=10)
        
        tk.Button(self, text="Start Exam", command=self.start_exam, bg="green", fg="white", font=("arial", 18, "bold")).pack(pady=10)
        tk.Button(self, text="View Results", command=self.view_results, bg="green", fg="white", font=("arial", 18, "bold")).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout, bg="green", fg="white").pack(pady=12)

    def start_exam(self):
        self.clear_window()

        tk.Label(self, text=f"Welcome {self.current_user}!", bg="green", fg="white", font=("arial", 18, "bold")).pack(pady=12)
        tk.Label(self, text=f"Exam: {self.current_exam}", bg="green", fg="white", font=("arial", 20, "bold")).pack(pady=10)

        self.current_question_index = 0
        self.total_marks = 0
        self.show_next_question()

    def show_next_question(self):
        if self.current_question_index < len(self.questions):
            question_frame = tk.Frame(self, bd=2, relief=tk.GROOVE, padx=10, pady=10)
            question_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
            
            question_label = tk.Label(question_frame, text=f"Question {self.current_question_index + 1}:", font=("Arial", 14, "bold"), fg="blue")
            question_label.pack(anchor=tk.W)
            
            question_text = tk.Label(question_frame, text=self.questions[self.current_question_index]['question'], font=("Arial", 14), wraplength=1200, justify=tk.LEFT)
            question_text.pack(pady=10, anchor=tk.W)
            
            option_frame = tk.Frame(question_frame, bd=2, relief=tk.GROOVE, width=1000)
            option_frame.pack(pady=10, padx=10)
            
            options = []
            for i in range(4):
                option_label = tk.Label(option_frame, text=self.questions[self.current_question_index]['options'][i], font=("Arial", 14), wraplength=1400, justify=tk.LEFT)
                option_label.pack(anchor=tk.W)
                options.append(option_label)
            
            answer_label = tk.Label(question_frame, text="Your Answer:", font=("Arial", 12), fg="black")
            answer_label.pack(pady=5, anchor=tk.W)
            
            answer_entry = tk.Entry(question_frame, width=10)
            answer_entry.pack(pady=5)
            
            def submit_answer():
                correct_answer = self.questions[self.current_question_index]['correct_answer']
                selected_answer = int(answer_entry.get())
                
                if selected_answer == correct_answer:
                    messagebox.showinfo("Result", "Correct answer!")
                    self.total_marks += 1
                    options[selected_answer - 1]['fg'] = 'green'  # Highlight correct answer in green
                else:
                    messagebox.showinfo("Result", f"Wrong answer! Correct answer: Option {correct_answer}")
                    options[selected_answer - 1]['fg'] = 'red'    # Highlight wrong answer in red
                    options[correct_answer - 1]['fg'] = 'green'   # Highlight correct answer in green
                
                self.current_question_index += 1
                question_frame.destroy()  # Clear the current question frame
                
                # If there are more questions, show the next question
                if self.current_question_index < len(self.questions):
                    self.show_next_question()
                else:
                    self.finish_exam()  # Finish exam after all questions are answered
            
            submit_button = tk.Button(question_frame, text="Submit Answer", command=submit_answer, bg="green", fg="white")
            submit_button.pack(pady=10)

    def finish_exam(self):
        messagebox.showinfo("Exam Finished", f"Exam finished! Total marks: {self.total_marks}/{len(self.questions)}")
        self.show_student_dashboard()  # Show student dashboard after finishing exam

    def view_results(self):
        
        self.clear_window()

    # Load user data
        data = load_user_data()

    # Get the current student's username
        current_username = self.current_user

    # Retrieve student data
        student_data = data.get("students", {}).get(current_username, {})
        results = student_data.get("results", [])

        if not results:
           tk.Label(self, text="No results found.", font=("Arial", 12)).pack(pady=10)
           tk.Button(self, text="Back", command=self.show_student_dashboard, bg="green", fg="white").pack(pady=10)
           return

        tk.Label(self, text=f"Results for {current_username}", font=("Arial", 14, "bold")).pack(pady=10)

    # Create a table to display results
        results_frame = tk.Frame(self)
        results_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Table headers
        tk.Label(results_frame, text="Exam Name", font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(results_frame, text="Score", font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=10).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(results_frame, text="Total Questions", font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=15).grid(row=0, column=2, padx=5, pady=5)

    # Populate the table with results
        for index, result in enumerate(results):
           tk.Label(results_frame, text=result["exam_name"], font=("Arial", 12), borderwidth=1, relief="solid", width=20).grid(row=index + 1, column=0, padx=5, pady=5)
           tk.Label(results_frame, text=f"{result['score']}/{result['total_questions']}", font=("Arial", 12), borderwidth=1, relief="solid", width=10).grid(row=index + 1, column=1, padx=5, pady=5)
           tk.Label(results_frame, text=result["total_questions"], font=("Arial", 12), borderwidth=1, relief="solid", width=15).grid(row=index + 1, column=2, padx=5, pady=5)

        tk.Button(self, text="Back", command=self.show_student_dashboard, bg="green", fg="white").pack(pady=10)
 # To be implemented for viewing student results

    def logout(self):
        self.current_user = None
        self.current_role = None
        self.show_main_menu()

    def verify_login(self, username, password, role):
        user_data = load_user_data()

        if username in user_data[role + "s"] and user_data[role + "s"][username]["password"] == password:
            return True
        return False# Dummy implementation, replace with actual authentication logic
        return True

    def add_user(self, fullname, username, password, role):
        data = load_user_data()
        users = data.get(role + "s", {})
        if username in users:
            return False
        users[username] = {"fullname": fullname, "password": password}
        data[role + "s"] = users
        save_user_data(data)
        return True# Dummy implementation, replace with actual user creation logic
        

if __name__ == "__main__":
    app = ExamSystemApp()
    app.mainloop()
