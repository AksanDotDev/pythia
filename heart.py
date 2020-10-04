from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext import commands
from config import config
from cogical import Cogical

Pythia = commands.Bot(command_prefix=commands.when_mentioned)


@Pythia.command(name="Marco")
async def marco_polo(ctx):
    await ctx.send("Polo!")

Pythia.add_cog(Cogical(Pythia))

Pythia.run(config.discord.token, bot=True, reconnect=True)
