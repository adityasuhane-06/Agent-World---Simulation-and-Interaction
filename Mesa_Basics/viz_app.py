
import mesa
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

class MyAgent(mesa.Agent):
    def __init__(self, model, energy):
        super().__init__(model)
        self.energy = energy
    
    def step(self):
        self.energy -= 1  # Energy kam hoti hai
        
        # Move to random neighbor
        neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_pos = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_pos)
        
        # Interact with others at same position
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if other != self and other.energy > 0:
                # Energy exchange
                self.energy += 5
                other.energy -= 5
                print(f"💥 Agent {self.unique_id} met Agent {other.unique_id} at {self.pos}")

class MyModel(mesa.Model):
    def __init__(self, n_agents=15, width=10, height=10, seed=None):
        super().__init__(seed=seed)
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        self.width = width
        self.height = height
        
        # Agents banao
        for _ in range(n_agents):
            agent = MyAgent(self, energy=self.random.randint(50, 100))
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(agent, (x, y))
            print(f"🟢 Agent {agent.unique_id} spawned at ({x}, {y}) with energy {agent.energy}")
    
    def step(self):
        self.agents.shuffle_do("step")

# 🎨 VISUALIZATION CODE
model = MyModel(n_agents=20, seed=42)

# Figure setup
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Agent Interaction Simulation', fontsize=16, fontweight='bold')

# Energy history track karne ke liye
energy_history = []
step_count = [0]

def update(frame):
    ax1.clear()
    ax2.clear()
    
    # LEFT PLOT - GRID
    ax1.set_xlim(-0.5, model.width - 0.5)
    ax1.set_ylim(-0.5, model.height - 0.5)
    ax1.set_aspect('equal')
    ax1.set_title(f'Agent Grid - Step {step_count[0]}', fontsize=14)
    ax1.set_xlabel('X Position')
    ax1.set_ylabel('Y Position')
    ax1.grid(True, alpha=0.3)
    
    # Grid lines
    for i in range(model.width + 1):
        ax1.axvline(i - 0.5, color='gray', linewidth=0.5, alpha=0.3)
    for i in range(model.height + 1):
        ax1.axhline(i - 0.5, color='gray', linewidth=0.5, alpha=0.3)
    
    # Plot agents
    for agent in model.agents:
        x, y = agent.pos
        
        # Energy ke basis pe color
        if agent.energy > 75:
            color = 'green'
        elif agent.energy > 50:
            color = 'yellow'
        elif agent.energy > 25:
            color = 'orange'
        else:
            color = 'red'
        
        # Agent draw karo
        ax1.scatter(x, y, c=color, s=300, alpha=0.8, edgecolors='black', linewidth=2)
        ax1.text(x, y, str(agent.unique_id), ha='center', va='center', 
                fontsize=8, fontweight='bold')
    
    # RIGHT PLOT - ENERGY GRAPH
    avg_energy = sum(a.energy for a in model.agents) / len(model.agents)
    energy_history.append(avg_energy)
    
    ax2.plot(energy_history, color='blue', linewidth=2, marker='o', markersize=4)
    ax2.set_title('Average Energy Over Time', fontsize=14)
    ax2.set_xlabel('Step')
    ax2.set_ylabel('Average Energy')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='Energy > 75'),
        Patch(facecolor='yellow', label='Energy 50-75'),
        Patch(facecolor='orange', label='Energy 25-50'),
        Patch(facecolor='red', label='Energy < 25')
    ]
    ax1.legend(handles=legend_elements, loc='upper right')
    
    # Model step
    model.step()
    step_count[0] += 1

# Animation
print("\n🚀 Starting visualization...\n")
ani = animation.FuncAnimation(
    fig, 
    update, 
    frames=200, 
    interval=500,  # 500ms = 0.5 second per step
    repeat=True
)

plt.tight_layout()
plt.show()