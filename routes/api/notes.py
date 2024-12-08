from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import ValidationError
from utils.storage import get_all_notes_paginated,get_all_notes, get_note_by_id, add_note, update_note, delete_note
from utils.schemas import NoteCreateSchema, NoteUpdateSchema

notes_bp = Blueprint('notes', __name__)


@notes_bp.route('/api/notes', methods=['GET'])
@swag_from({
    'tags': ['Notes'],
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1,
            'description': 'Page number for pagination (default is 1).'
        },
        {
            'name': 'page_size',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': 'Number of notes per page (default is 10).'
        }
    ],
    'responses': {
        '200': {
            'description': 'Paginated list of notes.',
            'schema': {
                'type': 'object',
                'properties': {
                    'page': {'type': 'integer'},
                    'page_size': {'type': 'integer'},
                    'total_notes': {'type': 'integer'},
                    'total_pages': {'type': 'integer'},
                    'notes': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'title': {'type': 'string'},
                                'content': {'type': 'string'}
                            }
                        }
                    }
                }
            },
            'examples': {
                'application/json': {
                    'page': 1,
                    'page_size': 10,
                    'total_notes': 15,
                    'total_pages': 2,
                    'notes': [
                        {'id': 1, 'title': 'Note 1', 'content': 'Content of note 1'},
                        {'id': 2, 'title': 'Note 2', 'content': 'Content of note 2'}
                    ]
                }
            }
        },
        '400': {
            'description': 'Invalid pagination parameters.',
            'examples': {
                'application/json': {
                    'error': 'Page and page_size must be positive integers.'
                }
            }
        }
    }
})
def get_notes():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        if page < 1 or page_size < 1:
            return jsonify({'error': 'Page and page_size must be positive integers.'}), 400

        result = get_all_notes_paginated(page=page, page_size=page_size)
        return jsonify(result), 200

    except ValueError:
        return jsonify({'error': 'Invalid query parameters. Page and page_size must be integers.'}), 400


@notes_bp.route('/api/notes/<int:note_id>', methods=['GET'])
@swag_from({
    'tags': ['Notes'],
    'parameters': [
        {
            'name': 'note_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the note'
        }
    ],
    'responses': {
        '200': {
            'description': 'Note found',
            'examples': {
                'application/json': {'id': 1, 'title': 'Note 1', 'content': 'Content of note 1'}
            }
        },
        '404': {
            'description': 'Note not found'
        }
    }
})
def get_note(note_id):
    note = get_note_by_id(note_id)
    if note:
        return jsonify(note), 200
    return jsonify({'message': 'Note not found'}), 404


@notes_bp.route('/api/notes', methods=['POST'])
@swag_from({
    'tags': ['Notes'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'content': {'type': 'string'}
                },
                'required': ['title', 'content']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Note created',
            'examples': {
                'application/json': {'id': 1, 'title': 'New note', 'content': 'Content of the new note'}
            }
        },
        '400': {
            'description': 'Missing fields or invalid data'
        }
    }
})
def create_note():
    data = request.get_json()
    schema = NoteCreateSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    note = validated_data
    note['id'] = len(get_all_notes()) + 1
    add_note(note)
    return jsonify(note), 201


@notes_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
@swag_from({
    'tags': ['Notes'],
    'parameters': [
        {
            'name': 'note_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the note to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'content': {'type': 'string'}
                },
                'required': ['title', 'content']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Note updated',
            'examples': {
                'application/json': {'id': 1, 'title': 'Updated note', 'content': 'Updated content'}
            }
        },
        '404': {
            'description': 'Note not found'
        },
        '400': {
            'description': 'Invalid data'
        }
    }
})
def update_note_route(note_id):
    data = request.get_json()
    schema = NoteUpdateSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    note = get_note_by_id(note_id)
    if note:
        note.update(validated_data)
        update_note(note_id, note)
        return jsonify(note), 200

    return jsonify({'message': 'Note not found'}), 404


@notes_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Notes'],
    'parameters': [
        {
            'name': 'note_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the note to delete'
        }
    ],
    'responses': {
        '200': {
            'description': 'Note deleted'
        },
        '404': {
            'description': 'Note not found'
        }
    }
})
def delete_note_route(note_id):
    note = get_note_by_id(note_id)
    if note:
        delete_note(note_id)
        return jsonify({'message': 'Note deleted successfully'}), 200
    return jsonify({'message': 'Note not found'}), 404
