
from recall_resource import Resource
from datetime import datetime
from pathlib import Path

from embedding_service import EmbeddingService
from search_service import SearchService
from lexical_search_service import LexicalSearchService
from hybrid_search_service import HybridSearchService
from reranking_service import RerankingService
from qdrant_service import QdrantService


# Initialize services
embedding_service = EmbeddingService()

qdrant_service = QdrantService()

# Load all existing resources directly from Qdrant
resources = qdrant_service.load_resources()

print(f"Loaded {len(resources)} resources from Qdrant.")


# Initialize search services
search_service = SearchService(
    embedding_service,
    resources,
    qdrant_service
)

lexical_search_service = LexicalSearchService(resources)

reranking_service = RerankingService()

hybrid_search_service = HybridSearchService(
    search_service,
    lexical_search_service,
    reranking_service
)


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
    print("Extension:", file_path.suffix)


def add_text():
    title = input("Enter title: ")
    text = input("Enter your text: ")

    resource = Resource(
        resource_type="TEXT",
        title=title,
        raw_text=text,
        created_at=datetime.now(),
        embedding=embedding_service.generate_embedding(text)
    )

    # Save directly to Qdrant
    qdrant_service.upsert_resources([resource])

    # Update in-memory resources for BM25 and other search services
    resources.append(resource)

    print("Resource added successfully!")


def show_resources():
    if not resources:
        print("RecallBox is empty.")
        return

    for resource in resources:
        print(f"Title: {resource.title}")
        print(f"ID: {resource.resource_id}")
        print("-" * 40)


def search():
    query = input("Enter search query: ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    if not resources:
        print("RecallBox is empty. Add something before searching.")
        return

    results = hybrid_search_service.search_with_reranking(query)

    if not results:
        print("No relevant results found.")
        return

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
        qdrant_service.close()
        print("Qdrant connection closed.")
        break

    else:
        print("Invalid option")
