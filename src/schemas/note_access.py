from pydantic import BaseModel
from src.models.note_access import Role



class AddRole(BaseModel):
    user_id: int
    role: Role = Role.VIEWER


class AddRoleDB(AddRole):
    note_id: int