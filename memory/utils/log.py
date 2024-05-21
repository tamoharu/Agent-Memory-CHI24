import os
from logging import basicConfig, getLogger, Logger, DEBUG, INFO, WARNING, ERROR, CRITICAL


class Log:
    def __init__(self, log_level, log_path, enable=True) -> None:
        # log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../assets/{log_path}'))
        basicConfig(format='%(message)s')
        self.enable() if enable else self.disable()
        self.get_package_logger().setLevel(self.get_log_levels()[log_level])
        self.disable_non_root_loggers()

    def get_package_logger(self) -> Logger:
        return getLogger()

    def debug(self, message: str) -> None:
        self.get_package_logger().debug(message + '\n')

    def info(self, message: str) -> None:
        self.get_package_logger().info(message + '\n')

    def warn(self, message: str) -> None:
        self.get_package_logger().warning(message + '\n')

    def error(self, message: str) -> None:
        self.get_package_logger().error(message + '\n')

    def enable(self) -> None:
        self.get_package_logger().disabled = False

    def disable(self) -> None:
        self.get_package_logger().disabled = True

    def disable_non_root_loggers(self) -> None:
        logger_dict = getLogger().manager.loggerDict
        for _, logger_instance in logger_dict.items():
            if isinstance(logger_instance, Logger):
                logger_instance.setLevel(CRITICAL + 10)

    def get_log_levels(self) -> dict:
        return\
        {
            'error': ERROR,
            'warn': WARNING,
            'info': INFO,
            'debug': DEBUG
        }