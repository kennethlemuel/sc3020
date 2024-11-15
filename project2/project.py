import tkinter as tk
from PIL import Image, ImageTk
from interface import create_scrollable_canvas, create_legend, resize_image, open_fullsize_image, view_statement_details
from preprocessing import connect_db, get_block_size, get_buffer_size, get_qep, disconnect_db, get_qep_statements, get_aqp
from threading import Thread
import tkinter.font as tkFont

# Global variables
global create_legend_flag, legend_canvas, click_instruction_label
legend_canvas = None
create_legend_flag = False
click_instruction_label = None
operator_selections = {}

def update_operator_selection(step, selected_operator):
    operator_selections[step] = selected_operator

def parse_qep_steps(plan, steps=None):
    if steps is None:
        steps = []
    steps.append(plan)  # Append the current step
    if "Plans" in plan:
        for subplan in plan["Plans"]:
            parse_qep_steps(subplan, steps)
    return steps


# Main Window Configuration
window = tk.Tk()
window.title("SQL Query Executor")
window.state("zoomed")
window.geometry(f"{int(4.5/5*window.winfo_screenwidth())}x{window.winfo_screenheight()}")

# Define fonts after initializing the Tk window
bold_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

# Functions
def execute_sql_query():
    global click_instruction_label, create_legend_flag
    status_label.config(text="Executing SQL Query...", fg="blue")

    def execute_query_thread():
        global click_instruction_label, create_legend_flag
        try:
            connect_db()
            # Fetch the QEP digraph and JSON structure
            qep_digraph, qep_json_structure = get_qep(query)

            if qep_digraph is None or qep_json_structure is None:
                result_label.config(text="Error: Invalid query. Please check your SQL syntax.")
                status_label.config(text="Error: Invalid SQL syntax.", fg="red")
                return

            # Save and display QEP image
            qep_image_path = "project2/qep_tree.png"
            try:
                image = Image.open(qep_image_path).convert("RGB")
                resized_image = image.resize((600, 600), Image.LANCZOS)
                qep_image = ImageTk.PhotoImage(resized_image)
                qep_display.config(image=qep_image)
                qep_display.image = qep_image
                qep_display.pack(fill="both", expand=True)
            except Exception as e:
                print(f"Error loading image into Tkinter: {e}")

            status_label.config(text="Query executed successfully!", fg="green")
        except Exception as e:
            result_label.config(text=f"Error: {str(e)}")
            status_label.config(text=f"Execution failed: {str(e)}", fg="red")

    query = sql_entry.get()
    query_thread = Thread(target=execute_query_thread)
    query_thread.start()



def generate_aqp_with_selections():
    query = sql_entry.get()

    # Call get_aqp with operator selections applied for each join type
    aqp_digraph = get_aqp(
        query,
        hashjoin_enabled=operator_selections.get(0, "Hash Join") == "Hash Join",
        mergejoin_enabled=operator_selections.get(1, "Merge Join") == "Merge Join",
        nestloop_enabled=operator_selections.get(2, "Nested Loop") == "Nested Loop",
        seqscan_enabled=True,   # Default value; add user control if needed
        indexscan_enabled=True  # Default value; add user control if needed
    )

    # Render and display the updated AQP in the interface
    # Assuming similar rendering steps as in execute_sql_query


# Function to execute the SQL query
def execute_aqp_query():
    global click_instruction_label, create_legend_flag

    def execute_query_thread():
        global click_instruction_label, create_legend_flag
        try:
            connect_db()
            qep_digraph = get_aqp(query, False, True, True, True, True)
            if qep_digraph is None:
                result_label.config(text="Error: Invalid query. Please check your SQL syntax.")
                return

            statements, details = get_qep_statements()
            buffer_size = get_buffer_size()
            blk_size = get_block_size()
            disconnect_db()

            # Save the QEP digraph as a PNG file
            qep_digraph.format = 'png'
            try:
                qep_digraph.render(filename="qep_tree")
            except Exception as e:
                print(e)

            # Open the QEP image and convert it to Tkinter PhotoImage
            qep_image = ImageTk.PhotoImage(resize_image("qep_tree.png", (600, 600)))
            qep_display.config(image=qep_image)
            qep_display.image = qep_image
            qep_display.pack(fill="both", expand=True)
            qep_display.bind("<Button-1>", lambda e: open_fullsize_image())

            # Display query execution result in the result label
            result_label.config(text="AQP query executed successfully!")

            qep_image = ImageTk.PhotoImage(resized_qep_img)
            qep_label.bind("<Button-1>", lambda e: open_fullsize_image())

            qep_label.config(image=qep_image)
            qep_label.image = qep_image
            qep_label.pack(side="top", fill="both", expand=True)

            # Define a bold font
            bold_font = tkFont.Font(family="Verdana", size=10, weight="bold")

            # Check if the label already exists, if not create it
            if click_instruction_label is None:
                click_instruction_label = tk.Label(qep_label.master, text="Click on the image to view it in full size", font=bold_font)
                click_instruction_label.pack(side="top")
            else:
                # Optionally update the label text or properties if needed
                click_instruction_label.config(text="Click on the image to view it in full size", font=bold_font)

            # Update the statements in the right frame
            analysis_output_label.config(text='\n'.join(statements), font=("Verdana", 10))
            analysis_output_label.pack(side="top", fill="both", expand=True)
            for widget in right_frame.winfo_children():
                if (isinstance(widget, tk.Button)):
                    widget.destroy()
            for i, detail in enumerate(details):
                button = tk.Button(aqp_display_frame, text=f"Step {i+1} Details", command=lambda s=detail: view_statement_details(window, s))
                button.pack()

            if not create_legend_flag:
                create_legend( legend_items, create_legend_flag, legend_canvas)
                create_legend_flag = True

            status_label.config(text="Query executed successfully!", fg="green")
        except Exception as e:
            result_label.config(text=f"Error: {str(e)}")
            status_label.config(text=f"Execution failed: {str(e)}", fg="red")

    query = sql_entry.get()
    query_thread = Thread(target=execute_query_thread)
    query_thread.start()

