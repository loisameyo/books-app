import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db, models

""" A file to run database migrations and upgrades"""
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

manager = Manager (app)
migrate = Migrate (app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()