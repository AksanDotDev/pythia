from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext import commands
import socket
import struct
from config import config


class Wake(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="Wake",
        aliases=["w"]
    )
    async def wake_com(self, ctx, arg: str):
        if arg.capitalize() in config.hosts:
            arg = arg.capitalize()
            mac = config.hosts[arg].MAC
            self.wake_on_lan(mac)
            await ctx.send(f"Waking {arg} on {mac}.")
        else:
            self.wake_on_lan(arg)
            await ctx.send(f"Waking device on {arg}.")

    def wake_on_lan(self, target_address):
        macaddress = target_address.replace(target_address[2], '')
        data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
        send_data = b''

        for i in range(0, len(data), 2):
            send_data = b''.join(
                [send_data, struct.pack('B', int(data[i: i + 2], 16))]
            )

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, (config.network.broadcast, 7))
