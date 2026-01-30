import mesa 
import numpy as np

# Agent with energy and interaction
class MyAgent(mesa.Agent):
    def __init__(self, model, age, energy):
        super().__init__(model)
        self.age = age
        self.energy = energy  # Naya property
    
    def step(self):
        self.age += 1
        
        # Move to random neighbor
        neighbors_pos = self.model.grid.get_neighborhood(
            self.pos, 
            moore=True, 
            include_center=False
        )
        new_pos = self.random.choice(neighbors_pos)
        self.model.grid.move_agent(self, new_pos)
        
        # 🤝 INTERACTION: Check if other agents are at same position
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        
        if len(cellmates) > 1:  # Agar aur bhi agents hain same cell mein
            for other in cellmates:
                if other != self:  # Khud ko chhod kar
                    # Energy exchange karo
                    energy_transfer = 5
                    self.energy += energy_transfer
                    other.energy -= energy_transfer
                    print(f"💥 Agent {self.unique_id} met Agent {other.unique_id} at {self.pos}")
                    print(f"   Energy: Agent {self.unique_id}={self.energy}, Agent {other.unique_id}={other.energy}")

# Model Class
class MyModel(mesa.Model):
    def __init__(self, n_agents, seed=None):
        super().__init__(seed=seed)
        self.grid = mesa.space.MultiGrid(10, 10, torus=True)
        
        # Data collector add karo
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Average Energy": lambda m: m.agents.agg("energy", np.mean),
                "Average Age": lambda m: m.agents.agg("age", np.mean)
            },
            agent_reporters={
                "Age": "age",
                "Energy": "energy"
            }
        )
        
        for _ in range(n_agents):
            age = self.random.randint(0, 50)
            energy = self.random.randint(50, 100)  # Initial energy
            agent = MyAgent(self, age, energy)
            x = self.random.randrange(0, 10)
            y = self.random.randrange(0, 10)
            self.grid.place_agent(agent, (x, y))
            print(f"🟢 Agent {agent.unique_id} spawned at ({x}, {y}) with energy {energy}")
    
    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)  # Data collect karo

# Test run
model = MyModel(n_agents=5, seed=43)
print("\n🚀 -----Simulation Start-----\n")
for i in range(3):
    print(f"\n{'='*50}")
    print(f"⏰ Step {i}")
    print('='*50)
    model.step()

# Data dekho
print("\n📊 Model Data:")
print(model.datacollector.get_model_vars_dataframe())