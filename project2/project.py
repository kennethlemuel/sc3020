import tkinter as tk
from PIL import Image, ImageTk
from interface import create_scrollable_canvas, create_legend, resize_image,\
    open_fullsize_image, view_statement_details
from preprocessing import connect_to_db, get_block_size, get_buffer_size, get_qep_image, \
                 close_db_connection, get_qep_statements, get_aqp
from threading import Thread
import tkinter.font as tkFont

# Global variables
global create_legend_flag, legend_canvas, click_instruction_label
legend_canvas = None
create_legend_flag = False
click_instruction_label = None

# Function to execute the SQL query
def execute_sql_query():
    global click_instruction_label, create_legend_flag
     # Update status to show the query is starting
    status_label.config(text="Executing SQL Query...", fg="blue")  # Added status update

    # Function to execute the SQL query in a separate thread
    def execute_query_thread():
        global click_instruction_label, create_legend_flag
        try:
            connect_to_db()

            # Fetch the QEP image
            qep_digraph = get_qep_image(query)

            # Check if QEP is None, indicating an invalid query
            if qep_digraph is None:
                result_label.config(text="Error: Invalid query. Please check your SQL syntax.")
                status_label.config(text="Error: Invalid SQL syntax.", fg="red")  # Error status update
                return

            statements, details = get_qep_statements()
            buffer_size = get_buffer_size()
            blk_size = get_block_size()

            close_db_connection()

            # Save the QEP digraph as a PNG file
            qep_digraph.format = 'png'
            try:
                qep_digraph.render(filename="qep_tree")
            except Exception as e:
                print(e)

            # Open the QEP image and convert it to Tkinter PhotoImage
            qep_image = Image.open("qep_tree.png")
            max_dimensions = (600, 600)  # Maximum dimensions for the image
            resized_qep_img = resize_image("qep_tree.png", max_dimensions)

            qep_image = ImageTk.PhotoImage(resized_qep_img)
            qep_label.bind("<Button-1>", lambda e: open_fullsize_image())

            qep_label.config(image=qep_image)
            qep_label.image = qep_image
            qep_label.pack(side="top", fill="both", expand=True)

            # Define a bold font
            bold_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

            # Check if the label already exists, if not create it
            if click_instruction_label is None:
                click_instruction_label = tk.Label(qep_label.master, text="Click on the image to view it in full size", font=bold_font)
                click_instruction_label.pack(side="top")
            else:
                click_instruction_label.config(text="Click on the image to view it in full size", font=bold_font)

            # Update the statements in the right frame
            analysis_output_label.config(text='\n'.join(statements), font=("Helvetica", 10))
            analysis_output_label.pack(side="top", fill="both", expand=True)
            for widget in right_frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.destroy()
            for i, detail in enumerate(details):
                button = tk.Button(right_frame, text=f"Step {i+1} Details", command=lambda s=detail: view_statement_details(window, s))
                button.pack()

            # Check if the legend has been created already
            if not create_legend_flag:
                create_legend(left_frame, legend_items, create_legend_flag, legend_canvas)
                create_legend_flag = True

            # Successful execution status update
            status_label.config(text="Query executed successfully!", fg="green")  # Success status update

        except Exception as e:
            result_label.config(text=f"Error: {str(e)}")
            status_label.config(text=f"Execution failed: {str(e)}", fg="red")  # Exception status update

    # Get the query from the entry field
    query = sql_entry.get()

    # Create a thread to execute the query
    query_thread = Thread(target=execute_query_thread)
    query_thread.start()
    
# Function to execute the SQL query
def execute_aqp_query():
    global click_instruction_label, create_legend_flag
    # Function to execute the SQL query in a separate thread
    def execute_query_thread():
        global click_instruction_label, create_legend_flag
        try:
            connect_to_db()
            
            # Fetch the QEP image
            qep_digraph = get_aqp(query, False, True, True, True, True)
            print(qep_digraph)

            # Check if QEP is None, indicating an invalid query
            if qep_digraph is None:
                result_label.config(text="Error: Invalid query. Please check your SQL syntax.")
                return
            print("success1")

            statements, details = get_qep_statements()
            buffer_size = get_buffer_size()
            blk_size = get_block_size()
            
            print("success2")
            
            close_db_connection()

            print("success3")

            # Save the QEP digraph as a PNG file
            qep_digraph.format = 'png'
            print("success3.5")
            
            try:
                qep_digraph.render(filename="qep_tree")
            except Exception as e:
                print(e)
            
            print("success4")

            # Open the QEP image and convert it to Tkinter PhotoImage
            qep_image = Image.open("qep_tree.png")
            
            print("success5")

            max_dimensions = (600, 600)  # Maximum dimensions for the image
            resized_qep_img = resize_image("qep_tree.png", max_dimensions)

            qep_image = ImageTk.PhotoImage(resized_qep_img)
            qep_label.bind("<Button-1>", lambda e: open_fullsize_image())

            qep_label.config(image=qep_image)
            qep_label.image = qep_image
            qep_label.pack(side="top", fill="both", expand=True)

            # Define a bold font
            bold_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

            # Check if the label already exists, if not create it
            if click_instruction_label is None:
                click_instruction_label = tk.Label(qep_label.master, text="Click on the image to view it in full size", font=bold_font)
                click_instruction_label.pack(side="top")
            else:
                # Optionally update the label text or properties if needed
                click_instruction_label.config(text="Click on the image to view it in full size", font=bold_font)

            # Update the statements in the right frame
            analysis_output_label.config(text='\n'.join(statements), font=("Helvetica", 10))
            analysis_output_label.pack(side="top", fill="both", expand=True)
            for widget in right_frame.winfo_children():
                if (isinstance(widget, tk.Button)):
                    widget.destroy()
            for i, detail in enumerate(details):
                button = tk.Button(right_frame, text=f"Step {i+1} Details", command=lambda s=detail: view_statement_details(window, s))
                button.pack()
            # Check if the legend has been created already
            if not create_legend_flag:
                # Call create_legend function
                create_legend(left_frame, legend_items, create_legend_flag, legend_canvas)
                # Set the flag to True to avoid recreating the legend
                create_legend_flag = True

        except Exception as e:
            result_label.config(text=f"Error: {str(e)}")

    # Get the query from the entry field
    query = sql_entry.get()

    # Create a thread to execute the query
    query_thread = Thread(target=execute_query_thread)
    query_thread.start()


