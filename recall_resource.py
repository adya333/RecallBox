
from datetime import datetime
import uuid


class Resource:

    def __init__(
        self,
        resource_type,
        title,
        raw_text,
        created_at=None,
        embedding=None,
        original_path=None,
        category=None,
        subcategory=None,
        tags=None,
        resource_id=None
    ):

        self.resource_id = resource_id or str(uuid.uuid4())

        self.resource_type = resource_type
        self.title = title
        self.raw_text = raw_text

        self.original_path = original_path

        self.category = category
        self.subcategory = subcategory
        self.tags = tags if tags is not None else []

        self.created_at = created_at or datetime.now()
        self.embedding = embedding

    def to_dict(self):

        return {
            "resource_id": self.resource_id,
            "type": self.resource_type,
            "title": self.title,
            "raw_text": self.raw_text,
            "original_path": self.original_path,
            "category": self.category,
            "subcategory": self.subcategory,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "embedding": self.embedding
        }

    @classmethod
    def to_obj(cls, data):

        return cls(
            resource_id=data["resource_id"],
            resource_type=data.get("resource_type", data.get("type")),
            title=data["title"],
            raw_text=data["raw_text"],
            original_path=data.get("original_path"),
            category=data.get("category"),
            subcategory=data.get("subcategory"),
            tags=data.get("tags"),
            created_at=datetime.fromisoformat(data["created_at"])
                if data.get("created_at") else None,
            embedding=data.get("embedding")
        )
