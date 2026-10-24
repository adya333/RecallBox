from datetime import datetime
import uuid

class Resource:
    def __init__(self, resource_type, title, raw_text, created_at, embedding, resource_id=None):
        if resource_id is None:
            self.resource_id = str(uuid.uuid4())
        else:
            self.resource_id = resource_id
        self.type = resource_type
        self.title = title
        self.raw_text = raw_text

        self.original_path = None

        self.category = None
        self.subcategory = None
        self.tags = []
        self.created_at = created_at
        self.embedding = embedding

    def to_dict(self):
        return {
            "resource_id": self.resource_id,
        "type": self.type,
        "title": self.title,
        "original_path": self.original_path,
        "raw_text": self.raw_text,
        "category": self.category,
        "subcategory": self.subcategory,
        "tags": self.tags,
        "created_at": self.created_at.isoformat(),
        "embedding": self.embedding
        } 

    def load_resources():
        with open("resources.json", "r") as file:
            data = json.load(file)   
        print(data)

    @classmethod
    # This is a decorator in python that is is used to define a method 
    # that is bound to the class itself rather than an individual object
    #  instance. The cls represents the class itself.
    def to_obj(cls,data):
        resource = cls(resource_id=data["resource_id"],
        resource_type=data["type"],
        title=data["title"],
        raw_text=data["raw_text"],
        created_at =  datetime.fromisoformat(data["created_at"]),
        embedding = data["embedding"])

        return resource
