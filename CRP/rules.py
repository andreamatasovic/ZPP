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
    
def calculate_reshuffle_index(stack, blocking_container_id):
    reshuffle_index = 0
    for container in stack:
        if container.id < blocking_container_id:
            reshuffle_index += 1
    return reshuffle_index

def RI(stacks):
    min_reshuffle_index = float('inf')
    target_stack = None
    current_stack = None
    blocking_container_id = None
    min_container_id = float('inf')

    for stack in stacks:
        for container in stack:
            if container.id < min_container_id:
                min_container_id = container.id
                current_stack= stack
                blocking_container_id = current_stack[-1]
    for stack in stacks:         
            current_reshuffle_index = calculate_reshuffle_index(stack, blocking_container_id)
            if current_reshuffle_index < min_reshuffle_index:
                min_reshuffle_index = current_reshuffle_index
                target_stack = stack
    return target_stack


def min(stack):
    min_id = float('inf')
    for container in stack:
        if container.id < min_id:
            min_id = container.id
    return min_id     

def RIL(stacks):
    min_reshuffle_index = float('inf')
    target_stack = None
    current_stack = None
    blocking_container_id = None
    min_container_id = float('inf')
    min_max_id= float('-inf')
    for stack in stacks:
        for container in stack:
            if container.id < min_container_id:
                min_container_id = container.id
                current_stack= stack
                blocking_container_id = current_stack[-1]
    for stack in stacks:         
            current_reshuffle_index = calculate_reshuffle_index(stack, blocking_container_id)
            min_in_stack=min(stack)
            if current_reshuffle_index < min_reshuffle_index:
                min_reshuffle_index = current_reshuffle_index
                target_stack = stack
            elif current_reshuffle_index == min_reshuffle_index:
                if min_in_stack > min_max_id:
                    min_max_id = min_in_stack
                    min_reshuffle_index = current_reshuffle_index
                    target_stack = stack
           
    return target_stack
