import sys
import time
import tkinter as tk

from io import StringIO
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw
from TSP_Solver import TSP_Solver

"""This file implements the graphical user interface for a Binary Particle Swarm Optimisation Algorithm that is used 
to solve the Travelling Salesman Problem. The GUI is composed of 4 frames, 1 for parameters, 1 for displaying the cmd 
output, 1 for showing a graph of current solution and 1 for showing the graph of the optimal solution."""


cmd_output = ""
# Optimal routes and distances have been used from the GA teaching tool
optimal_routes = {
    "5": [543, 317, 881, 179, 576, 579, 579, 782, 237, 609],
    "10": [647, 174, 608, 188, 267, 301, 262, 345, 427, 594, 192, 979, 441, 940, 729, 714, 650, 464, 897, 362],
    "15": [311, 630, 390, 472, 370, 429, 375, 403, 230, 317, 475, 268, 609, 222, 573, 104, 908, 114, 614, 477, 922, 894,
           596, 891, 640, 826, 580, 689, 341, 666],
    "20": [157, 282, 142, 317, 145, 431, 239, 644, 336, 628, 370, 871, 352, 888, 521, 961, 945, 918, 993, 931, 965, 619,
           886, 715, 844, 698, 559, 747, 590, 657, 535, 456, 706, 257, 419, 167, 360, 314, 245, 409]
}

best_distances = {
    "5": 1877.3563,
    "10": 2655.0572,
    "15": 3095.7532,
    "20": 3514.2509
}

# Pop-ups to be displayed after the user presses a button in the menu


def about():
    messagebox.showinfo("About", "This is a tool for visualising how PSO solves the TSP, "
                                 "developed as part of an undergraduate dissertation project done by Alicja Szwalek")


def instructions():
    messagebox.showinfo("Instructions", "To run the tool press the 'Run' button. "
                                        "The output of the command line will be shown in the right-top window after "
                                        "the algorithm finishes running. This is automatically scrolled down to show "
                                        "you the last iteration. "
                                        "The optimal distance is the length of the "
                                        "shortest possible route, which is shown in the right-bottom window. "
                                        "The best route obtained by the algorithm will be shown in the left-bottom "
                                        "window after the algorithm finishes running. ")


