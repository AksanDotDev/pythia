from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


async def pagified_send(target, msg, code_block=False):
    lines = msg.split('\n')
    message = "```" if code_block else ""
    for line in lines:
        with target.typing():
            if len(message) + len(line) + 4 >= 2000:
                await target.send(message + ("```" if code_block else ""))
                message = "```" if code_block else ""
            message += "\n" + line
    if message:
        await target.send(message + ("```" if code_block else ""))
