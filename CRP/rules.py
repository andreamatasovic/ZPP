from random import randint, random

def TLP(stacks):
    selected_containers = []
    min_position = float('inf')

    for stack in stacks:
        if stack:
            top_container = stack[-1]
            if top_container.position < min_position:
                min_position = top_container.position
                selected_containers = [top_container]
            elif top_container.position == min_position:
                selected_containers.append(top_container)

    if len(selected_containers) > 1:
        selected_container = random.choice(selected_containers)
    
    return selected_container

def RI(stacks):
    selected_container = None
    max_reshuffle_index = float('-inf')
    for stack in stacks:
        if stack:
            top_container = stack[-1]
            if top_container.reshuffle_index > max_reshuffle_index:
                max_reshuffle_index = top_container.reshuffle_index
                selected_container = top_container
    return selected_container

def RIL(stacks):
    selected_container = None
    min_lookahead_cost = float('inf')
    for stack in stacks:
        if stack:
            top_container = stack[-1]
            if top_container.lookahead_cost < min_lookahead_cost:
                min_lookahead_cost = top_container.lookahead_cost
                selected_container = top_container
    return selected_container