def run_gui():
    root = tk.Tk()
    root.title("PSO Tool")
    root.geometry("1000x650")
    menubar = tk.Menu(root)

    # Create frames
    frame1 = tk.Frame(root, width=480, height=280)
    frame2 = tk.Frame(root, width=480, height=280)
    frame3 = tk.Frame(root, width=480, height=280)
    frame4 = tk.Frame(root, width=480, height=280)

    # Put frames into the window
    frame1.grid(row=0, column=0, padx=0, pady=10)
    frame2.grid(row=0, column=1, padx=0, pady=10)
    frame3.grid(row=1, column=0, padx=10, pady=10)
    frame4.grid(row=1, column=1, padx=5, pady=10)

    # Create an instance of TSP Solver
    tsp_solver = TSP_Solver()

    # -------------------------- FRAME 1 --------------------------
    label1 = tk.Label(frame1, text="Change parameters", font=("Arial", 16))
    label1.grid(row=0, column=0, columnspan=2)

    # Dropdown button for difficulty
    label_difficulty = tk.Label(frame1, text="Change difficulty", font=("Arial", 12))
    label_difficulty.grid(row=1, column=0, sticky=tk.E)

    options = ["5", "10", "15", "20"]
    selected_difficulty = tk.StringVar(frame1)
    selected_difficulty.set(options[0])
    dropdown = tk.OptionMenu(frame1, selected_difficulty, *options)
    dropdown.grid(row=1, column=1, sticky=tk.W)

    def read_cities(*args):
        """
        Read cities from the csv_cities folder depending on the selected difficulty
        """
        difficulty = selected_difficulty.get()
        filepath = f"csv_cities/difficulty_{difficulty}.csv"
        tsp_solver.read_cities(filepath)

    selected_difficulty.trace('w', read_cities)

    # ---------Number of iterations-------------
    label_iterations = tk.Label(frame1, text="Number of iterations", font=("Arial", 12))
    label_iterations.grid(row=2, column=0, sticky=tk.E)

    # Field for entering the number of iterations
    enter_iterations = tk.Entry(frame1, width=7)
    enter_iterations.grid(row=2, column=1, sticky=tk.W)
    enter_iterations.insert(0, "20")

    # ----------Population size----------------
    label_population = tk.Label(frame1, text="Population size", font=("Arial", 12))
    label_population.grid(row=3, column=0, sticky=tk.E)

    # Field for entering the population size
    enter_population = tk.Entry(frame1, width=7)
    enter_population.grid(row=3, column=1, sticky=tk.W)
    enter_population.insert(0, "10")

    # ----------Inertia weight----------------
    label_inertia = tk.Label(frame1, text="Inertia weight:", font=("Arial", 12))
    label_inertia.grid(row=4, column=0, sticky=tk.E + tk.S)

    # Field for entering the inertia weight
    enter_inertia = tk.Scale(frame1, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
    enter_inertia.grid(row=4, column=1, sticky=tk.W)
    enter_inertia.set(0.5)  # default value

    # ----------Social parameter----------------
    label_social = tk.Label(frame1, text="Social coefficient:", font=("Arial", 12))
    label_social.grid(row=5, column=0, sticky=tk.E + tk.S)

    # Field for entering the social parameter
    enter_social = tk.Scale(frame1, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
    enter_social.grid(row=5, column=1, sticky=tk.W)
    enter_social.set(0.5)  # default value

    # ----------Cognitive parameter----------------
    label_cognitive = tk.Label(frame1, text="Cognitive coefficient:", font=("Arial", 12))
    label_cognitive.grid(row=6, column=0, sticky=tk.E + tk.S)

    # Field for entering the cognitive parameter
    enter_cognitive = tk.Scale(frame1, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
    enter_cognitive.grid(row=6, column=1, sticky=tk.W)
    enter_cognitive.set(0.5)  # default value

    # -----------Run the algorithm-----------------
    runtime = 0

    def run_pso():
        global runtime
        # clear the print messages from the previous run
        output_box.config(state=tk.NORMAL)
        output_box.delete('1.0', tk.END)
        output_box.config(state=tk.DISABLED)

        sys.stdout = StringIO()
        sys.stderr = StringIO()

        iterations = int(enter_iterations.get())
        population_size = int(enter_population.get())
        difficulty = selected_difficulty.get()
        filepath = f"csv_cities/difficulty_{difficulty}.csv"

        tsp_solver_instance = TSP_Solver(population_size, iterations)
        tsp_solver_instance.read_cities(filepath)

        start_time = time.time()  # Start the timer
        output_text = "Running PSO...\n"
        tsp_solver_instance.run()

        end_time = time.time()  # End the timer
        runtime = end_time - start_time  # Calculate the runtime

        # Append the output text to the output box
        append_output(output_text)

        cmd_out = sys.stdout.getvalue()
        # Reset stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        # Append any other command output to the output box
        append_output(cmd_out)

        # Show the current tour in frame3
        show_current_route(frame3, tsp_solver_instance.g_best_tour)

        # Update the runtime label with the calculated runtime
        runtime_label.config(text=f"Runtime: {runtime:.4f} seconds")

    run_button = tk.Button(frame1, text="Run", command=run_pso, width=10, height=1, font="Arial")
    run_button.grid(row=7, column=0, columnspan=2, pady=4)

    # -------------------------- FRAME 2 --------------------------
    label_output_title = tk.Label(frame2, text="Command Line Output", font=("Arial", 12))
    label_output_title.grid(row=0, column=0, padx=10, pady=5)

    def append_output(text):
        global cmd_output
        cmd_output += text + "\n"
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, text + "\n")
        output_box.yview(tk.END)  # scroll to the bottom of the output box
        output_box.config(state=tk.DISABLED)

    output_box = tk.Text(frame2, width=59, height=15)
    output_box.grid(row=1, column=0, padx=10, pady=10)
    output_box.config(state=tk.DISABLED)

    # Label for the runtime that gets updated later
    runtime_label = tk.Label(frame2, text="", font=("Arial", 11))
    runtime_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

    # Label for the best distance that gets updated later
    best_distance_label = tk.Label(frame2, text="", font=("Arial", 11))
    best_distance_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    def update_best_distance(*args):
        difficulty = selected_difficulty.get()
        # Update the label
        best_distance_label.config(text=f"Optimal Distance: {best_distances[difficulty]}")

    # Apply trace to the selected_difficulty
    selected_difficulty.trace('w', update_best_distance)

    # Initial update
    update_best_distance()

    # -------------------------- FRAME 3 --------------------------
    def show_current_route(frame, best_tour):
        canvas_width = 480
        canvas_height = 280
        margin = 100  # add space on the edges of the graph

        x_coordinates = [point[0] for point in best_tour]
        y_coordinates = [point[1] for point in best_tour]

        # Find the maximum and minimum coordinates
        min_x = min(x_coordinates) - margin
        max_x = max(x_coordinates) + margin
        min_y = min(y_coordinates) - margin - 50
        max_y = max(y_coordinates) + margin

        # Calculate the scaling factors
        x_scale = canvas_width / ((max_x - min_x) * 1.15)
        y_scale = canvas_height / ((max_y - min_y) * 1.15)

        # Create a white image in frame3
        img = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(img)

        # Draw the lines
        for i in range(0, len(best_tour) - 1):
            x1 = (best_tour[i][0] - min_x) * x_scale
            y1 = (best_tour[i][1] - min_y) * y_scale
            x2 = (best_tour[i + 1][0] - min_x) * x_scale
            y2 = (best_tour[i + 1][1] - min_y) * y_scale
            draw.line((x1, y1, x2, y2), fill="black", width=2)

        # Draw the last line
        x1 = (best_tour[-1][0] - min_x) * x_scale
        y1 = (best_tour[-1][1] - min_y) * y_scale
        x2 = (best_tour[0][0] - min_x) * x_scale
        y2 = (best_tour[0][1] - min_y) * y_scale
        draw.line((x1, y1, x2, y2), fill="black", width=2)

        # Draw the points
        for point in best_tour:
            x = (point[0] - min_x) * x_scale
            y = (point[1] - min_y) * y_scale
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="green")

        # Convert image to Tkinter PhotoImage
        img_tk = ImageTk.PhotoImage(img)

        # clear canvas
        for item in frame.winfo_children():
            item.destroy()

        # Display the image on the canvas
        canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk
        canvas.create_text(canvas_width / 2, 10, text="Current Solution", font=("Arial", 14), anchor=tk.N)
        canvas.pack()

    # -------------------------- FRAME 4 --------------------------
    def show_optimal_route(frame, difficulty):
        optimal_route = optimal_routes[difficulty]
        canvas_width = 480
        canvas_height = 280

        # Find the maximum and minimum coordinates in the optimal route
        margin = 100  # add space on the edges of the graph
        min_x = min(optimal_route[::2]) - margin
        max_x = max(optimal_route[::2]) + margin
        min_y = min(optimal_route[1::2]) - margin - 50
        max_y = max(optimal_route[1::2]) + margin

        # Calculate the scaling factors
        x_scale = canvas_width / ((max_x - min_x) * 1.15)
        y_scale = canvas_height / ((max_y - min_y) * 1.15)

        # Create a white image in frame4
        img = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(img)

        # Draw the lines
        for i in range(0, len(optimal_route) - 2, 2):
            x1 = (optimal_route[i] - min_x) * x_scale
            y1 = (optimal_route[i + 1] - min_y) * y_scale
            x2 = (optimal_route[i + 2] - min_x) * x_scale
            y2 = (optimal_route[i + 3] - min_y) * y_scale
            draw.line((x1, y1, x2, y2), fill="black", width=2)

        # Draw the last line
        x1 = (optimal_route[-2] - min_x) * x_scale
        y1 = (optimal_route[-1] - min_y) * y_scale
        x2 = (optimal_route[0] - min_x) * x_scale
        y2 = (optimal_route[1] - min_y) * y_scale
        draw.line((x1, y1, x2, y2), fill="black", width=2)

        # Draw the points
        for i in range(0, len(optimal_route), 2):
            x = (optimal_route[i] - min_x) * x_scale
            y = (optimal_route[i + 1] - min_y) * y_scale
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

        # Convert image to Tkinter PhotoImage
        img_tk = ImageTk.PhotoImage(img)

        # clear canvas
        for item in frame.winfo_children():
            item.destroy()

        # Display the image on the canvas
        canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk
        canvas.create_text(canvas_width / 2, 10, text="Optimal Solution", font=("Arial", 14), anchor=tk.N)
        canvas.pack()

    show_optimal_route(frame4, options[0])

    selected_difficulty.trace('w', lambda *args: show_optimal_route(frame4, selected_difficulty.get()))

    # Create the menu buttons
    about_menu = tk.Menu(menubar, tearoff=0)
    about_menu.add_command(label="About", command=about)
    about_menu.add_command(label="Instructions", command=instructions)

    # Add the "About" menu to the menu
    menubar.add_cascade(label="About", menu=about_menu)

    # Display the menu bar
    root.config(menu=menubar)

    # Run the main loop
    root.mainloop()


if __name__ == '__main__':
    tsp_solver = TSP_Solver()
    tsp_solver.read_cities('csv_cities/difficulty_20.csv')
    run_gui()

