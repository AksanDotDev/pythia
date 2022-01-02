from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext.commands import Bot, when_mentioned
from wake import Wake
from teryte import Teryte
from memory import Memory, Configuration, init_db, db_session
from memory_utilities import get_config
import time

cogs = [Wake, Teryte, Memory, Configuration]


Pythia = Bot(
    command_prefix=when_mentioned,
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


@Pythia.group(
    name="Actual",
    case_insensitive=True,
    invoke_without_command=True,
    pass_context=True,
    hidden=True
)
async def actual(ctx):
    name = get_config(db_session(), "true_name")
    if Pythia.user.name == name:
        await ctx.send(f"I am {name} actual.")
    else:
        await ctx.send("I am not really feeling myself.")


@actual.command(
    name="Help"
)
async def real_help(ctx):
    await ctx.send_help()


@actual.command(
    name="Name"
)
async def full_name(ctx):
    if full_name := get_config(db_session(), "full_name"):
        await ctx.send(f"I am {full_name}.")
    else:
        await ctx.send("My name is unimportant.")

if __name__ == "__main__":
    init_db()
    for cog in cogs:
        Pythia.add_cog(cog(Pythia))

    with open("/__env__/bot.key") as key:
        token = key.read()

    Pythia.run(token, bot=True, reconnect=True)
