import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from threading import Thread
from preprocessing import connect_db, get_qep, get_aqp, disconnect_db, get_qep_statements
import tkinter.font as tkFont

# Global variables
query_cost = 0
aqp_query_cost = 0
operator_selections = {}

def update_operator_selection(step, selected_operator):
    operator_selections[step] = selected_operator

# Main Window Configuration
window = tk.Tk()
window.title("SQL Query Executor")
# # Set the window size to cover the entire screen
window.geometry(f"{int(4.9/5*window.winfo_screenwidth())}x{window.winfo_screenheight()}")

# window.attributes("-fullscreen", True)

# # Function to exit full screen
# def exit_fullscreen(event=None):
#     window.attributes("-fullscreen", False)

# # Bind the Escape key to exit full screen
# window.bind("<Escape>", exit_fullscreen)

# Define fonts
bold_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

# Function to display help popup with pg_hint_plan information and an entry box
def show_help():
    help_window = tk.Toplevel(window)
    help_window.title("pg_hint_plan Help")
    help_window.geometry("400x300")

    # Instructions
    help_text = (
        "Type the desired scan/join methods in the box provided. There is no need to retype the original query again. Separate each method with a space.\n\n"
         "Scan Methods:\n\n"
         "1. SeqScan(table) - Sequential scan will be performed on the table\n"
         "2. TidScan(table) - Tid scan will be performed on the table\n"
         "3. IndexScan(table) - Index scan will be performed on the table\n"
         "4. IndexOnlyScan(table) - Index-only scan will be performed on the table\n"
         "5. BitmapScan(table) - Bitmap scan will be performed on the table\n\n"
         
         "6. NoSeqScan(table) - Sequential scan will NOT be performed on the table\n"
         "7. NoTidScan(table) - Tid scan will NOT be performed on the table\n"
         "8. NoIndexScan(table) - Index scan will NOT be performed on the table\n"
         "9. NoIndexOnlyScan(table) - Index-only scan will NOT be performed on the table\n"
         "10. NoBitMapScan(table) - Bitmap scan will NOT be performed on the table\n\n"
         
         "Join Methods:\n\n"
         "1. NestLoop(table1 table2) - Nested Loop Join will be performed on these tables\n"
         "2. HashJoin(table1 table2) - Hash Join will be performed on these tables\n"
         "3. MergeJoin(table1 table2) - Merge Join will be performed on these tables\n\n"
         
         "4. NoNestLoop(table1, table2) - Nested Loop Join will NOT be performed on these tables\n"
         "5. NoHashJoin(table1, table2) - Hash Join will NOT be performed on these tables\n"
         "6. NoMergeJoin(table1, table2) - Merge Join will NOT be performed on these tables\n\n"
         
         "Join Order:\n\n"
         "1. Leading(table1, table2) - These two tables will be joined together\n\n"
         
         "Join Direction:\n\n"
         "1. Leading((table1, table2)) - These two tables will be joined together, where table1 is the outer table and table2 is the inner table"
    )
    instructions = tk.Label(help_window, text=help_text, font=("Helvetica", 10), wraplength=450, justify="left")
    instructions.pack(pady=10, padx=10)

# Configure the grid layout for the main window
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)

# Top Frame for SQL and AQP Sections
top_frame = tk.Frame(window)
top_frame.grid(row=0, column=0, columnspan=2, pady=20)

# Load Help Icon
try:
    help_icon = Image.open("project2\help_icon.png").resize((20, 20), Image.LANCZOS)
    help_icon = ImageTk.PhotoImage(help_icon)
except Exception as e:
    print("Help icon not found:", e)
    help_icon = None  # Use no icon if not found

# SQL Query Section
sql_frame = tk.Frame(top_frame)
sql_frame.grid(row=0, column=0, padx=20)

sql_label = tk.Label(sql_frame, text="Enter SQL Query", font=("Verdana", 14, "bold"))
#sql_label.pack(pady=5)
# Center the label vertically and horizontally 
sql_label.pack(expand=True, fill='both')

sql_entry = tk.Entry(sql_frame, width=60, font=("Verdana", 12), bg="#e8f4fa", fg="#333333")
sql_entry.pack(pady=(5, 10))

execute_sql_button = tk.Button(sql_frame, text="Execute SQL Query", command=lambda: execute_query("sql"), font=("Segoe UI", 10, "bold"), bg="#4a90e2", fg="#ffffff")
execute_sql_button.pack(pady=10)

nil_button = tk.Button(sql_frame, borderwidth=0)
nil_button.pack(padx=2)

# AQP Query Section
aqp_frame = tk.Frame(top_frame)
aqp_frame.grid(row=0, column=1, padx=20)

