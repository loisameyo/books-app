from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db, models

""" A file to run database migrations and upgrades"""
manager = Manager (app)
migrate = Migrate (app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()