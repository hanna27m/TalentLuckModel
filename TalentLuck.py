from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random
import numpy as np


class Person(Agent):

    """
    class encodes humans that have given talent and build up capital over their lives 
    depending on the lucky and unlucky events they encounter throughout their lives

    params:
    model (mesa.model): model instance from which agents are called
    talent (float): value between 0 and 1 reflecting the talent of the person
    capital (int): starting value of capital
    """

    def __init__(self, model, talent, capital = 10):
      
        super().__init__(model)

        self.talent = talent
        self.capital = capital
        # count the number of lucky and unlucky events 
        self.num_lucky = 0
        self.num_unlucky = 0


    def live(self):

        # check cell and neighborhood for events
        pos_events = [event for event in self.model.grid.iter_neighbors(self.pos, moore = True, include_center = True) if isinstance(event, PositiveEvent)]
        neg_events = [event for event in self.model.grid.iter_neighbors(self.pos, moore = True, include_center = True) if isinstance(event, NegativeEvent)]

        # double capital with probability proportional to talent if positive event was encountered
        if pos_events:
            r = random.random()
            if r < self.talent:
                self.capital = 2 * self.capital
                # increase count of lucky events
                self.num_lucky += 1

        # halve capital if negative event was encountered
        if neg_events:
            self.capital = 0.5 * self.capital
            # increase count of unlucky events
            self.num_unlucky += 1



class PositiveEvent(Agent):

    """
    class encodes the positive / lucky events, after each time step, they randomly change location

    params:
    model (mesa.model): model instance from which agents are called

    """
    def __init__(self, model):
        super().__init__(model)

    def move(self):

        # move to random cell
        new_pos = random.choice(list(self.model.grid.coord_iter()))[1]
        self.model.grid.move_agent(self, new_pos)



class NegativeEvent(Agent):

    """
    class encodes the negative / unlucky events, after each time step, they randomly change location

    params:
    model (mesa.model): model instance from which agents are called
    
    """

    def __init__(self, model):
        super().__init__(model)

    def move(self):

        # move to random cell
        new_pos = random.choice(list(self.model.grid.coord_iter()))[1]
        self.model.grid.move_agent(self, new_pos)



class LuckTalentModel(Model):

    """
    Model Class of Luck vs. Talent Model

    params:
    height (int): Height of Grid
    width (int): Width of Grid
    n_actors (int): number of actors to be placed on grid
    n_events (int): number of events that move on grid
    prop_lucky (float): proportion of lucky events
    mean_talent (float): mean of normal distribution from which talent is sampled
    sd_talent (float): sd of normal distribution from which talent is sampled
    mean_start_capital (float): mean of start capital
    sd_start_capital (float): sd of start capital
    seed (int): random seed to make results reproducible
    """

    def __init__(self, 
                 height = 20,
                 width = 20, 
                 n_actors = 100,
                 n_events = 10,
                 prop_lucky = 0.5,
                 mean_talent = 0.5, 
                 sd_talent = 0.1,
                 mean_start_capital = 10,
                 sd_start_capital = 0,
                 seed = None):

        super().__init__(seed = seed)
        self.seed = seed
        self.height = height
        self.width = width
        self.n_actors = n_actors
        self.n_events = n_events
        self.prop_lucky = prop_lucky

        self.years_passed = 0

        # create grid with height and width
        self.grid = MultiGrid(width=self.width, height=self.height, torus = True)

        # create agents 
        for agent in range(n_actors):

            # sample talent from normal distribution with given mean and sd
            talent = np.random.normal(loc = mean_talent, scale = sd_talent)
            # sample capital from normal distribution with given mean and sd
            start_capital = np.random.normal(loc = mean_start_capital, scale= sd_start_capital)
            # choose location randomly
            coords = random.sample(list(self.grid.empties), 1)[0]

            agent = Person(self, talent, start_capital)
            self.grid.place_agent(agent, coords)


        # create events
        n_pos = int(prop_lucky * n_events)  # proportion of lucky events 
        n_neg = n_events - n_pos # rest is unlucky

        for pos_event in range(n_pos):

            # select random cell
            coords = random.choice(list(self.grid.coord_iter()))[1]
            event = PositiveEvent(self)
            # put event on grid
            self.grid.place_agent(event, coords)

        for neg_event in range(n_neg):

            # select random cell
            coords =  random.choice(list(self.grid.coord_iter()))[1]
            event = NegativeEvent(self)
            # put event on grid
            self.grid.place_agent(event, coords)


        # set up data collection
        self.datacollector = DataCollector(
            agent_reporters= {"Wealth": lambda a: getattr(a, "capital", None),
                              "Talent": lambda a: getattr(a, "talent", None),
                              "luckyEvents": lambda a: getattr(a, "num_lucky", None),
                              "unluckyEvents": lambda a: getattr(a, "num_unlucky", None)},
            model_reporters= {"Gini": self.compute_gini,
                              "Min / Max": self.min_and_max}
        )

        self.running = True
        self.datacollector.collect(self)


    def step(self):

        self.agents_by_type[Person].do("live")
        self.agents_by_type[NegativeEvent].do("move")
        self.agents_by_type[PositiveEvent].do("move")

        self.years_passed += 0.5

        self.datacollector.collect(self)
        
        # end model if 40 years have passed
        if self.years_passed >= 40:
            self.running = False


    def compute_gini(self):
        # Calculate the Gini coefficient for the model's current wealth distribution.
        
        agent_wealths = [agent.capital for agent in self.agents_by_type[Person]]
        x = sorted(agent_wealths)
        n = self.n_actors
        # Calculate using the standard formula for Gini coefficient
        b = sum(xi * (n - i) for i, xi in enumerate(x)) / (n * sum(x))
        return 1 + (1 / n) - 2 * b
    

    def min_and_max(self):
        # get the minimum and maximum capital 
        
        agent_wealths = [agent.capital for agent in self.agents_by_type[Person]]
        x = sorted(agent_wealths)
        n = self.n_actors
        min = x[0]
        max = x[n-1]
        return [min, max]
