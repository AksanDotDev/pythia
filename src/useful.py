from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext import commands
from usefuls import useful_dict


class Useful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="Useful",
        aliases=["u"]
    )
    async def useful_com(self, ctx, *args: str):
        n = len(args)
        if n == 0:
            await ctx.send('\n'.join(useful_dict))
        elif n == 1:
            if args[0].lower() in useful_dict:
                await ctx.send(useful_dict[args[0].lower()])
            else:
                await ctx.send("I've nothing for that yet, sorry.")
        else:
            await ctx.send("Sorry, still learning, can't handle that yet.")
