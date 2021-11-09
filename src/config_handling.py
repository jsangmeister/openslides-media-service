import os
import sys


def get_type_for(config_value):
    if config_value in (
        "MEDIA_DATABASE_PORT",
        "MEDIA_BLOCK_SIZE",
        "PRESENTER_PORT",
    ):
        return int
    return str


def get_default_for(config_value):
    if config_value == "MEDIA_BLOCK_SIZE":
        return 4096


def init_config(app):
    file_configs = (
        "MEDIA_DATABASE_USER",
        "MEDIA_DATABASE_PASSWORD",
    )

    all_configs = (
        "MEDIA_DATABASE_HOST",
        "MEDIA_DATABASE_PORT",
        "MEDIA_DATABASE_NAME",
        "MEDIA_DATABASE_USER",
        "MEDIA_DATABASE_PASSWORD",
        "MEDIA_BLOCK_SIZE",
        "PRESENTER_HOST",
        "PRESENTER_PORT",
    )

    for config in all_configs:
        if config in file_configs:
            value = get_config_from(app, config + "_FILE")
        else:
            value = os.environ.get(config, get_default_for(config))
        if not value:
            continue
        try:
            value = get_type_for(config)(value)
        except Exception:  # noqa
            app.logger.critical(
                f"Environment variable for '{config}' does not have the "
                f"type {str(get_type_for(config))}"
            )
            sys.exit(1)
        app.config[config] = value

    for config in all_configs:
        if app.config.get(config) is None:
            app.logger.critical(f"Did not find an environment variable for '{config}'")
            sys.exit(1)


def get_config_from(app, config):
    path = os.environ.get(config)
    if not path:
        app.logger.critical(f"Did not find environment variable for '{config}'")
        sys.exit(1)
    try:
        with open(path) as file_:
            return file_.read()
    except Exception:  # noqa
        app.logger.critical(f"Reading path '{path}' from config '{config}' went wrong.")
        sys.exit(1)
