from src.repositories.base import BaseRepository
from src.models.note_access import NoteAccessOrm


class UserRepository(BaseRepository):
    model = NoteAccessOrm


