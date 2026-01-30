import mesa

class MyAgent(mesa.Agent):
    def __init__(self, model, age):
        super().__init__(model)
        self.age = age
    
    def step(self):
        self.age += 1

class MyModel(mesa.Model):
    def __init__(self, n_agents, seed=None):  # seed parameter add karo
        super().__init__(seed=seed)  # seed pass karo
        
        for _ in range(n_agents):
            age = self.random.randint(0, 50)  # Ab ye kaam karega
            MyAgent(self, age)
    
    def step(self):
        self.agents.shuffle_do("step")

# Model chalaao
model = MyModel(n_agents=10, seed=42)  # seed optional hai
for i in range(10):
    model.step()
    avg_age = sum(a.age for a in model.agents) / len(model.agents)
    print(f"Step {i}: Average age = {avg_age:.1f}")