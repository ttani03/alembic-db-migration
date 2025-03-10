import importlib.util
import os
import sys
from logging.config import fileConfig
from os.path import basename, dirname, join, splitext

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

import database

models_dir = join(dirname(__file__), '../../models')  # Adjust the relative path as needed
model_files = [f for f in os.listdir(models_dir) if f.endswith('.py') and f != '__init__.py']
imported_models = []

for model_file in model_files:
    module_name = splitext(model_file)[0]
    module_path = join(models_dir, model_file)
    spec = importlib.util.spec_from_file_location(f'models.{module_name}', module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f'models.{module_name}'] = module
    spec.loader.exec_module(module)
    imported_models.append(module_name)

model_name = [splitext(basename(f))[0] for f in model_files]
missing_models = [model for model in model_name if model not in imported_models]

if missing_models:
    print(f"Missing model imports: {', '.join(missing_models)}", file=sys.stderr)
    sys.exit(1)

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
user_name = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
host = os.environ.get('MYSQL_HOST')
database_name = os.environ.get('MYSQL_DATABASE')

DATABASE = f'mysql+mysqlconnector://{user_name}:{password}@{host}/{database_name}?charset=utf8'

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option("sqlalchemy.url", DATABASE)
target_metadata = database.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
