from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from src.api.folders import router as router_folders
# from src.api.note_access import router as router_note_access
from src.api.notes import router as router_notes
# from src.api.users import router as router_user

app = FastAPI(docs_url=None)

app.include_router(router_folders)
# app.include_router(router_note_access)
app.include_router(router_notes)
# app.include_router(router_user)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)