
from pathlib import Path
from recall_resource import Resource
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, MatchAny


class QdrantService:

    def __init__(self):
        self.storage_path = Path("qdrant_data")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.collection_name = "recallbox"
        self.vector_size = 384

        self.client = QdrantClient(
            path=str(self.storage_path)
        )

        self.create_collection()

    def load_resources(self):
        resources = []
        offset = None

        while True:
            points, next_offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=True
            )

            for point in points:
                payload = point.payload

                resource = Resource(
                    resource_id=payload["resource_id"],
                    resource_type=payload["resource_type"],
                    title=payload["title"],
                    raw_text=payload["raw_text"],
                    created_at=datetime.fromisoformat(payload["created_at"]),
                    embedding=point.vector,
                    original_path=payload.get("original_path"),
                    category=payload.get("category"),
                    subcategory=payload.get("subcategory"),
                    tags=payload.get("tags", [])
                )

                resources.append(resource)

            if next_offset is None:
                break

            offset = next_offset

        return resources
    
    
    def build_filter(self, resource_type=None, category=None, tags=None):
      conditions = []

      if resource_type:
        conditions.append(FieldCondition(
          key = "resource_type",
          match=MatchValue(value=resource_type)
        ))
      if category:
        conditions.append(FieldCondition(
          key = "category",
          match = MatchValue(value=category)
        ))
      if tags:
        conditions.append(
          FieldCondition(
            key="tags",
            match=MatchAny(ans=tags)
          )
        )
      if not conditions:
        return None
      
      return Filter(must=conditions)



    def create_collection(self):

        if self.client.collection_exists(self.collection_name):
            print("RecallBox collection already exists.")
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE
            )
        )

        print("RecallBox collection created successfully.")

    
    
    def search(self, query_embedding, limit=10, resource_type=None, category=None, tags=None):
        
        query_filter = self.build_filter(
          resource_type=resource_type,
          category=category,
          tags=tags
        )
        
        response  = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=query_filter,
            limit=limit,
            with_payload=True
        )
        results = []
        for point in response.points:
          resource_id = point.payload.get("resource_id")

          if resource_id:
            results.append((resource_id, point.score))
        return results




    def upsert_resources(self, resources):

        points = []

        for resource in resources:

            if resource.embedding is None:
                continue

            point = PointStruct(
                id=resource.resource_id,
                vector=resource.embedding,
                payload={
                    "resource_id": resource.resource_id,
                    "title": resource.title,
                    "raw_text": resource.raw_text,
                    "resource_type": resource.resource_type,
                    "category": resource.category,
                    "subcategory": resource.subcategory,
                    "tags": resource.tags,
                    "created_at": resource.created_at.isoformat(),
                    "original_path": resource.original_path
                }
            )

            points.append(point)

        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

        print(f"Successfully migrated {len(points)} resources.")

    def close(self):
        self.client.close()
