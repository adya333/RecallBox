from re import search
from recall_resource import Resource
from datetime import datetime
from storage import save_resources, load_resources, backfill_embeddings
from pathlib import Path
from embedding_service import EmbeddingService
from search_service import SearchService
from lexical_search_service import LexicalSearchService
from hybrid_search_service import HybridSearchService

embedding_service = EmbeddingService()
resources = load_resources()
search_service = SearchService(embedding_service, resources)
lexical_search_service = LexicalSearchService(resources)
hybrid_search_service = HybridSearchService(search_service, lexical_search_service)

# Backfill function to add embeddings into the already existing resources
# which currently dont have any embeddings
# updated_count = backfill_embeddings(resources, embedding_service)
# for resource in resources:
#     print(
#         resource.title,
#         "->",
#         "Embedding exists" if resource.embedding is not None else "Embedding missing"
#     )

# if(updated_count>0):
#   save_resources(resources)
#   print(f"Backfilled embeddings: {updated_count}")

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
        embedding = embedding_service.generate_embedding(text)
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

def search():
    query = input("Enter search query:").strip()

    if not query:
      print("Search query cannot be empty.")
      return
    
    if not resources:
      print("Recall Box is empty. Add something before searching..")

    results = hybrid_search_service.search(query)
   

  

    

   

    if not results:
      print("No relevant results found.")
    
    for resource, score in results:
      print(f"Title: {resource.title}")
      print(f"Text: {resource.raw_text}")
      print(f"Relevance Score: {score:.4f}")


while True:

    print("\n--- RecallBox ---")
    print("1. Add text")
    print("2. Add file")
    print("3. Show resources")
    print("4. Search")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_text()

    elif choice == "2":
        add_file()

    elif choice == "3":
        show_resources()

    elif choice == "4":
        search()
    elif choice == "5":
        break

    else:
        print("Invalid option")