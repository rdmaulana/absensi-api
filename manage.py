import unittest
from app import app, db, models
from flask.cli import FlaskGroup

cli = FlaskGroup(app)

@cli.command("test")
def test():
    tests = unittest.TestLoader().discover('tests_old', pattern='old_test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    cli()