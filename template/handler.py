from typing import Dict, Any

import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "vendor"))
from library import utils  # noqa: E402

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: Any, context: Any) -> Dict[str, Any]:
    return utils.respond_success(event)
