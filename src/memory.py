from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext import commands
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pythia_utilities import pagified_send

engine = db.create_engine("sqlite:////__env__/memory.db")
Base = declarative_base(engine)


def db_session():
    return sessionmaker(bind=engine, autoflush=True)()


def init_db():
    Base.metadata.create_all()


class Useful(Base):
    __tablename__ = "usefuls"
    useful_key = db.Column(db.Unicode(256), primary_key=True)
    useful_msg = db.Column(db.UnicodeText)

    def __init__(self, key, msg):
        self.useful_key = key
        self.useful_msg = msg


class Memory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = db_session()

    @commands.command(
        name="Remember",
        aliases=["save", "store"],
    )
    async def save_useful(self, ctx, key: str, msg: str):
        if self.session.query(Useful).filter(
                    Useful.useful_key == key
                ).one_or_none():
            await ctx.send(
                f"I'm already remembering something for {key}"
                + ", do you want to **revise** it?"
            )
        else:
            entry = self.session.merge(Useful(key, msg))
            self.session.commit()
            await pagified_send(
                ctx,
                f"Remembering {entry.useful_msg} for {entry.useful_key}."
            )

    @commands.command(
        name="Recall",
        aliases=["query", "load"],
    )
    async def show_useful(self, ctx, key: str):
        if result := self.session.query(Useful.useful_msg).filter(
                    Useful.useful_key == key
                ).one_or_none():
            await pagified_send(ctx, result.useful_msg)
        else:
            await ctx.send("I don't **remember** anything for that, sorry.")

    @commands.command(
        name="Append",
        aliases=["extend", "add"],
    )
    async def append_useful(self, ctx, key: str, msg: str):
        if result := self.session.query(Useful).filter(
                    Useful.useful_key == key
                ).one_or_none():
            compound = result.useful_msg + "\n" + msg
            self.session.query(Useful).filter(Useful.useful_key == key).update(
                {"useful_msg": compound},
                synchronize_session="evaluate"
            )
            self.session.commit()
            result = self.session.query(Useful).filter(
                Useful.useful_key == key
            ).one()
            await pagified_send(
                ctx,
                f"I'm now remembering {result.useful_msg} "
                + f"for {result.useful_key}."
            )
        else:
            await ctx.send(
                f"I'm not currently remembering anything for {key}"
                + ", do you want me to **remember** this?"
            )

    @commands.command(
        name="Revise",
        aliases=["overwrite", "update"],
    )
    async def update_useful(self, ctx, key: str, msg: str):
        if self.session.query(Useful).filter(
                    Useful.useful_key == key
                ).one_or_none():
            self.session.query(Useful).filter(Useful.useful_key == key).update(
                {"useful_msg": msg},
                synchronize_session="evaluate"
            )
            self.session.commit()
            result = self.session.query(Useful).filter(
                Useful.useful_key == key
            ).one()
            await ctx.send(
                f"I'm now remembering {result.useful_msg} "
                + f"for {result.useful_key}."
            )
        else:
            await ctx.send(
                f"I'm not currently remembering anything for {key}"
                + ", do you want me to **remember** this?"
            )

    @commands.command(
        name="Forget",
        aliases=["delete", "remove", "clear"],
    )
    async def delete_useful(self, ctx, key: str):
        if self.session.query(Useful).filter(
                    Useful.useful_key == key
                ).one_or_none():
            self.session.query(Useful).filter(
                Useful.useful_key == key
            ).delete()
            self.session.commit()
            await ctx.send(
                f"I've forgotten what I had for {key}."
            )
        else:
            await ctx.send(
                f"I'm don't remember anything for {key}, so, job done?"
            )

    @commands.command(
        name="Recite",
        aliases=["list", "keys", "dir"],
    )
    async def list_useful(self, ctx):
        raw = self.session.query(Useful.useful_key).all()
        msg = f"I'm currently remember {len(raw)} things, for:"
        for entry in raw:
            msg += f"\n{entry.useful_key}"
        await pagified_send(ctx, msg)


class Config(Base):
    __tablename__ = "configuration"
    config_key = db.Column(db.Unicode(256), primary_key=True)
    config_val = db.Column(db.UnicodeText)

    def __init__(self, key, val):
        self.config_key = key
        self.config_val = val


