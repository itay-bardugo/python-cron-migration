__version__ = "0.0.1"

from cron_migration.cli.manager import CommandsManager
from cron_migration.cli.facade import OperationsFacade

# registering all commands here
import cron_migration.cli.operations.init
import cron_migration.cli.operations.make_revision

# end
from cron_migration.app.models.environment import Environment

environment = Environment()
