import json
from resource import Resource

def save_resources(resources):
    resource_dict = []

    for r in resources:
        resource_dict.append(r.to_dict())

    with open("resources.json","w") as file:
        json.dump(resource_dict, file, indent=4)


def load_resources():
    with open("resources.json", "r") as file:
        data = json.load(file)

    resources = []

    for item in data:
        resource = Resource.to_obj(item)
        resources.append(resource)

    return resources
    