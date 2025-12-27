def send(sender, receiver, payload):
    print(f"\n📡 {sender} → {receiver.__class__.__name__}")
    receiver.receive(payload)
