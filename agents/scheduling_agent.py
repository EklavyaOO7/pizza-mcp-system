class SchedulingAgent:

    def receive(self, payload):
        print(f"\n📅 Scheduling delivery")
        print(f"Order ID: {payload['order_id']}")
        print(f"ETA: {payload['eta']}")
        print("✅ Delivery scheduled")
