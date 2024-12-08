from math import ceil

notes_storage = []

def get_all_notes():
    return notes_storage

def get_all_notes_paginated(page=1, page_size=10):

    if page < 1 or page_size < 1:
        raise ValueError("Page and page_size must be positive integers.")

    total_notes = len(notes_storage)
    total_pages = ceil(total_notes / page_size)
    start = (page - 1) * page_size
    end = start + page_size
    notes = notes_storage[start:end]

    return {
        "page": page,
        "page_size": page_size,
        "total_notes": total_notes,
        "total_pages": total_pages,
        "notes": notes,
    }


def get_note_by_id(note_id):
    for note in notes_storage:
        if note['id'] == note_id:
            return note
    return None


def add_note(note):
    notes_storage.append(note)


def update_note(note_id, updated_note):
    for idx, note in enumerate(notes_storage):
        if note['id'] == note_id:
            notes_storage[idx].update(updated_note)
            return True
    return False


def delete_note(note_id):

    for idx, note in enumerate(notes_storage):
        if note['id'] == note_id:
            del notes_storage[idx]
            return True
    return False
