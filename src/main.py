from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from src.api.folders import router as router_folders
from src.api.note_access import router as router_note_access
from src.api.notes import router as router_notes
from src.api.users import router as router_user

app = FastAPI()

app.include_router(router_folders)
app.include_router(router_note_access)
app.include_router(router_notes)
app.include_router(router_user)


if __name__ == "main":
    uvicorn.run("main:app",reload=True)