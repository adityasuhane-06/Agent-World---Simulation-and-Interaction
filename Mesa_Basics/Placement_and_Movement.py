import mesa 
# this is my actor
class MyAgent(mesa.Agent):
    def __init__(self, model,age):
        super().__init__(model)
        self.age = age
    def step(self):
        self.age+=1
        print(f"Agent {self.unique_id} now is {self.age} years old")
        neighbors=self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
        new_pos=self.random.choice(neighbors)
        self.model.grid.move_agent(self,new_pos)
        print(f"Agent {self.unique_id} moved to {new_pos}")

# Model Class ye mera simulation ha 

class MyModel(mesa.Model):
    def __init__(self,n_agents,seed=None):
        super().__init__(seed=seed)
        self.grid=mesa.space.MultiGrid(10,10,torus=True)
        for _ in range(n_agents):
            age=self.random.randint(0,50)
            agent=MyAgent(self,age)
            x=self.random.randrange(0,10)
            y=self.random.randrange(0,10)
            self.grid.place_agent(agent,(x,y))
            print(f"Agent {agent.unique_id} is at {x},{y}")
    
    def step(self):
        self.agents.shuffle_do("step")

model = MyModel(n_agents=10, seed=43)
print("\n-----Simulation Start-----\n")
for i in range(4):
    print(f"\n==== Step{i}====")
    model.step()