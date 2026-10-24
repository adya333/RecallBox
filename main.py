from resource import Resource
from datetime import datetime
from storage import save_resources, load_resources
from pathlib import Path



resources = load_resources()

def add_file():
    file_path_input = input("Enter file path:")
    file_path = Path(file_path_input)

    if not file_path.exists():
        print("File does not exist.")
        return

    if not file_path.is_file():
        print("The given path is not a file.")
        return

    print("Path:", file_path)
    print("Name:", file_path.name)
    print("Extension:",file_path.suffix)

def add_text():
    title = input("Enter title: ")
    text = input("Enter your text: ")

    resource = Resource(
        resource_type="TEXT",
        title=title,
        raw_text=text,
        created_at = datetime.now(),
        embedding = None
    )

    resources.append(resource)
    save_resources(resources)

    print("Resource added successfully!")


def show_resources():
    if len(resources) == 0:
        print("RecallBox is empty.")
        return

    for resource in resources:
        print( resource.to_dict())

while True:

    print("\n--- RecallBox ---")
    print("1. Add text")
    print("2. Add file")
    print("3. Show resources")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_text()

    elif choice == "2":
        add_file()

    elif choice == "3":
        show_resources()

    elif choice == "4":
        break

    else:
        print("Invalid option")