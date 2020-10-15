from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from discord.ext import commands
from enum import IntEnum
from inspect import signature


class Cogical(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="Logic",
        aliases=["l", "logi"]
    )
    async def logic(self, ctx, *args):
        n = len(args)
        if n == 0:
            await self.print_chars(ctx)
        elif n == 1:
            await self.truth_table(ctx, *args)
        else:
            await ctx.send("Sorry, still learning, can't handle that yet.")

    @commands.command(
        name="Symbols",
        aliases=["glc", "logichars"]
    )
    async def print_chars(self, ctx):
        await ctx.send(
            " ".join(map(str, Symbol))
            + " " +
            " ".join(map(str, Boolean))
        )

    @commands.command(
        name="Truth",
        aliases=["gtt"]
    )
    async def truth_table(self, ctx, arg: str):
        symbol = get_symbol(arg)
        if symbol:
            await ctx.send("```" + get_symbol_truth_table(symbol) + "```")
        else:
            await ctx.send("I can't make a truth table for that.")


def get_symbol(term: str):
    if len(term) != 1:
        return None
    for symbol in Symbol:
        if term == str(symbol):
            return symbol
    else:
        return None


def get_symbol_truth_table(symbol):
    sym_sig = signature(symbol._function_)
    table = " " + " | ".join(sym_sig.parameters.keys()) + " | "
    if len(sym_sig.parameters) == 2:
        table += f" {str(symbol)} ".join(sym_sig.parameters.keys())
    else:
        table += str(symbol) + "".join(sym_sig.parameters.keys())
    table += "\n" + (len(table) + 1)*"="
    for i in range(2 ** len(sym_sig.parameters)):
        table += "\n"
        args = []
        for j in range(len(sym_sig.parameters)):
            if j:
                table += " |"
            value = Boolean.TRUE if i & (j + 1) else Boolean.FALSE
            table += f" {str(value)}"
            args.append(value._bool_)
        table += " |"
        table += "  " if len(sym_sig.parameters) == 1 else "   "
        result = get_boolean_bool(symbol._function_(*args))
        table += result._symbol_
    return table


def get_boolean_bool(term: bool):
    if term:
        return Boolean.TRUE
    else:
        return Boolean.FALSE


class Boolean(IntEnum):
    TRUE = (1, '⊤', True)
    FALSE = (0, '⊥', False)

    def __new__(cls, value, symbol, bool):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._symbol_ = symbol
        obj._bool_ = bool
        return obj

    def __str__(self):
        return self._symbol_


class Symbol(IntEnum):
    NOT = (0, '¬', lambda A: not A)
    AND = (1, '∧', lambda A, B: A and B)
    OR = (2, '∨', lambda A, B: A or B)
    MATERIAL_IMPLICATION = (3, '⇒', lambda A, B: (not A) or B)
    MATERIAL_EQUIVALENCE = (
        4, '⇔', lambda A, B: (A and B) or (not A and not B))

    def __new__(cls, value, symbol, function):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._symbol_ = symbol
        obj._function_ = function
        return obj

    def __str__(self):
        return self._symbol_


class Sentence(object):

    def validate(self):
        pass

    def evaluate(self):
        pass
