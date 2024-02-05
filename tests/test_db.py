from blog.db import get_db
import pytest
import sqlite3

def test_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)





