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
        # "Text Placeholder Lorem Ipsum blabla\n\n"
        # "Enter your hint-based query below:"
    )
    instructions = tk.Label(help_window, text=help_text, font=("Helvetica", 10), wraplength=450, justify="left")
    instructions.pack(pady=10, padx=10)

    # Entry box for the query
    hint_query_entry = tk.Text(help_window, width=60, height=5, font=("Verdana", 10))
    hint_query_entry.insert("1.0", "EXPLAIN /*+ NestLoop(orders customer) */ SELECT * FROM orders INNER JOIN customer ON orders.o_custkey = customer.c_custkey;")
    hint_query_entry.pack(pady=10, padx=10)

    # Function to apply the hint query to the main SQL entry box
    def apply_example():
        sql_entry.delete(0, tk.END)
        sql_entry.insert(0, hint_query_entry.get("1.0", "end-1c"))  # Insert the query without the newline at the end
        help_window.destroy()

    # Button to apply the hint query
    apply_button = tk.Button(help_window, text="Apply Example to SQL Query", command=apply_example, font=("Segoe UI", 10, "bold"), bg="#4a90e2", fg="#ffffff")
    apply_button.pack(pady=10)

# Configure the grid layout for the main window
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)

# Top Frame for SQL and AQP Sections
top_frame = tk.Frame(window)
top_frame.grid(row=0, column=0, columnspan=2, pady=20)

# Load Help Icon
try:
    help_icon = Image.open("help_icon.png").resize((20, 20), Image.LANCZOS)
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

sql_image_canvas = tk.Canvas(sql_output_frame, bg="#ffffff")  # Create a canvas for the SQL image
sql_image_canvas.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

sql_scrollbar = tk.Scrollbar(sql_output_frame, orient="vertical", command=sql_image_canvas.yview)  # Vertical scrollbar
sql_scrollbar.pack(side="right", fill="y")

sql_image_canvas.configure(yscrollcommand=sql_scrollbar.set)

#SQL steps output area
sql_steps_output = tk.Label(sql_output_frame, text="Query steps will appear here.", font=("Verdana", 10), wraplength=300)
sql_steps_output.pack(side="right", fill="both", expand=True, padx=5)



# AQP Output Section
aqp_output_frame = tk.LabelFrame(bottom_frame, text="AQP Query Output", font=("Verdana", 12, "bold"))
aqp_output_frame.grid(row=0, column=1, padx=25, sticky="nsew")
aqp_output_frame.grid_rowconfigure(0, weight=1)

aqp_image_canvas = tk.Canvas(aqp_output_frame, bg="#ffffff")  # Create a canvas for the AQP image
aqp_image_canvas.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

aqp_scrollbar = tk.Scrollbar(aqp_output_frame, orient="vertical", command=aqp_image_canvas.yview)  # Vertical scrollbar
aqp_scrollbar.pack(side="right", fill="y")

aqp_image_canvas.configure(yscrollcommand=aqp_scrollbar.set)

# AQP steps output area
aqp_steps_output = tk.Label(aqp_output_frame, text="AQP steps will appear here.", font=("Verdana", 10), wraplength=300)
aqp_steps_output.pack(side="right", fill="both", expand=True, padx=5)


# Function to execute queries and update outputs
def execute_query(query_type):
    query = sql_entry.get() if query_type == "sql" else aqp_entry.get()
    display_canvas = sql_image_canvas if query_type == "sql" else aqp_image_canvas  # Use the scrollable canvas
    steps_output = sql_steps_output if query_type == "sql" else aqp_steps_output
    cost_label = qep_cost_label if query_type == "sql" else aqp_cost_label

    def execute_query_thread():
        try:
            connect_db()
            if query_type == "sql":
                qep_digraph, query_cost = get_qep(query)
                print(qep_digraph)
                display_image(qep_digraph, display_canvas)  # Update to use the canvas
                statements, _ = get_qep_statements()
                steps_output.config(text='\n'.join(statements))
                cost_label.config(text=f"QEP Cost: {query_cost}")
            elif query_type == "aqp":
                aqp_digraph, aqp_query_cost = get_aqp(query)
                print(aqp_digraph)
                display_image(aqp_digraph, display_canvas)  # Update to use the canvas
                statements, _ = get_qep_statements()
                steps_output.config(text='\n'.join(statements))
                cost_label.config(text=f"AQP Cost: {aqp_query_cost}")
            disconnect_db()
        except Exception as e:
            steps_output.config(text=f"Error: {str(e)}")

    query_thread = Thread(target=execute_query_thread)
    query_thread.start()

# Function to display the image and fit it to the canvas width
def display_image(image_path, canvas):
    try:
        # Open the image
        image = Image.open(image_path).convert("RGB")

        # Get the current canvas width and height
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Ensure the canvas has been rendered and dimensions are available
        if canvas_width == 1 or canvas_height == 1:  # Default dimensions before rendering
            canvas.update_idletasks()  # Force the canvas to update
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

        # Maintain aspect ratio while resizing
        img_aspect_ratio = image.width / image.height
        canvas_aspect_ratio = canvas_width / canvas_height

        if img_aspect_ratio > canvas_aspect_ratio:
            # Fit by width
            new_width = canvas_width
            new_height = int(canvas_width / img_aspect_ratio)
        else:
            # Fit by height
            new_height = canvas_height
            new_width = int(canvas_height * img_aspect_ratio)

        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)

        # Clear any previous content on the canvas
        canvas.delete("all")

        # Display the image at the center of the canvas
        canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=tk_image)

        # Update the scroll region to match the image dimensions
        canvas.config(scrollregion=canvas.bbox("all"))

        # Store the image reference to prevent garbage collection
        canvas.image = tk_image
    except Exception as e:
        print(f"Error displaying image: {e}")





# Cost Comparison at the bottom
cost_panel = tk.Frame(window, height=40, bg="#f0f0f0")
cost_panel.grid(row=2, column=0, columnspan=2, sticky="nsew")

qep_cost_label = tk.Label(cost_panel, text=f"QEP Cost: {query_cost}", font=("Segoe UI", 10, "bold"), fg="#ff4d4d" if aqp_query_cost < query_cost else "#27ae60", bg="#f0f0f0")
qep_cost_label.pack(side="left", padx=10)

aqp_cost_label = tk.Label(cost_panel, text=f"AQP Cost: {aqp_query_cost}", font=("Segoe UI", 10, "bold"), fg="#27ae60" if aqp_query_cost < query_cost else "#ff4d4d", bg="#f0f0f0")
aqp_cost_label.pack(side="left", padx=10)

# Start the mainloop
window.mainloop()
