class Container:
    def __init__(self, container_id, position, reshuffle_index, lookahead_cost=0):
        self.id = container_id
        self.position = position
        self.reshuffle_index = reshuffle_index
        self.lookahead_cost = lookahead_cost

    def __repr__(self):
        return f"Container(id={self.id}, position={self.position}, reshuffle_index={self.reshuffle_index}, lookahead_cost={self.lookahead_cost})"