# Top Panel (Query Entry and Buttons)
top_canvas = tk.Canvas(window)
top_canvas.pack(side=tk.TOP, padx=10, pady=10)

# Create frames for different sections
query_panel = tk.Frame(window, height=80, bg="#f0f0f0") # Query entry panel
query_panel.pack(side="top", fill="x", padx=10, pady=10)


cost_panel = tk.Frame(window, height=40, bg="#f0f0f0")  # Cost comparison panel
cost_panel.pack(side="bottom", fill="x", padx=10, pady=10)

# Add labels to each panel for clarity
tk.Label(query_panel, text="Query Panel", font=("Verdana", 12, "bold"), bg="lightgrey").pack(side="top")


#tk.Label(aqp_panel, text="AQP Panel", font=("Verdana", 12, "bold")).pack(side="top")
tk.Label(cost_panel, text="Cost Comparison", font=("Verdana", 12, "bold"), bg="lightgrey").pack(side="top")
# Sample cost comparison values for QEP and AQP
qep_cost = 500  # Placeholder value; replace with actual QEP cost retrieval
aqp_cost = 400  # Placeholder value; replace with actual AQP cost retrieval

# Display cost comparison with color coding
qep_cost_label = tk.Label(cost_panel, text=f"QEP Cost: {qep_cost}", font=("Segoe UI", 10, "bold"), fg="#ff4d4d" if aqp_cost < qep_cost else "#27ae60", bg="#f0f0f0")
qep_cost_label.pack(side="left", padx=10)

aqp_cost_label = tk.Label(cost_panel, text=f"AQP Cost: {aqp_cost}", font=("Segoe UI", 10, "bold"), fg="#27ae60" if aqp_cost < qep_cost else "#ff4d4d", bg="#f0f0f0")
aqp_cost_label.pack(side="left", padx=10)

title_label = tk.Label(top_canvas, text="Enter SQL Query", font=("Verdana", 18, "bold"), fg="#4a90e2", bg="#ffffff")
title_label.pack(pady=(10, 5)) 


sql_entry = tk.Entry(top_canvas, width=70, font=("Verdana", 12), bg="#e8f4fa", fg="#333333")
sql_entry.pack(pady=(5, 10))


execute_button = tk.Button(top_canvas, text="Execute Query", command=execute_sql_query, font=("Segoe UI", 12, "bold"), bg="#4a90e2", fg="#ffffff")
execute_button.pack(pady=(5, 5))


execute_aqp_button = tk.Button(top_canvas, text="Execute AQP Query", command=execute_aqp_query, font=("Segoe UI", 12, "bold"), bg="#4a90e2", fg="#ffffff")
execute_aqp_button.pack(pady=(0, 10))


# Create scrollable left and right canvases
left_canvas, left_frame = create_scrollable_canvas(window, side=tk.LEFT, min_width=300)
right_canvas, right_frame = create_scrollable_canvas(window, side=tk.RIGHT, min_width=300)
right_frame.pack(fill="both", expand=True)

# Create separate frames within left_frame and right_frame
image_frame = tk.Frame(left_frame, bg="#ffffff")
image_frame.pack(side="top", fill="both", expand=True)
qep_label = tk.Label(right_frame, text="Display AQP", font=("Verdana", 12, "bold")).pack(side="top")
controls_frame = tk.Frame(right_frame, bg="#ffffff")
controls_frame.pack(side="top", fill="both", expand=True)

# Create a label to display the QEP analysis output in the right canvas
analysis_output_label = tk.Label(right_frame, text="", font=("Verdana", 12), justify=tk.LEFT, wraplength=550)
analysis_output_label.place()

# Legend items
legend_items = [
    {"text": "Start-up cost: Estimated units to start up a node to start a query"},
    {"text": "Total cost: Estimated units to finish processing and return results"},
    {"text": "Shared Hit Blocks: Number of shared blocks read from buffer"},
    {"text": "Local Read Blocks: Number of local blocks read into buffer"}
]

# Create a label to display the QEP image in the left canvas
qep_label = tk.Label(left_frame, font=("Verdana", 12))
qep_label.place()

# Create a label to display the result in the left canvas
result_label = tk.Label(left_frame, text="", font=("Verdana", 12))
result_label.place()

# Placeholder for QEP display
qep_display = tk.Label(image_frame, font=("Verdana", 12))
qep_display.pack(fill="both", expand=True)

#qep_scrollbar = tk.Scrollbar(right_frame, command=qep_display.yview)
#qep_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#qep_display.config(yscrollcommand=qep_scrollbar.set)

# Create a frame for displaying status messages at the bottom
status_frame = tk.Frame(window, height=30, bg="#f0f0f0")
status_frame.pack(side="bottom", fill="x")

# Add a label inside the status frame to display messages
status_label = tk.Label(status_frame, text="Status: Ready", anchor="w", font=("Segoe UI", 10), fg="#333333", bg="#f0f0f0")
status_label.pack(fill="x", padx=10)


# Start the mainloop
window.mainloop()
