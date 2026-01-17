from .build import Build
from .deploy import Deploy
from .run_application import RunApplication
from .run_backend import RunBackend
from .try_camera_module import TryCameraModule
from .update_and_redeploy import UpdateAndRedeploy

COMMAND_OPTIONS = {
    "build": Build,
    "deploy": Deploy,
    "run_application": RunApplication,
    "run_backend": RunBackend,
    "try_camera_module": TryCameraModule,
    "update_and_redeploy": UpdateAndRedeploy
}


class CommandNotFoundError(Exception):
    pass


def get_command_names():
    """Returns a list with the names of the possible commands the system
    can use.
    """
    return list(COMMAND_OPTIONS.keys())


def get_instance_of_run_config_by_name(command_name, args, raw_args):
    if command_name not in get_command_names():
        raise CommandNotFoundError

    return COMMAND_OPTIONS[command_name](args, raw_args)
