from agents.ordering_agent import OrderingAgent
from agents.scheduling_agent import SchedulingAgent

scheduler = SchedulingAgent()
ordering = OrderingAgent(scheduler)

ordering.handle("Please order a large Margherita pizza")
