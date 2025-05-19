from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from typing import List, Dict
from datetime import datetime
import uuid

# In-memory store for notes: Dict[user_id, List[Dict[note_id, content, date]]]
user_notes: Dict[str, List[Dict[str, str]]] = {
    "U001": [
        {"note_id": "N001", "content": "Buy groceries", "date": "2025-05-01"},
        {"note_id": "N002", "content": "Meeting at 3PM", "date": "2025-05-02"}
    ],
    "U002": []
}

mcp = FastMCP("NoteManager")

# Utility to generate unique note IDs
def generate_note_id() -> str:
    return str(uuid.uuid4())[:8]  # short unique ID

# Tool: View all notes
@mcp.tool()
def get_notes(user_id: str) -> str:
    """Fetch all notes for a user"""
    notes = user_notes.get(user_id)
    if notes is not None:
        if notes:
            result = f"Notes for {user_id}:\n"
            for n in notes:
                result += f"- [{n['note_id']}] {n['content']} (added on {n['date']})\n"
            return result.strip()
        return "No notes found."
    return "User ID not found."

# Tool: Add a new note
@mcp.tool()
def add_note(user_id: str, note: str) -> str:
    """Add a note with current date and generated ID"""
    if user_id not in user_notes:
        return "User ID not found."
    
    today = datetime.now().strftime("%Y-%m-%d")
    note_id = generate_note_id()
    user_notes[user_id].append({"note_id": note_id, "content": note, "date": today})
    return f"Note added for {user_id} with ID {note_id} on {today}."

# Tool: Delete a note by note_id
@mcp.tool()
def delete_note_by_id(user_id: str, note_id: str) -> str:
    """Delete a specific note by its ID"""
    notes = user_notes.get(user_id)
    if notes is None:
        return "User ID not found."

    for n in notes:
        if n["note_id"] == note_id:
            notes.remove(n)
            return f"Note with ID {note_id} removed for {user_id}."
    return f"Note with ID {note_id} not found."

# Tool: Search notes by keyword
@mcp.tool()
def search_notes(user_id: str, keyword: str) -> str:
    """Search notes for a keyword"""
    notes = user_notes.get(user_id)
    if notes is None:
        return "User ID not found."

    matches = [n for n in notes if keyword.lower() in n["content"].lower()]
    if matches:
        result = f"Notes containing '{keyword}' for {user_id}:\n"
        for n in matches:
            result += f"- [{n['note_id']}] {n['content']} (added on {n['date']})\n"
        return result.strip()
    return f"No notes containing '{keyword}' found."

# Tool: Search notes by date
@mcp.tool()
def search_notes_by_date(user_id: str, date: str) -> str:
    """Search notes added on a specific date (YYYY-MM-DD)"""
    notes = user_notes.get(user_id)
    if notes is None:
        return "User ID not found."

    matches = [n for n in notes if n["date"] == date]
    if matches:
        result = f"Notes added on {date} for {user_id}:\n"
        for n in matches:
            result += f"- [{n['note_id']}] {n['content']}\n"
        return result.strip()
    return f"No notes found on {date}."

# Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}! How can I assist you with your notes today?"

@mcp.prompt()
def summarize_notes(user_id: str) -> list[base.Message]:
 
    return [
        base.SystemMessage("You are a concise note-summarizer."),
        base.UserMessage(f"You need to summarize the notes for {user_id}:"),
        base.AssistantMessage("Please give me a bullet-point summary and provide the date in literal form like Jan 01 2025.")
    ]
if __name__ == "__main__":
    mcp.run()
