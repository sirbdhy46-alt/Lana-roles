import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.logger import bot_logger as logger

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN") or os.getenv("DISCORD_TOKEN")
PREFIX = "."

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.reactions = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

COGS = [
    "cogs.role_manager",
    "cogs.aesthetic_roles",
    "cogs.giveaway",
    "cogs.ticket_system",
    "cogs.starboard",
    "cogs.voice_system",
    "cogs.guide_system",
    "cogs.autosetup",
]

BANNER = """
╔══════════════════════════════════════════╗
║   ✦ AI Server Manager  ·  discord bot   ║
║   Prefix: .   |   Ready to dominate     ║
╚══════════════════════════════════════════╝
"""

STATUS_CYCLE = [
    (".autosetup | Server Manager", discord.ActivityType.watching),
    ("your roles 👁️", discord.ActivityType.watching),
    ("the server 🛡️", discord.ActivityType.watching),
    (".help | Premium AI Bot", discord.ActivityType.playing),
]

_status_index = 0


async def rotate_status():
    global _status_index
    await bot.wait_until_ready()
    while not bot.is_closed():
        name, atype = STATUS_CYCLE[_status_index % len(STATUS_CYCLE)]
        await bot.change_presence(activity=discord.Activity(type=atype, name=name))
        _status_index += 1
        await asyncio.sleep(30)


@bot.event
async def on_ready():
    print(BANNER)
    logger.info(f"✦ Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"✦ Serving {len(bot.guilds)} guild(s)")
    bot.loop.create_task(rotate_status())


@bot.event
async def on_guild_join(guild: discord.Guild):
    logger.info(f"Joined new guild: {guild.name} ({guild.id})")
    ch = guild.system_channel or next(
        (c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None
    )
    if ch:
        embed = _welcome_embed(guild)
        await ch.send(embed=embed)


def _welcome_embed(guild: discord.Guild) -> discord.Embed:
    embed = discord.Embed(
        title="✦ AI Server Manager has arrived",
        description=(
            "```\n"
            "  ╔══════════════════════════════╗\n"
            "  ║   Premium AI Server Bot      ║\n"
            "  ║   Your server just levelled  ║\n"
            "  ║   up. Let's build it right.  ║\n"
            "  ╚══════════════════════════════╝\n"
            "```\n"
            "**Run `.autosetup` to begin full server optimization.**\n"
            "**Run `.help` to see all available commands.**"
        ),
        color=0x5865F2
    )
    embed.add_field(
        name="⚡ What I can do",
        value=(
            "• Create **90+ aesthetic roles** with symbols & colors\n"
            "• Auto-assign **♛ Server Owner** role to the owner\n"
            "• Smart **role cleanup** & hierarchy management\n"
            "• **Ticket system** with categories & transcripts\n"
            "• **Starboard**, **VC roles**, and **Server Guide**"
        ),
        inline=False
    )
    embed.set_footer(text=f"Serving {guild.name} | Prefix: .")
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    return embed


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="🔒 Access Denied",
            description=f"You need **{', '.join(error.missing_permissions)}** permission(s) to use this.",
            color=0xFF3860
        )
        await ctx.send(embed=embed, delete_after=8)
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title="⚠️ Bot Missing Permissions",
            description=f"I'm missing: `{'`, `'.join(error.missing_permissions)}`",
            color=0xFF9900
        )
        await ctx.send(embed=embed, delete_after=8)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❓ Missing Argument",
            description=f"Use `.help` to see correct usage.",
            color=0xFFDD57
        )
        await ctx.send(embed=embed, delete_after=6)
    else:
        logger.error(f"Unhandled error in [{ctx.command}]: {error}")
        embed = discord.Embed(
            title="💥 Unexpected Error",
            description=f"```{str(error)[:300]}```",
            color=0xFF3860
        )
        await ctx.send(embed=embed)


@bot.command(name="help")
async def help_command(ctx: commands.Context):
    embed = discord.Embed(
        title="",
        description=(
            "```\n"
            "╔═══════════════════════════════════════╗\n"
            "║   ✦  AI SERVER MANAGER  —  COMMANDS  ║\n"
            "║       Prefix: .   |   All Systems Go  ║\n"
            "╚═══════════════════════════════════════╝\n"
            "```"
        ),
        color=0x5865F2
    )

    sections = [
        ("⚡ Core", [
            ("`.autosetup`", "Full automated server optimization"),
            ("`.rollback`", "Restore from last backup"),
            ("`.analyze`", "Deep-scan current role structure"),
        ]),
        ("♛ Owner System", [
            ("`.assignowner`", "Auto-assign ♛ Server Owner role to guild owner"),
        ]),
        ("🎭 Roles", [
            ("`.createroles`", "Create 90+ aesthetic roles"),
            ("`.cleanroles`", "Delete empty & duplicate roles"),
            ("`.reorderroles`", "Sort roles by category"),
            ("`.optimizeadmin`", "Rename admin/mod to aesthetic format"),
            ("`.roleguide`", "Show live role guide"),
        ]),
        ("🎫 Tickets", [
            ("`.ticketpanel`", "Post interactive ticket panel"),
        ]),
        ("⭐ Starboard", [
            ("`.setupstarboard`", "Create ⭐ starboard channel"),
        ]),
        ("🎤 Voice", [
            ("`.setupvc`", "Create VC roles"),
        ]),
        ("📖 Guide", [
            ("`.setupguide`", "Create server guide channel"),
        ]),
    ]

    for name, cmds in sections:
        embed.add_field(
            name=f"━━ {name} ━━",
            value="\n".join(f"`{c}` — {d}" for c, d in cmds),
            inline=False
        )

    embed.set_footer(
        text=f"AI Server Manager  •  {ctx.guild.name}  •  Safety first, always backed up"
    )
    await ctx.send(embed=embed)


async def main():
    if not TOKEN:
        logger.error("No Discord token found! Set DISCORD_BOT_TOKEN in your environment.")
        return

    async with bot:
        for cog in COGS:
            try:
                bot.load_extension(cog)
                logger.info(f"✓ Loaded: {cog}")
            except Exception as e:
                logger.error(f"✗ Failed to load {cog}: {e}")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
