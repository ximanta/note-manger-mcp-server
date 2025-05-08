# Note Manager MCP Server for Claude Desktop

 MCP Server for a  note management application that integrates with Agents with MCP client integration - Tested with Claude Desktop, allowing you to manage notes during your conversations with Claude.

## Features

- View all notes for a user
- Add new notes with automatic date timestamps
- Delete notes by ID
- Search notes by keyword
- Search notes by date

## Installation

### Prerequisites

- Python 3.10 or higher
- Claude Desktop application

### Setup Steps

1. **Install uv** (Python package manager)
   ```bash
   pip install uv
   
   # On Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Create project directory**
   ```bash
   uv init note-manager-mcp-server
   cd note-manager-mcp-server
   ```

3. **Add MCP CLI**
   ```bash
   uv add "mcp[cli]"
   ```

4. **Create main.py**
   
   Create a `main.py` file in your project directory with the note management server code. (See the implementation details section for what to include)

5. **Install server in Claude Desktop**
   ```bash
   uv run mcp install main.py
   ```

6. **Restart Claude Desktop**
   - Close any running instance of Claude from Task Manager
   - Restart Claude Desktop
   - You should now see the note management tools available in Claude

## Implementation Details

The server provides the following tools to Claude:

- `get_notes(user_id)`: Fetch all notes for a user
- `add_note(user_id, note)`: Add a new note with current date
- `delete_note_by_id(user_id, note_id)`: Delete a specific note by ID
- `search_notes(user_id, keyword)`: Search notes for keywords
- `search_notes_by_date(user_id, date)`: Find notes by creation date

Data is stored in memory during the session.

## Usage

Once installed, you can interact with the note manager through Claude Desktop by asking:

- "Show me my notes"
- "Add a new note about [topic]"
- "Delete note with ID [note_id]"
- "Find notes about [keyword]"
- "Show notes from [date]"

Claude will use the appropriate tools to manage your notes.

## Note

This is a simple implementation with in-memory storage. Notes are NOT persisted between server restarts.