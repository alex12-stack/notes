from src.repositories.folders import FoldersRepository
from src.repositories.users import UsersRepository
from src.repositories.note_access import Note_Access_Repository
from src.repositories.notes import NotesRepository




class DBManager:

    def __init__(self,session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.folders = FoldersRepository(self.session)
        self.users = UsersRepository(self.session)
        self.note_access = Note_Access_Repository(self.session)
        self.notes = NotesRepository(self.session)

        return self

    async def __aexit__(self,*args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()


