from pathlib import Path
from typing import List
from core.connector import ConnectorType
from core.connectors.note import BaseNoteConnector, Note


class LocalMarkdownNotesConnector(BaseNoteConnector):
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def _note_path(self, note: Note) -> Path:
        return Path(self.root_dir, f"{note.title}.md")

    def get_notes(self, path: str, limit: int = 10) -> List[Note]:
        notes = []
        search_path = Path(self.root_dir, path)
        search_path.mkdir(parents=True, exist_ok=True)

        for file in search_path.glob("*.md"):
            if limit and len(notes) >= limit:
                break

            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                note = Note(
                    id=str(file.relative_to(self.root_dir)),
                    title=file.stem,
                    content=content
                )
                notes.append(note)

        return notes

    def create_note(self, note: Note):
        note_path = self._note_path(note)
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note.content)

    def update_note(self, note: Note):
        note_path = self._note_path(note)
        if not note_path.exists():
            raise FileNotFoundError("Note not found")

        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note.content)

    def delete_note(self, note: Note):
        note_path = self._note_path(note)
        if not note_path.exists():
            raise FileNotFoundError("Note not found")

        note_path.unlink()
