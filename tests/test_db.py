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

def test_init_db_command(runner, monkeypatch):
    class Recoder(object): 
        called = False
    
    def fake_init_db():
        Recoder.called = True
    
    monkeypatch.setattr('blog.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])

    assert 'Initialised' in result.output
    assert Recoder.called



