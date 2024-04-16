import tkinter as tk
import sys
from io import StringIO
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw
from TSP_Solver import TSP_Solver
from Particle import Particle

cmd_output = ""
optimal_routes = {
    "5": [543, 317, 881, 179, 576, 579, 579, 782, 237, 609],
    "10": [647, 174, 608, 188, 267, 301, 262, 345, 427, 594, 192, 979, 441, 940, 729, 714, 650, 464, 897, 362],
    "15": [311, 630, 390, 472, 370, 429, 375, 403, 230, 317, 475, 268, 609, 222, 573, 104, 908, 114, 614, 477, 922, 894,
           596, 891, 640, 826, 580, 689, 341, 666],
    "20": [157, 282, 142, 317, 145, 431, 239, 644, 336, 628, 370, 871, 352, 888, 521, 961, 945, 918, 993, 931, 965, 619,
           886, 715, 844, 698, 559, 747, 590, 657, 535, 456, 706, 257, 419, 167, 360, 314, 245, 409]
}


def about():
    messagebox.showinfo("About", "This is a tool for visualising how PSO solves the TSP")


def run_gui():
    root = tk.Tk()
    root.title("PSO Tool")
    root.geometry("1000x600")
    menubar = tk.Menu(root)

    frame1 = tk.Frame(root, width=480, height=280)
    frame2 = tk.Frame(root, width=480, height=280)
    frame3 = tk.Frame(root, width=480, height=280)
    frame4 = tk.Frame(root, width=480, height=280)

    # Pack frames into the window (use grid or pack as per your preference)
    frame1.grid(row=0, column=0, padx=10, pady=10)
    frame2.grid(row=0, column=1, padx=10, pady=10)
    frame3.grid(row=1, column=0, padx=10, pady=10)
    frame4.grid(row=1, column=1, padx=10, pady=10)

    tsp_solver = TSP_Solver()

    # FRAME 1
    label1 = tk.Label(frame1, text="Change parameters", font=("Arial", 16))
    label1.grid(row=0, column=0, columnspan=2)

    # Dropdown button for difficulty
    label_difficulty = tk.Label(frame1, text="Change difficulty", font=("Arial", 12))
    label_difficulty.grid(row=1, column=0, sticky=tk.E)

    options = ["5", "10", "15", "20"]
    var = tk.StringVar(frame1)
    var.set(options[0])
    dropdown = tk.OptionMenu(frame1, var, *options)
    dropdown.grid(row=1, column=1, sticky=tk.W)

    def read_cities(*args):
        difficulty = var.get()
        filepath = f"csv_cities/difficulty_{difficulty}.csv"
        tsp_solver.read_cities(filepath)

    var.trace('w', read_cities)

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
    enter_inertia.set(0.01)

    # ----------Social parameter----------------
    label_social = tk.Label(frame1, text="Social parameter:", font=("Arial", 12))
    label_social.grid(row=5, column=0, sticky=tk.E + tk.S)

    # Field for entering the social parameter
    enter_social = tk.Scale(frame1, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
    enter_social.grid(row=5, column=1, sticky=tk.W)
    enter_social.set(0.01)

    # ----------Cognitive parameter----------------
    label_cognitive = tk.Label(frame1, text="Cognitive parameter:", font=("Arial", 12))
    label_cognitive.grid(row=6, column=0, sticky=tk.E + tk.S)

    # Field for entering the cognitive parameter
    enter_cognitive = tk.Scale(frame1, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
    enter_cognitive.grid(row=6, column=1, sticky=tk.W)
    enter_cognitive.set(0.01)

    # -----------Run the algorithm-----------------
    def run_pso():
        # clear the print messages from previous run
        output_box.config(state=tk.NORMAL)
        output_box.delete('1.0', tk.END)
        output_box.config(state=tk.DISABLED)

        sys.stdout = StringIO()
        sys.stderr = StringIO()

        inertia_weight = enter_inertia.get()
        cognitive_param = enter_cognitive.get()
        social_param = enter_social.get()
        iterations = int(enter_iterations.get())
        population_size = int(enter_population.get())
        difficulty = var.get()
        filepath = f"csv_cities/difficulty_{difficulty}.csv"

        print(f"Inertia weight: {inertia_weight}")
        print(f"Cognitive parameter: {cognitive_param}")
        print(f"Social parameter: {social_param}")
        print(f"Iterations: {iterations}")
        print(f"Population size: {population_size}")
        print(f"Difficulty: {difficulty}")

        tsp_solver = TSP_Solver(population_size, iterations)
        tsp_solver.read_cities(filepath)
        pso_solver = Particle(tsp_solver.cities_positions, inertia_weight, cognitive_param, social_param)
        print("Running PSO...")
        tsp_solver.run()

        cmd_output = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__  # Reset stdout
        sys.stderr = sys.__stderr__
        append_output(cmd_output)

        # show the current tour in frame3
        show_current_route(frame3, tsp_solver.best_g_tour)

    run_button = tk.Button(frame1, text="Run", command=run_pso, width=10, height=1, font=("Arial"))
    run_button.grid(row=7, column=0, columnspan=2, pady=4)

    # FRAME 2
    label_output_title = tk.Label(frame2, text="Command Line Output", font=("Arial", 12))
    label_output_title.grid(row=0, column=0, padx=10, pady=5)

    def append_output(text):
        global cmd_output
        cmd_output += text + "\n"
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, text + "\n")
        output_box.config(state=tk.DISABLED)

    output_box = tk.Text(frame2, width=50, height=15)
    output_box.grid(row=1, column=0, padx=10, pady=10)
    output_box.config(state=tk.DISABLED)

    # FRAME 3
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

    # FRAME 4
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

    var.trace('w', lambda *args: show_optimal_route(frame4, var.get()))

    # Create a menu button called "About"
    about_menu = tk.Menu(menubar, tearoff=0)
    about_menu.add_command(label="About", command=about)

    # Add the "About" menu to the menu
    menubar.add_cascade(label="About", menu=about_menu)

    # Display the menu bar
    root.config(menu=menubar)

    # Run the main loop
    root.mainloop()