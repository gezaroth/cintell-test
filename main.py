import random
from abc import ABC, abstractmethod

class Market:
    def __init__(self, initial_stock=100000, initial_price=200.0):
        self.stock = initial_stock
        self.price = initial_price

    def buy(self):
        if self.stock > 0:
            self.stock -= 1
            self.price *= 1.005

    def sell(self):
        self.stock += 1
        self.price *= 0.995 

class Agent(ABC):
    def __init__(self, balance=1000.0):
        self.balance = balance
        self.inventory = 0

    @abstractmethod
    def act(self, market):
        pass

class RandomAgent(Agent):
    def act(self, market):
        action = random.choice(['buy', 'sell', 'nothing'])
        if action == 'buy' and self.balance >= market.price:
            self.balance -= market.price
            self.inventory += 1
            market.buy()
        elif action == 'sell' and self.inventory > 0:
            self.balance += market.price
            self.inventory -= 1
            market.sell()

class TrendFollowingAgent(Agent):
    def act(self, market, previous_price):
        if market.price >= previous_price * 1.01:
            if random.random() < 0.75 and self.balance >= market.price:
                self.balance -= market.price
                self.inventory += 1
                market.buy()
        else:
            if random.random() < 0.2 and self.inventory > 0:
                self.balance += market.price
                self.inventory -= 1
                market.sell()

class AntiTrendAgent(Agent):
    def act(self, market, previous_price):
        if market.price <= previous_price * 0.99:
            if random.random() < 0.75 and self.balance >= market.price:
                self.balance -= market.price
                self.inventory += 1
                market.buy()
        else:
            if random.random() < 0.2 and self.inventory > 0:
                self.balance += market.price
                self.inventory -= 1
                market.sell()

class CustomAgent(Agent):
    def act(self, market, previous_price, iterations_left):
        if iterations_left > 50: 
            if market.price <= previous_price * 0.98 and self.balance >= market.price:
                self.balance -= market.price
                self.inventory += 1
                market.buy()
            elif self.inventory > 0 and market.price > previous_price * 1.02:
                self.balance += market.price
                self.inventory -= 1
                market.sell()
        else:
            if self.inventory > 0:
                self.balance += market.price
                self.inventory -= 1
                market.sell()

class Simulation:
    def __init__(self):
        self.market = Market()
        self.agents = self.create_agents()
        self.iterations = 1000

    def create_agents(self):
        agents = [RandomAgent() for _ in range(51)]
        agents += [TrendFollowingAgent() for _ in range(24)]
        agents += [AntiTrendAgent() for _ in range(24)]
        agents.append(CustomAgent())  # Nuestro agente personalizado
        return agents
    
    def run(self):
        previous_price = self.market.price
        for i in range(self.iterations):
            random.shuffle(self.agents)
            for agent in self.agents:
                if isinstance(agent, CustomAgent):
                    agent.act(self.market, previous_price, self.iterations - i)
                elif isinstance(agent, (TrendFollowingAgent, AntiTrendAgent)):
                    agent.act(self.market, previous_price)
                else:
                    agent.act(self.market)
            previous_price = self.market.price

if __name__ == "__main__":
    sim = Simulation()
    sim.run()

    total_balance = 0
    total_inventory = 0
    for i, agent in enumerate(sim.agents):
        print(f"Agent {i}: Balance=${agent.balance:.2f}, Inventory={agent.inventory} cards")
        total_balance += agent.balance
        total_inventory += agent.inventory

    print(f"\nMarket price: ${sim.market.price:.2f}")
    print(f"Total agent balance: ${total_balance:.2f}")
    print(f"Total agent inventory: {total_inventory} cards")
    print(f"Market stock: {sim.market.stock} cards")