class Host(Base):
    __tablename__ = "hosts"
    hostname = db.Column(db.Unicode(24), primary_key=True)
    ip_address = db.Column(db.Unicode(12))
    url_address = db.Column(db.Unicode(48))
    mac_address = db.Column(db.Unicode(18))

    def __init__(
        self,
        hostname,
        url_address="",
        ip_address="",
        mac_address=""
    ):
        self.hostname = hostname
        self.url_address = url_address
        self.ip_address = ip_address
        self.mac_address = mac_address


class Configuration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = db_session()

    @commands.command(
        name="Configure",
        aliases=["set", "config_set", "config_save"]
    )
    @commands.is_owner()
    async def set_config(self, ctx, key: str, val: str):
        if self.session.query(Config).filter(
                    Config.config_key == key
                ).one_or_none():
            self.session.query(Config).filter(Config.config_key == key).update(
                {"config_val": val},
                synchronize_session="evaluate"
            )
            self.session.commit()
            result = self.session.query(Config).filter(
                Config.config_key == key
            ).one()
            await ctx.send(
                f"Updated config `{result.config_key}` "
                + f"to `{result.config_val}`."
            )
        else:
            entry = self.session.merge(Config(key, val))
            self.session.commit()
            await ctx.send(
                f"Added config `{entry.config_key}` as `{entry.config_val}`."
            )

    @commands.command(
        name="Unconfigure",
        aliases=["del", "config_del", "config_clear"],
    )
    @commands.is_owner()
    async def del_config(self, ctx, key: str):
        if self.session.query(Config).filter(
                    Config.config_key == key
                ).one_or_none():
            self.session.query(Config).filter(
                Config.config_key == key
            ).delete()
            self.session.commit()
            await ctx.send(
                f"Deleted the value for `{key}`."
            )
        else:
            await ctx.send(
                f"I don't have a value for `{key}` anyway."
            )

    @commands.command(
        name="Config",
        aliases=["dump_config", "config_list"],
    )
    @commands.is_owner()
    async def list_config(self, ctx):
        raw = self.session.query(Config).all()
        msg = ""
        for entry in raw:
            msg += f"\n{entry.config_key}: \"{entry.config_val}\""
        await pagified_send(ctx, msg, code_block=True)

    @commands.command(
        name="Host",
        aliases=["host_add", "host_set"]
    )
    @commands.is_owner()
    async def set_host(self, ctx, *args: str):
        if self.session.query(Host).filter(
                    Host.hostname == args[0]
                ).one_or_none():
            self.session.query(Host).filter(Host.hostname == args[0]).update(
                {"url_address": args[1],
                 "ip_address": args[2],
                 "mac_address": args[3]},
                synchronize_session="evaluate"
            )
            self.session.commit()
            result = self.session.query(Host).filter(
                Host.hostname == args[0]
            ).one()
            await ctx.send(
                f"Updated host `{result.hostname}` "
                + "with:\n```"
                + f"url_address : {result.url_address}\n"
                + f"ip_address : {result.ip_address}\n"
                + f"mac_address : {result.mac_address}"
                + "```"
            )
        else:
            entry = self.session.merge(Host(*args))
            self.session.commit()
            await ctx.send(
                f"Added host `{entry.hostname}` "
                + "with:\n```"
                + f"url_address : {entry.url_address}\n"
                + f"ip_address : {entry.ip_address}\n"
                + f"mac_address : {entry.mac_address}"
                + "```"
            )

    @commands.command(
        name="Unhost",
        aliases=["host_rem", "host_del"],
    )
    @commands.is_owner()
    async def del_host(self, ctx, name: str):
        if self.session.query(Host).filter(
                    Host.hostname == name
                ).one_or_none():
            self.session.query(Host).filter(
                Host.hostname == name
            ).delete()
            self.session.commit()
            await ctx.send(
                f"Deleted the host `{name}`."
            )
        else:
            await ctx.send(
                f"I already don't have an entry for `{name}`."
            )

    @commands.command(
        name="Hosts",
        aliases=["dump_host", "host_list"],
    )
    @commands.is_owner()
    async def list_host(self, ctx):
        raw = self.session.query(Host).all()
        msg = ""
        for entry in raw:
            msg += (
                f"host : {entry.hostname}\n"
                + f" - url_address : {entry.url_address}\n"
                + f" - ip_address : {entry.ip_address}\n"
                + f" - mac_address : {entry.mac_address}\n\n"
            )
        await pagified_send(ctx, msg, code_block=True)
