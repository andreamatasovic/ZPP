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
    
def calculate_reshuffle_index(stack):
    if not stack:
        return
    for i in range(len(stack)):
        stack[i].reshuffle_index = len(stack) - 1 - i 

def calculate_lookahead_cost(stacks, container, target_stack):
    simulated_stacks = [stack.copy() for stack in stacks]
    current_stack = next(stack for stack in stacks if container in stack)
    current_stack.remove(container)
    target_stack.append(container)
    additional_cost = 0
    for stack in simulated_stacks:
        if stack:
            top_container = stack[-1]
        if top_container.position == container.position:
                additional_cost += 1  

    return additional_cost

def RI(stacks):
    selected_container = None
    max_reshuffle_index = float('-inf')
    for stack in stacks:
        calculate_reshuffle_index(stack)  
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
            lookahead_cost = calculate_lookahead_cost(stacks, top_container, [])
            top_container.lookahead_cost = lookahead_cost
            if lookahead_cost < min_lookahead_cost:
                min_lookahead_cost = lookahead_cost
                selected_container = top_container
    
    return selected_container

