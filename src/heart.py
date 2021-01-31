from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext import commands
from wake import Wake
from memory import Memory, Configuration, init_db
import time

cogs = [Wake, Memory, Configuration]


Pythia = commands.Bot(
    command_prefix=commands.when_mentioned,
    case_insensitive=True
    )


@Pythia.command(name="Marco")
async def marco_polo(ctx):
    await ctx.send("Polo!")


Pythia.remove_command("help")


@Pythia.command(
    name="Help"
)
async def false_help(ctx):
    if "_last_call" not in false_help.__dict__:
        false_help._last_call = 0
    this_call = time.monotonic()
    if (this_call - false_help._last_call) < 60:
        await ctx.send("***HELP!!!***")
    else:
        await ctx.send("Do you mean actual help?")
    false_help._last_call = this_call


@Pythia.command(
    name="Actual",
    aliases=["Real", "R"],
    hidden=True
)
async def actual(ctx, arg: str):
    if arg == "help":
        await ctx.send_help()

if __name__ == "__main__":
    init_db()
    for cog in cogs:
        Pythia.add_cog(cog(Pythia))

    with open("/__env__/bot.key") as key:
        token = key.read()

    Pythia.run(token, bot=True, reconnect=True)
