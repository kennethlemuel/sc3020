import os
import psycopg2
from graphviz import Digraph
from preprocessing import analyze_qep, add_nodes
import constants

# Function to execute the SQL query
def get_aqp(query, aqp_query):
    try:
        global connection
        global cursor

        # Create a connection to the database
        connection = psycopg2.connect(
            dbname=constants.dbname,
            user=constants.user,
            password=constants.password,
            host=constants.host,
            port=constants.port
        )

        # Create a cursor
        global cursor
        cursor = connection.cursor()
        
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) /*+ {aqp_query} */ {query}"
        print("in")
        cursor.execute(explain_query)
        print("out")
        global qep_json, qep_cost
        qep_cost = 0.0
        qep_json = cursor.fetchone()[0][0]
        analyze_qep(qep_json['Plan'])
        

        # Check if the QEP image is available in the JSON
        if "Plan" in qep_json:
            dot = Digraph(comment="Query Execution Plan")
            dot.graph_attr['bgcolor'] = 'lightyellow'
            add_nodes(dot, qep_json["Plan"])
            
            # Define the file path for the QEP image
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, "aqp_tree")
            dot.format = 'png'
            
            # Render and save the image
            dot.render(filename=image_path, cleanup=True)  # ".png" will be automatically added by Graphviz
            return image_path + ".png", qep_cost  # Return the image path and plan cost
        else:
            return None
        
    except Exception as e:
        # Handle exceptions, and return an informative message
        return [f"Error analyzing the query: {str(e)}"]