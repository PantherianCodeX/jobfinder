import yaml

# Load and print tasks.yaml for debugging
with open("src/jobfinder/config/tasks.yaml", "r") as file:
    tasks = yaml.safe_load(file)
    print(tasks)