### Particle Swarm Optimisation teaching tool
The tool is designed to solve the Travelling Salesmen Problem

Follow the steps to install and run the tool:
1. Download Anaconda on your device
2. Clone the repository on your device:
   2.1 Open Git Bash
   2.1 Change the current working directory to the location where you want to copy the project
   2.2 Use `git clone https://github.com/aszwalek1/PSO-tool.git` to clone the project
3. Open Anaconda Prompt and run `conda env update -f environment_COM3524.yml`
4. In the same Anaconda Prompt run `conda activate environment_COM3524`
5. Navigate to the location of the project
6. Run `python TSP_Solver.py` to start the tool

## How to use the tool
The tool is divided into 4 parts.
In top-left square you can see the default settings for running the PSO algorithm. You can change the number of cities (difficulty), 
number of iterations, number of particles (population size) and the parameters influencing the algorithm (inertia weight, social coefficient and cognitive coefficient)

When you change the difficulty of the problem, the optimal solution to that problem will be shown in the bottom-right square. 

After you run the algorithm you will be able to see the command line output in the top-right square and the visual representation of the current solution in the bottom-left square.

