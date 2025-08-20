## About the Project

This project is based on the paper "Talent vs. Luck: The role of randomness in success and failure" by Pluchino et al. (2018) (https://doi.org/10.1142/S0219525918500145). 
The file TalentLuck.py is an implementation of their agent-based model that they describe in their paper. 
The model simulates the evolution of wealth over a period of 40 years with time steps equal to 6 months. Agents with a fixed talent increase or decrease their capital if they 
experience lucky or unlucky events. The simulation leads to an unequal distribution of wealth resembling real-world wealth distributions. 
A full description of the model along with an analysis of the simulation results can be found in the report (Report_TalentLuckModel.pdf).

## Installation 

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
   
   ```sh
   pip install -r requirements.txt
   ```

## How to Use

* TalentLuck.py contains the implementation of the model using the Mesa framework.

* The accompanying Jupyter Notebook imports the model, runs simulations, and analyzes the results.

* Simulation data is stored in the data folder.

* TalentLuckApp.py provides an interactive visualization of the simulation. To run it, execute:
  
  ```sh
  solara run TalentLuckApp.py
  ```

  This should open a browser window in which the simulation can be started and each step is visualized.
