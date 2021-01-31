from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext import commands
import socket
import struct
from memory import db_session, Host, Config


class Wake(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = db_session()

    @commands.command(
        name="Wake",
        aliases=["boot"]
    )
    async def wake_com(self, ctx, arg: str):
        if result := self.session.query(Host.mac_address).filter(
                    Host.hostname == arg
                ).one_or_none():
            mac_address = result.mac_address
            localhost = self.session.query(Config.config_val).filter(
                Config.config_key == "localhost"
            ).one_or_none()
            if localhost and localhost.config_val == arg:
                await ctx.send("They're already awake... I'm online.")
            elif result := self.session.query(Config.config_val).filter(
                        Config.config_key == "broadcast_ip"
                    ).one_or_none():
                await ctx.send(f"Waking {arg} on {mac_address}.")
                wake_on_lan(result.config_val, mac_address)
            else:
                await ctx.send(
                    "I don't know a `broadcast_ip`. Can't help you."
                )
        else:
            if result := self.session.query(Config.config_val).filter(
                    Config.config_key == "broadcast_ip"
                    ).one_or_none():
                await ctx.send(f"Waking device on {arg}.")
                wake_on_lan(result.config_val, arg)
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
