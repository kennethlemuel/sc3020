import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from threading import Thread
from preprocessing import connect_db, get_qep, disconnect_db, get_qep_statements
from whatif import get_aqp
import tkinter.font as tkFont

# Global variables
query = ""
aqp_query = ""
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

# Set the window size to match the screen resolution
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Maximize the window
window.state('zoomed')  # For Windows, ensures the window is maximized in a windowed fullscreen mode.


# Define fonts
bold_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

# Function to display help popup with pg_hint_plan information and an entry box
# Function to display help popup with pg_hint_plan information and an entry box
def show_help():
    help_window = tk.Toplevel(window)
    help_window.title("pg_hint_plan Help")


    window_width = 800
    window_height = 700
    x_position = 100  # Distance from the left edge of the screen
    y_position = 50   # Distance from the top edge of the screen
    help_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Add a scrollbar to the help window
    help_canvas = tk.Canvas(help_window)
    help_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(help_window, orient="vertical", command=help_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    help_canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas for the content
    content_frame = tk.Frame(help_canvas, bg="#f0f0f0")
    help_canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Add headers and content as separate Labels
    sections = [
        (None,  # No header for the introduction
         "Type the desired scan/join methods in the box provided. There is no need to retype the original query again. Separate each method with a space.\n\n"),
        ("Scan Methods:", "1. SeqScan(table) - Sequential scan will be performed on the table\n"
                          "2. TidScan(table) - Tid scan will be performed on the table\n"
                          "3. IndexScan(table) - Index scan will be performed on the table\n"
                          "4. IndexOnlyScan(table) - Index-only scan will be performed on the table\n"
                          "5. BitmapScan(table) - Bitmap scan will be performed on the table\n\n"
                          "6. NoSeqScan(table) - Sequential scan will NOT be performed on the table\n"
                          "7. NoTidScan(table) - Tid scan will NOT be performed on the table\n"
                          "8. NoIndexScan(table) - Index scan will NOT be performed on the table\n"
                          "9. NoIndexOnlyScan(table) - Index-only scan will NOT be performed on the table\n"
                          "10. NoBitMapScan(table) - Bitmap scan will NOT be performed on the table\n"),
        ("Join Methods:", "1. NestLoop(table1 table2) - Nested Loop Join will be performed on these tables\n"
                          "2. HashJoin(table1 table2) - Hash Join will be performed on these tables\n"
                          "3. MergeJoin(table1 table2) - Merge Join will be performed on these tables\n\n"
                          "4. NoNestLoop(table1, table2) - Nested Loop Join will NOT be performed on these tables\n"
                          "5. NoHashJoin(table1, table2) - Hash Join will NOT be performed on these tables\n"
                          "6. NoMergeJoin(table1, table2) - Merge Join will NOT be performed on these tables\n"),
        ("Join Order:", "1. Leading(table1, table2) - These two tables will be joined together\n\n"),
        ("Join Direction:", "1. Leading((table1, table2)) - These two tables will be joined together, where table1 is the outer table and table2 is the inner table"),
    ]

    # Iterate through the sections and add them to the content frame
    for header, content in sections:
        if header:  # If there's a header, make it bold
            header_label = tk.Label(content_frame, text=header, font=("Helvetica", 12, "bold"), bg="#f0f0f0")
            header_label.pack(anchor="w", pady=(10, 5), padx=10)

        if content:  # Add the content below the header
            content_label = tk.Label(content_frame, text=content, font=("Helvetica", 10), bg="#f0f0f0", justify="left", wraplength=750)
            content_label.pack(anchor="w", pady=(0, 5), padx=10)

    # Update scrollable region
    def update_scrollregion(event):
        help_canvas.configure(scrollregion=help_canvas.bbox("all"))

    content_frame.bind("<Configure>", update_scrollregion)


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

# Cost Comparison at the top
cost_panel = tk.Frame(top_frame, height=40, bg="#f0f0f0")
cost_panel.grid(row=1, column=0, columnspan=2, sticky="nsew")

qep_cost_label = tk.Label(cost_panel, text=f"QEP Cost: {query_cost}", font=("Segoe UI", 10, "bold"), fg="#ff4d4d" if aqp_query_cost < query_cost else "#27ae60", bg="#f0f0f0")
qep_cost_label.pack(side="left", padx=10)

aqp_cost_label = tk.Label(cost_panel, text=f"AQP Cost: {aqp_query_cost}", font=("Segoe UI", 10, "bold"), fg="#27ae60" if aqp_query_cost < query_cost else "#ff4d4d", bg="#f0f0f0")
aqp_cost_label.pack(side="right", padx=10)

# Bottom Frame for Outputs
bottom_frame = tk.Frame(window)
bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ns")

# Configure the grid layout for the bottom frame
bottom_frame.columnconfigure(0, weight=5)
bottom_frame.columnconfigure(1, weight=5)
bottom_frame.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand vertically


# SQL Output Section
sql_output_frame = tk.LabelFrame(bottom_frame, text="SQL Query Output", font=("Verdana", 12, "bold"))
sql_output_frame.grid(row=0, column=0, padx=25, pady= 25, sticky="nsew")
sql_output_frame.grid_rowconfigure(0, weight=1)

sql_image_canvas = tk.Canvas(sql_output_frame, bg="#ffffff")  # Canvas for SQL image
sql_image_canvas.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

# Add a frame for steps with scrollbar
sql_steps_frame = tk.Frame(sql_output_frame)
sql_steps_frame.pack(side="right", fill=tk.BOTH, expand=True, padx=5)

sql_steps_scrollbar = tk.Scrollbar(sql_steps_frame, orient="vertical")  # Scrollbar for query steps
sql_steps_scrollbar.pack(side="right", fill="y")

sql_steps_output = tk.Text(sql_steps_frame, wrap="word", font=("Verdana", 10), yscrollcommand=sql_steps_scrollbar.set)
sql_steps_output.pack(side="left", fill="both", expand=True)

sql_steps_scrollbar.config(command=sql_steps_output.yview)

# AQP Output Section
aqp_output_frame = tk.LabelFrame(bottom_frame, text="AQP Query Output", font=("Verdana", 12, "bold"))
aqp_output_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
aqp_output_frame.grid_rowconfigure(0, weight=1)

aqp_image_canvas = tk.Canvas(aqp_output_frame, bg="#ffffff")  # Canvas for AQP image
aqp_image_canvas.pack(side="left", fill=tk.BOTH, expand=True, padx=5)

# Add a frame for steps with scrollbar
aqp_steps_frame = tk.Frame(aqp_output_frame)
aqp_steps_frame.pack(side="right", fill=tk.BOTH, expand=True, padx=5)

aqp_steps_scrollbar = tk.Scrollbar(aqp_steps_frame, orient="vertical")  # Scrollbar for query steps
aqp_steps_scrollbar.pack(side="right", fill="y")

aqp_steps_output = tk.Text(aqp_steps_frame, wrap="word", font=("Verdana", 10), yscrollcommand=aqp_steps_scrollbar.set)
aqp_steps_output.pack(side="left", fill="both", expand=True)

aqp_steps_scrollbar.config(command=aqp_steps_output.yview)

# Function to execute queries and update outputs
def execute_query(query_type):
    global query, aqp_query
    if query_type == "sql":
        query = sql_entry.get()
    else:
        aqp_query = aqp_entry.get()
    
    display_canvas = sql_image_canvas if query_type == "sql" else aqp_image_canvas  # Use the scrollable canvas
    steps_output = sql_steps_output if query_type == "sql" else aqp_steps_output
    cost_label = qep_cost_label if query_type == "sql" else aqp_cost_label

    # Clear the text box and display "Query in progress..."
    steps_output.delete("1.0", tk.END)
    steps_output.insert(tk.END, "Query in progress...\n")

    def execute_query_thread():
        try:
            connect_db()
            if query_type == "sql":
                qep_digraph, query_cost = get_qep(query)
                display_image(qep_digraph, display_canvas)  # Update to use the canvas
                statements, _ = get_qep_statements()
                steps_output.delete("1.0", tk.END)  # Clear the text box
                steps_output.insert(tk.END, '\n'.join(statements))  # Add actual query steps
                cost_label.config(text=f"QEP Cost: {query_cost}")
            elif query_type == "aqp":
                aqp_digraph, aqp_query_cost = get_aqp(query, aqp_query)
                display_image(aqp_digraph, display_canvas)  # Update to use the canvas
                statements, _ = get_qep_statements()
                steps_output.delete("1.0", tk.END)  # Clear the text box
                steps_output.insert(tk.END, '\n'.join(statements))  # Add actual query steps
                cost_label.config(text=f"AQP Cost: {aqp_query_cost}")
            disconnect_db()
        except Exception as e:
            steps_output.delete("1.0", tk.END)  # Clear the text box
            steps_output.insert(tk.END, f"Error: {str(e)}\n")  # Add error message

    query_thread = Thread(target=execute_query_thread)
    query_thread.start()


# Function to open the image in a full-screen window with scrollwheel zoom
def open_full_image(image_path):
    try:
        # Create a new full-screen window
        full_image_window = tk.Toplevel(window)
        full_image_window.title("Full Image Viewer")
        full_image_window.attributes("-fullscreen", True)

        # Bind the Escape key to exit full-screen mode
        full_image_window.bind("<Escape>", lambda e: full_image_window.destroy())

        # Add a close button
        close_button = tk.Button(
            full_image_window,
            text="Exit Fullscreen",
            font=("Helvetica", 12),
            bg="#ff4d4d",
            fg="white",
            command=full_image_window.destroy
        )
        close_button.pack(side=tk.TOP, anchor="e", padx=10, pady=10)

        # Create a canvas for the image
        canvas = tk.Canvas(full_image_window, bg="black")
        canvas.pack(fill=tk.BOTH, expand=True)

        # Open the image
        image = Image.open(image_path).convert("RGB")
        tk_image = ImageTk.PhotoImage(image)
        canvas.image = tk_image  # Prevent garbage collection

        # Add the image to the canvas
        img_id = canvas.create_image(0, 0, anchor="nw", image=tk_image)

        # Update the scroll region
        canvas.config(scrollregion=canvas.bbox(img_id))

        # Track zoom level
        scale = 1.0

        # Function to zoom the image
        def zoom(event):
            nonlocal scale
            zoom_factor = 1.1 if event.delta > 0 else 0.9  # Zoom in or out
            scale *= zoom_factor

            # Resize the image while maintaining aspect ratio
            new_width = int(image.width * scale)
            new_height = int(image.height * scale)
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            tk_resized_image = ImageTk.PhotoImage(resized_image)

            # Update the image on the canvas
            canvas.itemconfig(img_id, image=tk_resized_image)
            canvas.image = tk_resized_image  # Prevent garbage collection

            # Center the image on the canvas
            canvas.coords(img_id, canvas.winfo_width() // 2, canvas.winfo_height() // 2)

            # Update scroll region to fit the resized image
            canvas.config(scrollregion=canvas.bbox(img_id))

        # Bind the scrollwheel to the zoom function
        canvas.bind("<MouseWheel>", zoom)

        # Panning variables
        pan_start_x = 0
        pan_start_y = 0

        # Function to start panning
        def start_pan(event):
            nonlocal pan_start_x, pan_start_y
            pan_start_x = event.x
            pan_start_y = event.y

        # Function to execute panning
        def do_pan(event):
            nonlocal pan_start_x, pan_start_y
            dx = event.x - pan_start_x
            dy = event.y - pan_start_y
            canvas.move("all", dx, dy)
            pan_start_x = event.x
            pan_start_y = event.y

        # Bind mouse events for panning
        canvas.bind("<ButtonPress-1>", start_pan)
        canvas.bind("<B1-Motion>", do_pan)

    except Exception as e:
        print(f"Error displaying full image: {e}")

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

        # Bind double-click to open the full image
        canvas.bind("<Double-1>", lambda event: open_full_image(image_path))

    except Exception as e:
        print(f"Error displaying image: {e}")


# # Cost Comparison at the bottom
# cost_panel = tk.Frame(window, height=40, bg="#f0f0f0")
# cost_panel.grid(row=2, column=0, columnspan=2, sticky="nsew")

# qep_cost_label = tk.Label(cost_panel, text=f"QEP Cost: {query_cost}", font=("Segoe UI", 10, "bold"), fg="#ff4d4d" if aqp_query_cost < query_cost else "#27ae60", bg="#f0f0f0")
# qep_cost_label.pack(side="left", padx=10)

# aqp_cost_label = tk.Label(cost_panel, text=f"AQP Cost: {aqp_query_cost}", font=("Segoe UI", 10, "bold"), fg="#27ae60" if aqp_query_cost < query_cost else "#ff4d4d", bg="#f0f0f0")
# aqp_cost_label.pack(side="left", padx=10)

# Start the mainloop
window.mainloop()