# Create the main window
window = tk.Tk()
window.title("SQL Query Executor")

# Set the window to maximize on startup
window.state("zoomed") 

# Set the window size to cover the entire screen
window.geometry(f"{int(4.5/5*window.winfo_screenwidth())}x{window.winfo_screenheight()}")

# Create a top canvas for title, entry field, and button
top_canvas = tk.Canvas(window)
top_canvas.pack(side=tk.TOP, padx=10, pady=10)

# Create frames for different sections
query_panel = tk.Frame(window, height=100, bg="lightgrey")  # Query entry panel
query_panel.pack(side="top", fill="x", padx=10, pady=10)

qep_panel = tk.Frame(window, height=300, bg="white")  # QEP visualization panel
qep_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)

aqp_panel = tk.Frame(window, height=300, bg="white")  # AQP visualization panel
aqp_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)

cost_panel = tk.Frame(window, height=50, bg="lightgrey")  # Cost comparison panel
cost_panel.pack(side="bottom", fill="x", padx=10, pady=10)

# Add labels to each panel for clarity
tk.Label(query_panel, text="Query Panel", font=("Helvetica", 12, "bold"), bg="lightgrey").pack(side="top")
tk.Label(qep_panel, text="QEP Panel", font=("Helvetica", 12, "bold")).pack(side="top")
# Dropdown for operator selection
operator_var = tk.StringVar(qep_panel)
operator_var.set("Select Operator")  # default value

operator_dropdown = tk.OptionMenu(qep_panel, operator_var, "Hash Join", "Merge Join")
operator_dropdown.pack(pady=5)

# Button to apply changes based on selected operator
apply_operator_button = tk.Button(qep_panel, text="Apply Operator Change", font=("Helvetica", 10),
                                  command=lambda: modify_operator(operator_var.get()))
apply_operator_button.pack(pady=5)

tk.Label(aqp_panel, text="AQP Panel", font=("Helvetica", 12, "bold")).pack(side="top")
tk.Label(cost_panel, text="Cost Comparison", font=("Helvetica", 12, "bold"), bg="lightgrey").pack(side="top")
# Sample cost comparison values for QEP and AQP
qep_cost = 500  # Placeholder value; replace with actual QEP cost retrieval
aqp_cost = 400  # Placeholder value; replace with actual AQP cost retrieval

# Display cost comparison with color coding
qep_cost_label = tk.Label(cost_panel, text=f"QEP Cost: {qep_cost}", font=("Helvetica", 10, "bold"),
                          fg="green" if aqp_cost < qep_cost else "red")
qep_cost_label.pack(side="left", padx=10)

aqp_cost_label = tk.Label(cost_panel, text=f"AQP Cost: {aqp_cost}", font=("Helvetica", 10, "bold"),
                          fg="green" if aqp_cost < qep_cost else "red")
aqp_cost_label.pack(side="left", padx=10)

title_label = tk.Label(top_canvas, text="Enter SQL Query", font=("Helvetica", 18, "bold"))
title_label.pack(pady=(10, 5)) 


sql_entry = tk.Entry(top_canvas, width=70, font=("Helvetica", 12))
sql_entry.pack(pady=(5, 10))


execute_button = tk.Button(top_canvas, text="Execute Query", command=execute_sql_query, font=("Helvetica", 12, "bold"))
execute_button.pack(pady=(5, 5))

execute_aqp_button = tk.Button(top_canvas, text="Execute AQP Query", command=execute_aqp_query, font=("Helvetica", 12, "bold"))
execute_aqp_button.pack(pady=(0, 10))


# Create scrollable left and right canvases
left_canvas, left_frame = create_scrollable_canvas(window, side=tk.LEFT, min_width=400)
right_canvas, right_frame = create_scrollable_canvas(window, side=tk.RIGHT, min_width=400)

# Create a label to display the QEP analysis output in the right canvas
analysis_output_label = tk.Label(right_frame, text="", font=("Helvetica", 12), justify=tk.LEFT, wraplength=550)
analysis_output_label.place()

# Legend items
legend_items = [
    {"text": "Start-up cost: Estimated units to start up a node to start a query"},
    {"text": "Total cost: Estimated units to finish processing and return results"},
    {"text": "Shared Hit Blocks: Number of shared blocks read from buffer"},
    {"text": "Local Read Blocks: Number of local blocks read into buffer"}
]

# Create a label to display the QEP image in the left canvas
qep_label = tk.Label(left_frame, font=("Helvetica", 12))
qep_label.place()

# Create a label to display the result in the left canvas
result_label = tk.Label(left_frame, text="", font=("Helvetica", 12))
result_label.place()

# Create a frame for displaying status messages at the bottom
status_frame = tk.Frame(window, height=30, bg="lightgrey")
status_frame.pack(side="bottom", fill="x")

# Add a label inside the status frame to display messages
status_label = tk.Label(status_frame, text="Status: Ready", anchor="w", font=("Helvetica", 10))
status_label.pack(fill="x", padx=10)


# Start the mainloop
window.mainloop()