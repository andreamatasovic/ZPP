import json
from Container import Container

def parse_input(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    stacks = []
    for stack_data in data['stacks']:
        stack = []
        for container_data in stack_data:
            container = Container(container_data['id'], container_data['position'],
                                  container_data['reshuffle_index'], container_data.get('lookahead_cost', 0))
            stack.append(container)
        stacks.append(stack)
    return stacks
