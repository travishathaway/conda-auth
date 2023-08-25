"""
A place to register plugin hooks
"""
from conda.plugins import CondaAuthHandler, CondaPreCommand, CondaSubcommand, hookimpl

from .handlers import OAuth2Handler, BasicAuthHandler, oauth2, basic_auth
from .constants import OAUTH2_NAME, HTTP_BASIC_AUTH_NAME
from .cli import login_wrapper, logout_wrapper


@hookimpl
def conda_subcommands():
    """
    Registers subcommands
    """
    yield CondaSubcommand(
        name="login", action=login_wrapper, summary="Login to a channel"
    )
    yield CondaSubcommand(
        name="logout", action=logout_wrapper, summary="Logout of a channel"
    )


@hookimpl
def conda_pre_commands():
    """
    Registers pre-command hooks
    """
    yield CondaPreCommand(
        name=f"{HTTP_BASIC_AUTH_NAME}-collect_credentials",
        action=basic_auth.get_action_func(),
        run_for={"search", "install", "update", "notices", "create", "search"},
    )
    yield CondaPreCommand(
        name=f"{OAUTH2_NAME}-collect_token",
        action=oauth2.get_action_func(),
        run_for={"search", "install", "update", "notices", "create", "search"},
    )


@hookimpl
def conda_auth_handlers():
    """
    Registers auth handlers
    """
    yield CondaAuthHandler(name=HTTP_BASIC_AUTH_NAME, handler=BasicAuthHandler)
    yield CondaAuthHandler(name=OAUTH2_NAME, handler=OAuth2Handler)