aqp_label = tk.Label(aqp_frame, text="Enter AQP Query", font=("Verdana", 14, "bold"))
#aqp_label.pack(pady=5)
# Center the label vertically and horizontally 
aqp_label.pack(expand=True, fill='both')

aqp_entry = tk.Entry(aqp_frame, width=60, font=("Verdana", 12), bg="#e8f4fa", fg="#333333")
aqp_entry.pack(pady=(5, 10))

execute_aqp_button = tk.Button(aqp_frame, text="Execute AQP Query", command=lambda: execute_query("aqp"), font=("Segoe UI", 10, "bold"), bg="#4a90e2", fg="#ffffff")
execute_aqp_button.pack(pady=10)

help_aqp_button = tk.Button(aqp_frame, image=help_icon, command=show_help, borderwidth=0)
help_aqp_button.pack(padx=2)

# Bottom Frame for Outputs
bottom_frame = tk.Frame(window)
bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ns")

# Configure the grid layout for the bottom frame
bottom_frame.columnconfigure(0, weight=5)
bottom_frame.columnconfigure(1, weight=5)
bottom_frame.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand vertically


# SQL Output Section
sql_output_frame = tk.LabelFrame(bottom_frame, text="SQL Query Output", font=("Verdana", 12, "bold"))
sql_output_frame.grid(row=0, column=0, padx=25, sticky="nsew")
sql_output_frame.grid_rowconfigure(0, weight=1) 


qep_display = tk.Label(sql_output_frame, font=("Verdana", 12), bg="#ffffff", width=40, height=20)
qep_display.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

sql_steps_output = tk.Label(sql_output_frame, text="Query steps will appear here.", font=("Verdana", 10), wraplength=300)
sql_steps_output.pack(side="right", fill="both", expand=True, padx=5)

# AQP Output Section
aqp_output_frame = tk.LabelFrame(bottom_frame, text="AQP Query Output", font=("Verdana", 12, "bold"))
aqp_output_frame.grid(row=0, column=1, padx=25, sticky="nsew")
aqp_output_frame.grid_rowconfigure(0, weight=1)


aqp_display = tk.Label(aqp_output_frame, font=("Verdana", 12), bg="#ffffff", width=40, height=20)
aqp_display.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

aqp_steps_output = tk.Label(aqp_output_frame, text="AQP steps will appear here.", font=("Verdana", 10), wraplength=300)
aqp_steps_output.pack(side="right", fill="both", expand=True, padx=5)

# Function to execute queries and update outputs
def execute_query(query_type):
    query = sql_entry.get() if query_type == "sql" else aqp_entry.get()
    display_label = qep_display if query_type == "sql" else aqp_display
    steps_output = sql_steps_output if query_type == "sql" else aqp_steps_output
    cost_label = qep_cost_label if query_type == "sql" else aqp_cost_label

    def execute_query_thread():
        try:
            connect_db()
            if query_type == "sql":
                qep_digraph, query_cost = get_qep(query)
                print(qep_digraph)
                display_image(qep_digraph, display_label)
                statements, _ = get_qep_statements()
                steps_output.config(text='\n'.join(statements))
                cost_label.config(text=f"QEP Cost: {query_cost}")
            elif query_type == "aqp":
                aqp_digraph, aqp_query_cost = get_aqp(query)
                print(aqp_digraph)
                display_image(aqp_digraph, display_label)
                statements, _ = get_qep_statements()
                steps_output.config(text='\n'.join(statements))
                cost_label.config(text=f"AQP Cost: {aqp_query_cost}")
            disconnect_db()
        except Exception as e:
            steps_output.config(text=f"Error: {str(e)}")

    query_thread = Thread(target=execute_query_thread)
    query_thread.start()

# Function to display the image
def display_image(image_path, display_label):
    try:
        image = Image.open(image_path).convert("RGB")
        resized_image = image.resize((300, 300), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        display_label.config(image=tk_image)
        display_label.image = tk_image
    except Exception as e:
        print(e)

# Cost Comparison at the bottom
cost_panel = tk.Frame(window, height=40, bg="#f0f0f0")
cost_panel.grid(row=2, column=0, columnspan=2, sticky="nsew")

qep_cost_label = tk.Label(cost_panel, text=f"QEP Cost: {query_cost}", font=("Segoe UI", 10, "bold"), fg="#ff4d4d" if aqp_query_cost < query_cost else "#27ae60", bg="#f0f0f0")
qep_cost_label.pack(side="left", padx=10)

aqp_cost_label = tk.Label(cost_panel, text=f"AQP Cost: {aqp_query_cost}", font=("Segoe UI", 10, "bold"), fg="#27ae60" if aqp_query_cost < query_cost else "#ff4d4d", bg="#f0f0f0")
aqp_cost_label.pack(side="left", padx=10)

# Start the mainloop
window.mainloop()
