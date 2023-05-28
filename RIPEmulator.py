class RIPEmulator:
    def __init__(self, address, connections):
        self.address = address
        self.connections = set(connections)

        self.next = {connection: connection for connection in self.connections}
        self.metrics = {connection: 1 for connection in self.connections}
