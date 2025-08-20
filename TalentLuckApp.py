from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
from TalentLuck import LuckTalentModel, Person, NegativeEvent, PositiveEvent
import solara
from mesa.visualization.utils import update_counter
from matplotlib.figure import Figure

# portrayal of agents and events
def agent_portrayal(agent):

    if agent is None:
        return
    
    portrayal = {"size": 25}

    # agents as black crosses
    if isinstance(agent, Person):
        portrayal["color"] = "black"
        portrayal["marker"] = "x"
    # negative events as red circles
    elif isinstance(agent, NegativeEvent):
        portrayal["color"] = "red"
        portrayal["marker"] = "o"
    # positive events as green circles
    elif isinstance(agent, PositiveEvent):
        portrayal["color"] = "green"
        portrayal["marker"] = "o"
        
    return portrayal


# plotting wealth histogram
@solara.component
def Histogram(model):
    update_counter.get()  
    fig = Figure()
    ax = fig.subplots()
    agent_wealths = [agent.capital for agent in model.agents_by_type[Person]]
    ax.hist(agent_wealths, bins=100)
    ax.set_xlabel("Capital")
    ax.set_ylabel("Number of Agents")
    solara.FigureMatplotlib(fig)


# specifying model parameter sliders
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "height": Slider(label="Height of grid", value = 20, min = 5, max = 30, step = 1),
    "width": Slider("Width of grid", min = 5,value = 20, max = 30, step = 1),
    "n_events": Slider("Number of events", value = 20, min = 10, max = 100, step = 2),
    "prop_lucky": Slider("Proportion of Lucky Events", value = 0.5, min = 0.1, max = 0.9, step = 0.1),
    "n_actors": Slider("Number of People",value = 100, min = 10, max = 500, step = 1),
    "mean_talent": Slider("Mean Talent", value = 0.5, min = 0, max = 1, step = 0.1),
    "sd_talent": Slider("SD Talent", value = 0.1 , min = 0, max = 1, step = 0.1),
    "mean_start_capital": Slider("Mean Start Capital", value = 10, min = 1, max = 5000, step = 10),
    "sd_start_capital": Slider("SD Start Capital", value = 0 , min = 0, max = 1000, step = 50)
}

# function to remove axes
def post_process(ax):
    ax.set_xticks([])
    ax.set_yticks([])

# plot of the simulation
space_component = make_space_component(agent_portrayal, post_process= post_process)

# plotting Gini coefficient
GiniPlot = make_plot_component("Gini")


# creating the page with all components
page = SolaraViz(
    LuckTalentModel(),
    components=[space_component, GiniPlot, Histogram],
    model_params=model_params,
    name="Talent vs. Luck Model"
)