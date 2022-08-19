import logging
import sys

from fastapi import Request
from loguru import logger as LG

logger = logging.getLogger('test')
LG.remove()
LG.add(sys.stdout, colorize=True,
           format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")


async def logging_dependency(request: Request):
    LG.debug(f"{request.method} {request.url}")
    LG.debug("Params:")
    for name, value in request.path_params.items():
        LG.debug(f"\t{name}: {value}")
    LG.debug("Headers:")
    for name, value in request.headers.items():
        LG.debug(f"\t{name}: {value}")
