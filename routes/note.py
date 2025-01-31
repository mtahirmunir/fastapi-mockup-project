from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from config.db import conn  # Ensure this is correctly set up
from fastapi.staticfiles import StaticFiles

note = APIRouter()
templates = Jinja2Templates(directory="templates")

# Remove note.mount() from here. It should be in main.py

@note.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    docs = conn.notes.notes.find({})  
    newDocs = []
    
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),  # Convert ObjectId to string
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]
        })
    
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.post("/", response_class=JSONResponse)
async def create_note(request: Request):
    form = await request.form()  # Get form data directly

    # Create a cleaned dictionary matching MongoDB fields
    cleaned_data = {
        "title": form.get("title", ""),  # Changed "note" to "title"
        "desc": form.get("desc", ""),
        "important": form.get("important") == "on"  # Convert 'on' to True, else False
    }

    # Insert into MongoDB
    inserted_note = conn.notes.notes.insert_one(cleaned_data)

    return JSONResponse(content={"success": True, "note_id": str(inserted_note.inserted_id)})

