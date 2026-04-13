import discord
from discord.ext import commands
from cogs.role_templates import CATEGORY_LABELS, CATEGORY_ORDER, CATEGORY_COLORS
from utils.logger import setup_logger

logger = setup_logger("GuideSystem")

ROLE_DESCRIPTIONS = {
    "owner":       "Full server control — the guild owner's exclusive role",
    "admin":       "Highest staff rank — full server management",
    "mod":         "Enforce rules and keep the community safe",
    "bot":         "Automated bot accounts and integrations",
    "royalty":     "Fantasy & royalty titles — Princess, King, Bishop, Knight…",
    "vip":         "Boosters, legends & special recognition roles",
    "talent":      "Skill-based roles — Artist, Singer, Writer, Coder…",
    "progression": "Skill progression — Noob → Pro → Legend → Mythic",
    "level":       "Activity-based levels earned by chatting",
    "voice":       "Dynamically assigned while in voice channels",
    "friends":     "Friend & personality roles — Best Friend, Homie, Squad…",
    "community":   "Community behavior & personality roles",
    "cool":        "Cosmic & aesthetic identity roles — Stardust, Nebula…",
    "crazy":       "Wild card roles with chaotic energy — Chaos Agent, Glitch…",
    "member":      "Default member role for all server members",
}


class GuideSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="setupguide")
    @commands.has_permissions(manage_channels=True)
    async def setup_guide(self, ctx: commands.Context):
        guild = ctx.guild
        existing = discord.utils.find(
            lambda c: "guide" in c.name.lower() or "info" in c.name.lower(),
            guild.text_channels
        )
        if existing:
            embed = discord.Embed(
                title="📖 Guide Already Exists",
                description=f"Server guide is already up at {existing.mention}",
                color=0x5865F2
            )
            await ctx.send(embed=embed)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=True, send_messages=False, read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                send_messages=True, embed_links=True, manage_messages=True
            )
        }
        try:
            channel = await guild.create_text_channel(
                "📖・server-guide",
                overwrites=overwrites,
                topic="Everything you need to know about this server",
                reason="[AutoSetup] Server guide channel"
            )
            await self._post_guide(channel, guild)
            embed = discord.Embed(
                title="📖 Server Guide Created!",
                description=f"Your server guide has been set up at {channel.mention}",
                color=0x5865F2
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ Missing permissions to create the guide channel.")

    async def _post_guide(self, channel: discord.TextChannel, guild: discord.Guild):
        welcome = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════════════╗\n"
                f"║   ✦  WELCOME TO {guild.name[:28].upper():<28}║\n"
                "║        Your complete server handbook         ║\n"
                "╚══════════════════════════════════════════════╝\n"
                "```\n"
                "This guide covers every role, system, and feature available in this server.\n"
                "Read through to understand how everything works!\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "📖 **Sections below:**\n"
                "• 🎭 Role Structure & Categories\n"
                "• ⚙️ Server Systems Overview\n"
                "• 🤖 Bot Commands Reference\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=0x5865F2
        )
        welcome.set_thumbnail(url=guild.icon.url if guild.icon else None)
        welcome.set_footer(text="Use .roleguide for the live role list  |  .help for all commands")
        await channel.send(embed=welcome)

        role_embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║    🎭   ROLE STRUCTURE GUIDE         ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=0x7289DA
        )
        for cat in CATEGORY_ORDER:
            label = CATEGORY_LABELS[cat]
            desc = ROLE_DESCRIPTIONS.get(cat, "")
            role_embed.add_field(name=label, value=desc, inline=False)
        await channel.send(embed=role_embed)

        systems_embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║    ⚙️   SERVER SYSTEMS OVERVIEW      ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=0x00BCD4
        )
        systems_embed.add_field(
            name="🎫 Ticket System",
            value=(
                "Open a private support ticket using `.ticketpanel`.\n"
                "**Categories:** Support · Report · Partnership · Help · Appeal\n"
                "Tickets are private — only you and staff can see them."
            ),
            inline=False
        )
        systems_embed.add_field(
            name="⭐ Starboard",
            value=(
                "React to any message with ⭐ **3+ times** to feature it in the Hall of Fame!\n"
                "The best moments live forever in `#⭐・starboard`."
            ),
            inline=False
        )
        systems_embed.add_field(
            name="🎤 Voice Roles",
            value=(
                "You automatically receive the `☁ Active Voice` role when you join a voice channel.\n"
                "It's removed when you leave."
            ),
            inline=False
        )
        systems_embed.add_field(
            name="📈 Progression System",
            value=(
                "Earn roles by being active: `✶ Noob` → `✷ Rising Star` → `✸ Pro` → `✹ Expert` → `✺ Legend` → `❂ Diamond` → `♛ Mythic`\n"
                "Level roles (`❖ Level 5` through `❖ Level 100`) are earned by chatting."
            ),
            inline=False
        )
        systems_embed.add_field(
            name="♛ Owner Role",
            value=(
                "The server owner automatically receives the `♛ Server Owner` role.\n"
                "This role is managed by the AI Server Manager bot."
            ),
            inline=False
        )
        await channel.send(embed=systems_embed)

        commands_embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║    🤖   BOT COMMANDS REFERENCE       ║\n"
                "║          Prefix: .                   ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=0xFFD740
        )
        commands_embed.add_field(
            name="⚡ Core Commands",
            value=(
                "`.autosetup` — Full automated server optimization\n"
                "`.rollback` — Restore server from last backup\n"
                "`.analyze` — Scan and report on role structure"
            ),
            inline=False
        )
        commands_embed.add_field(
            name="🎭 Role Management",
            value=(
                "`.createroles` — Create all 90+ template roles\n"
                "`.cleanroles` — Remove empty/duplicate roles\n"
                "`.reorderroles` — Sort roles by category\n"
                "`.optimizeadmin` — Rename staff roles aesthetically\n"
                "`.assignowner` — Assign ♛ Server Owner role\n"
                "`.roleguide` — Show live role guide"
            ),
            inline=False
        )
        commands_embed.add_field(
            name="🎫 Systems",
            value=(
                "`.ticketpanel` — Post ticket panel\n"
                "`.setupstarboard` — Create starboard channel\n"
                "`.setupvc` — Create voice roles\n"
                "`.setupguide` — Create this guide channel"
            ),
            inline=False
        )
        commands_embed.set_footer(text="AI Server Manager  •  Premium Bot  •  Safety first")
        await channel.send(embed=commands_embed)

        logger.info(f"Server guide posted in #{channel.name} ({guild.name})")


def setup(bot: commands.Bot):
    bot.add_cog(GuideSystem(bot))
