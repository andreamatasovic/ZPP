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
    
def calculate_reshuffle_index(stack, target_container_id):
    reshuffle_index = 0
    for container in stack:
        if container.id < target_container_id:
            reshuffle_index += 1
    return reshuffle_index

def RI(stacks):
    selected_container = None
    max_reshuffle_index = float('-inf')
    
    for stack in stacks:
        if stack:
            top_container = stack[-1] 
            top_container.reshuffle_index = calculate_reshuffle_index(stack, top_container.id)
            
            if top_container.reshuffle_index > max_reshuffle_index:
                max_reshuffle_index = top_container.reshuffle_index
                selected_container = top_container
                
    return selected_container

def lookahead_cost(original_stack, container, target_stack):

    simulated_original_stack = original_stack.copy()
    simulated_original_stack.remove(container)
    simulated_target_stack = target_stack.copy()
    simulated_target_stack.append(container)

    max_reshuffle_index_original = float('-inf')
    for cont in simulated_original_stack:
        reshuffle_index = calculate_reshuffle_index(simulated_original_stack, cont.id)
        if reshuffle_index > max_reshuffle_index_original:
            max_reshuffle_index_original = reshuffle_index

    max_reshuffle_index_target = float('-inf')
    for cont in simulated_target_stack:
        reshuffle_index = calculate_reshuffle_index(simulated_target_stack, cont.id)
        if reshuffle_index > max_reshuffle_index_target:
            max_reshuffle_index_target = reshuffle_index

    return max(max_reshuffle_index_original, max_reshuffle_index_target)

def RIL(stacks):
    selected_container = None
    max_reshuffle_index = float('-inf')
    candidate_stacks = []

    for stack in stacks:
        if stack:
            calculate_reshuffle_index(stack, stack[-1].id)
    
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
