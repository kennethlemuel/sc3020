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

def create_operator_buttons(qep_steps):
    # Clear any existing operator buttons in the right_frame
    for widget in right_frame.winfo_children():
        if isinstance(widget, (tk.OptionMenu, tk.Label)):
            widget.destroy()

    # Loop through each step in the QEP and create a dropdown for it
    for i, step in enumerate(qep_steps):
        relation_name = step.get("Relation Name", "Unknown")
        step_label = tk.Label(right_frame, text=f"Step {i + 1}: {step['Node Type']} on {relation_name}")
        step_label.pack(side="top", anchor="w", padx=10)

        # For scan operations, create a dropdown for selecting scan type
        if step["Node Type"] in ["Seq Scan", "Index Scan"]:
            scan_var = tk.StringVar(right_frame)
            scan_var.set("Select Scan Type")
            scan_dropdown = tk.OptionMenu(
                right_frame, scan_var, "Seq Scan", "Index Scan",
                command=lambda op, step=i: update_operator_selection(step, op)
            )
            scan_dropdown.pack(side="top", padx=10, pady=5)

        # For join operations, create dropdowns for Join Type and Join Order
        elif step["Node Type"] in ["Hash Join", "Merge Join", "Nested Loop"]:
            # Join Type Dropdown
            join_type_var = tk.StringVar(right_frame)
            join_type_var.set("Select Join Type")
            join_type_dropdown = tk.OptionMenu(
                right_frame, join_type_var, "Hash Join", "Index Join", "Nested Loop Join",
                command=lambda op, step=i: update_operator_selection(step, op)
            )
            join_type_dropdown.pack(side="top", padx=10, pady=5)

            # Extract the names of the relations involved in this join operation
            if "Plans" in step and len(step["Plans"]) >= 2:
                left_relation = step["Plans"][0].get("Relation Name", "Unknown")
                right_relation = step["Plans"][1].get("Relation Name", "Unknown")

                # Join Order Dropdown
                join_order_var = tk.StringVar(right_frame)
                join_order_var.set("Select Join Order")
                join_order_dropdown = tk.OptionMenu(
                    right_frame, join_order_var,
                    f"{left_relation} join {right_relation}",
                    f"{right_relation} join {left_relation}",
                    command=lambda order, step=i: update_operator_selection(f"{step}_order", order)
                )
                join_order_dropdown.pack(side="top", padx=10, pady=5)

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
        global click_instruction_label, create_legend_flag, qep_json
        try:
            connect_db()
            qep_digraph = get_qep(query)
            if qep_digraph is None:
                result_label.config(text="Error: Invalid query. Please check your SQL syntax.")
                status_label.config(text="Error: Invalid SQL syntax.", fg="red")
                return

            # Extract QEP steps by parsing the JSON structure
            qep_steps = parse_qep_steps(qep_digraph['Plan'])  # Assuming the QEP JSON has a root 'Plan' node
            buffer_size = get_buffer_size()
            blk_size = get_block_size()
            disconnect_db()

            # Create operator selection buttons for each step in the QEP
            create_operator_buttons(qep_steps)
             # Display success status
            status_label.config(text="Query executed successfully!", fg="green")
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
            result_label.config(text="Query executed successfully!")

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
                click_instruction_label.config(text="Click on the image to view it in full size", font=bold_font)

            # Update the statements in the right frame
            analysis_output_label.config(text='\n'.join(statements), font=("Verdana", 10))
            analysis_output_label.pack(side="top", fill="both", expand=True)
            for widget in right_frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.destroy()
            for i, detail in enumerate(details):
                button = tk.Button(aqp_display_frame, text=f"Step {i+1} Details", command=lambda s=detail: view_statement_details(window, s))
                button.pack()

            if not create_legend_flag:
                create_legend(qep_panel, legend_items, create_legend_flag, legend_canvas)
                create_legend_flag = True

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
                create_legend(qep_panel, legend_items, create_legend_flag, legend_canvas)
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

qep_panel = tk.Frame(window, height=300, bg="#ffffff")  # QEP visualization panel
qep_panel.pack(side="left", fill="both", expand=True, padx=2, pady=2)

execute_button = tk.Button(top_canvas, text="Execute Query", command=execute_sql_query, font=("Segoe UI", 12, "bold"), bg="#4a90e2", fg="#ffffff")
execute_button.pack(pady=(5, 5))

cost_panel = tk.Frame(window, height=40, bg="#f0f0f0")  # Cost comparison panel
cost_panel.pack(side="bottom", fill="x", padx=10, pady=10)

# Add labels to each panel for clarity
tk.Label(query_panel, text="Query Panel", font=("Verdana", 12, "bold"), bg="lightgrey").pack(side="top")
tk.Label(qep_panel, text="QEP Panel", font=("Verdana", 12, "bold")).pack(side="top")

operator_var = tk.StringVar(qep_panel)
operator_var.set("Select Operator")  # default value
operator_dropdown = tk.OptionMenu(qep_panel, operator_var, "Hash Join", "Merge Join")
operator_dropdown.pack(pady=5)

# Button to apply changes based on selected operator
apply_operator_button = tk.Button(qep_panel, text="Apply Operator Change", font=("Verdana", 10),
                                  command=lambda: modify_operator(operator_var.get()))
apply_operator_button.pack(pady=5)

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

generate_aqp_button = tk.Button(top_canvas, text="Generate AQP with Selections", command=generate_aqp_with_selections, font=("Segoe UI", 12, "bold"), bg="#4a90e2", fg="#ffffff")
generate_aqp_button.pack(pady=(0, 10))

execute_aqp_button = tk.Button(top_canvas, text="Execute AQP Query", command=execute_aqp_query, font=("Segoe UI", 12, "bold"), bg="#4a90e2", fg="#ffffff")
execute_aqp_button.pack(pady=(0, 10))


# Create scrollable left and right canvases
left_canvas, left_frame = create_scrollable_canvas(window, side=tk.LEFT, min_width=300)
right_canvas, right_frame = create_scrollable_canvas(window, side=tk.RIGHT, min_width=300)
right_frame.pack(fill="both", expand=True)


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

qep_label = tk.Label(right_frame, text="Display AQP", font=("Verdana", 12, "bold")).pack(side="top")
#qep_label = tk.Label(right_frame, text="Display AQP", font=("Verdana", 10))
#qep_label.pack()

# Placeholder for QEP display
qep_display = tk.Text(right_frame, wrap=tk.WORD, font=("Verdana", 12), state=tk.DISABLED)
qep_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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
