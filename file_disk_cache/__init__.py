import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

from file_disk_cache.config.logging import configure_logger
configure_logger()