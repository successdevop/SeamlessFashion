from pydantic import BaseModel, ConfigDict


class ORMBaseSchema(BaseModel):
    """Base schema for API models that can be populated from ORM objects."""
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )