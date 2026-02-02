def serialize_product_from_dict(data: dict) -> dict:
    return {
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "image": data.get("image", ""),
        "category": data.get("category"),
        "tags": data.get("tags", []),
        "featured": data.get("featured", False),
        "volumes": data.get("volumes", []),
        "notes": data.get("notes"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
