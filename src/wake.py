from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext import commands
import socket
import struct
from memory import db_session
from memory_utilities import get_config, get_host_mac


class Wake(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = db_session()

    @commands.command(
        name="Wake",
        aliases=["boot"]
    )
    async def wake_com(self, ctx, arg: str):
        if mac_address := get_host_mac(self.session, arg):
            if get_config(self.session, "localhost") == arg:
                await ctx.send("They're already awake... I'm online.")
            elif b_ip := get_config(self.session, "broadcast_ip"):
                await ctx.send(f"Waking {arg} on {mac_address}.")
                wake_on_lan(b_ip, mac_address)
            else:
                await ctx.send(
                    "I don't know a `broadcast_ip`. Can't help you."
                )
        else:
            if b_ip := get_config(self.session, "broadcast_ip"):
                await ctx.send(f"Waking device on {arg}.")
                wake_on_lan(b_ip, arg)
            else:
                await ctx.send(
                    "I don't know a `broadcast_ip`. Can't help you."
                )


def wake_on_lan(target_ip, target_mac):
    macaddress = target_mac.replace(':', '')
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = b''

    for i in range(0, len(data), 2):
        send_data = b''.join(
            [send_data, struct.pack('B', int(data[i: i + 2], 16))]
        )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (target_ip, 7))
