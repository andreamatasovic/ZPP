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
        current_container = stack[i]
        count_higher_priority = sum(1 for container in stack if container.priority < current_container.priority)
        current_container.reshuffle_index = count_higher_priority



def lookahead_cost(stack, container, target_stack):
    simulated_stack = stack.copy()
    simulated_stack.remove(container)
    target_stack.append(container)

    max_priority = float('-inf')
    for cont in simulated_stack:
        if cont.priority > max_priority:
            max_priority = cont.priority
    
    return max_priority    


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
    max_reshuffle_index = float('-inf')
    candidate_stacks = []

    for stack in stacks:
        calculate_reshuffle_index(stack)
    
    for stack in stacks:
        if stack:
            top_container = stack[-1]
            if top_container.reshuffle_index > max_reshuffle_index:
                max_reshuffle_index = top_container.reshuffle_index
                candidate_stacks = [stack]
            elif top_container.reshuffle_index == max_reshuffle_index:
                candidate_stacks.append(stack)
 
    if len(candidate_stacks) > 1:
        min_max_priority = float('inf')
        for stack in candidate_stacks:
            top_container = stack[-1]
            cost = lookahead_cost(stack, top_container, [])
            if cost < min_max_priority:
                min_max_priority = cost
                selected_container = top_container
    else:
        selected_container = candidate_stacks[0][-1]
    
    return selected_container
