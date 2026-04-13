import discord
from discord.ext import commands
from utils.logger import setup_logger

logger = setup_logger("AestheticRoles")

# ── Keyword → (symbol, color, label) ─────────────────────────────────────────
# Checked in order — first match wins.
PRESETS = [
    # Power / authority
    (["owner", "founder", "chief", "boss"],               "♛", 0xFFD700, "gold"),
    (["admin", "administrator", "director"],               "✦", 0xFFC200, "amber"),
    (["co-admin", "coadmin", "co admin"],                  "✧", 0xE8B400, "warm gold"),
    (["manager", "supervisor", "head"],                    "⚜", 0xD4AC0D, "dark gold"),
    (["moderator", "mod", "guard", "patrol"],              "⚡", 0xFF4500, "fire orange"),
    (["junior mod", "jr mod", "trial mod", "trial"],       "⟡", 0xFFA07A, "light orange"),
    (["staff", "team", "official", "crew official"],       "⚜", 0xD4AC0D, "staff gold"),

    # Royalty / fantasy
    (["queen", "empress"],                                 "♛", 0xFF69B4, "royal pink"),
    (["king", "emperor"],                                  "♚", 0x8B0000, "crimson"),
    (["princess", "duchess"],                              "✦", 0xFFB7C5, "blush pink"),
    (["prince", "duke"],                                   "✧", 0x6A5ACD, "slate purple"),
    (["royal", "royalty", "noble"],                        "♛", 0xFFD700, "gold"),
    (["knight", "paladin", "warrior", "soldier"],         "⚔", 0xB22222, "blood red"),
    (["wizard", "mage", "warlock", "sorcerer", "witch"],   "⌘", 0x483D8B, "arcane purple"),
    (["archer", "hunter", "ranger", "assassin"],           "🏹", 0x556B2F, "hunter green"),
    (["dragon", "dragonlord", "dragon tamer"],             "❂", 0xFF4500, "dragon red"),
    (["fairy", "sprite", "fae", "elven", "elf"],           "༄", 0xFFAEDD, "fairy pink"),
    (["mermaid", "siren", "ocean spirit"],                 "⟡", 0x00CED1, "sea teal"),

    # VIP / status
    (["vip", "very important", "exclusive"],               "✺", 0xE040FB, "vip purple"),
    (["legend", "legendary", "mythic", "goat"],            "✺", 0xFF4500, "legend orange"),
    (["elite", "supreme", "apex", "ultra"],                "✸", 0xAB47BC, "elite violet"),
    (["premium", "pro member", "gold member"],             "✦", 0xFFD700, "premium gold"),
    (["booster", "boost", "nitro"],                        "♡", 0xFF73FA, "booster pink"),
    (["veteran", "og", "original", "founder member"],      "✺", 0xFFD700, "veteran gold"),
    (["server legend", "server icon"],                     "✦", 0xFFD700, "server gold"),

    # Talents / skills
    (["artist", "art", "illustrator", "painter"],          "✹", 0xFF6B6B, "art red"),
    (["singer", "vocalist", "voice", "idol"],              "♪", 0xFF69B4, "singer pink"),
    (["rapper", "rap", "mc", "flow"],                      "♪", 0x2C2C2C, "rap dark"),
    (["dj", "disc jockey", "music producer"],              "♪", 0x00CED1, "dj teal"),
    (["coder", "programmer", "developer", "dev", "tech"],  "⌨", 0x5865F2, "dev blurple"),
    (["writer", "author", "poet", "novelist"],             "✍", 0x9C27B0, "writer purple"),
    (["streamer", "content creator", "youtuber"],          "▶", 0xFF0000, "stream red"),
    (["gamer", "gaming", "player", "game"],                "⚔", 0x1E90FF, "gamer blue"),
    (["photographer", "photo", "camera"],                  "✹", 0x607D8B, "photo grey"),

    # Cosmic / cool
    (["cosmic", "galaxy", "universe", "milky way"],        "⚝", 0x9575CD, "cosmic purple"),
    (["star", "starlight", "stellar"],                     "★", 0xFFFF00, "star yellow"),
    (["nebula", "aurora", "astral"],                       "⚝", 0xBB86FC, "nebula lavender"),
    (["comet", "meteor", "shooting star"],                 "⚝", 0x69FFFA, "comet cyan"),
    (["void", "abyss", "darkness", "black hole"],          "❖", 0x1A1A2E, "void black"),
    (["phantom", "ghost", "specter", "wraith"],            "⌗", 0x37474F, "phantom grey"),
    (["shadow", "shade", "dark", "umbra"],                 "⌗", 0x263238, "shadow dark"),

    # Nature / elemental
    (["fire", "flame", "blaze", "inferno", "pyro"],        "🔥", 0xFF4500, "fire red"),
    (["ice", "frost", "frozen", "blizzard", "arctic"],     "❄", 0x00BFFF, "ice blue"),
    (["lightning", "thunder", "storm", "bolt"],            "⚡", 0xFFFF00, "lightning yellow"),
    (["earth", "nature", "forest", "wood", "tree"],        "⚘", 0x228B22, "nature green"),
    (["ocean", "sea", "wave", "aqua", "water"],            "≋", 0x00BFFF, "ocean blue"),
    (["wind", "air", "breeze", "hurricane"],               "☁", 0x90CAF9, "sky blue"),
    (["sun", "solar", "dawn", "golden", "sunshine"],       "☼", 0xFFFF00, "sun yellow"),
    (["moon", "lunar", "moonlight", "midnight"],           "☽", 0x7E57C2, "moon purple"),
    (["night", "nightfall", "dusk", "twilight"],           "☽", 0x3F51B5, "night blue"),

    # Vibes / community
    (["chill", "relaxed", "lofi", "calm"],                 "☁", 0x90CAF9, "chill blue"),
    (["friend", "homie", "bff", "buddy", "pal"],           "♡", 0xFF69B4, "friend pink"),
    (["squad", "gang", "crew", "fam", "family"],           "✪", 0x00FF7F, "squad green"),
    (["love", "heart", "sweet", "cutie", "babe"],          "♡", 0xFF4081, "love rose"),
    (["comedian", "funny", "meme", "joke", "lol"],         "༒", 0xFF6347, "comedian orange"),
    (["cactus", "plant", "succulent"],                     "⚘", 0x2E7D32, "cactus green"),
    (["duck", "ducky", "quack"],                           "𓆪", 0xFFFF00, "duck yellow"),
    (["frog", "toad", "ribbit"],                           "𓆩", 0x00CC44, "frog green"),
    (["chaos", "anarchy", "random", "glitch"],             "⌁", 0xFF00FF, "chaos magenta"),
    (["surfer", "surf", "beach", "wave rider"],            "≈", 0x00BFFF, "surf blue"),
    (["angel", "heaven", "divine", "holy", "seraph"],      "✦", 0xFFF9C4, "divine light"),
    (["demon", "devil", "infernal", "hellfire"],           "❂", 0xFF1744, "demon red"),

    # Progression / level
    (["noob", "newbie", "beginner", "starter", "fresh"],   "✶", 0xD3D3D3, "noob grey"),
    (["rising", "rising star", "up and coming"],           "✷", 0x87CEEB, "rising sky"),
    (["pro", "professional", "skilled"],                   "✸", 0x32CD32, "pro green"),
    (["expert", "master", "advanced"],                     "✹", 0x1E90FF, "expert blue"),
    (["veteran", "old timer", "long time"],                "✺", 0xFF4500, "vet orange"),
    (["god", "deity", "omnipotent", "immortal"],           "⚝", 0xFFD700, "god gold"),
]

DEFAULT_SYMBOL = "✦"
DEFAULT_COLOR  = 0x5865F2


def _pick_preset(name: str) -> tuple[str, int, str]:
    """Return (symbol, color, color_label) for the given role name."""
    lowered = name.lower()
    for keywords, symbol, color, label in PRESETS:
        if any(kw in lowered for kw in keywords):
            return symbol, color, label
    return DEFAULT_SYMBOL, DEFAULT_COLOR, "blurple"


def _build_aesthetic_name(raw_name: str, symbol: str) -> str:
    """Prepend symbol if it isn't already there."""
    stripped = raw_name.strip()
    # Don't double-prefix if user already put a symbol
    for sym, _, _, _ in PRESETS:
        pass  # just iterate; we check below
    known_symbols = {p[0] for p in PRESETS} | {DEFAULT_SYMBOL}
    first_char = stripped[0] if stripped else ""
    if first_char in known_symbols or ord(first_char) > 127:
        return stripped  # already has a symbol
    return f"{symbol} {stripped}"


MEMBER_PERMS = discord.Permissions(
    send_messages=True, read_message_history=True, add_reactions=True,
    connect=True, speak=True
)


class AestheticRoles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="mkrole", aliases=["makerole", "newrole", "arole"])
    @commands.has_permissions(manage_roles=True)
    async def make_aesthetic_role(self, ctx: commands.Context, *, name: str):
        """
        Create an aesthetic role by just typing the name.
        The bot picks the perfect symbol, color, and style automatically.

        Usage:  .mkrole Gamer
                .mkrole Night Owl
                .mkrole Chill Vibes
                .mkrole Fire Lord
        """
        guild = ctx.guild

        symbol, color, color_label = _pick_preset(name)
        aesthetic_name = _build_aesthetic_name(name, symbol)

        # Check if it already exists
        existing = discord.utils.get(guild.roles, name=aesthetic_name)
        if existing:
            await ctx.send(embed=discord.Embed(
                title="⚠️ Role Exists",
                description=f"**{existing.name}** already exists: {existing.mention}",
                color=0xFF9900
            ))
            return

        if len(guild.roles) >= 250:
            await ctx.send("❌ This server has hit Discord's 250 role limit.")
            return

        thinking = await ctx.send(embed=discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║   ✦  AESTHETIC ROLE GENERATOR        ║\n"
                "╚══════════════════════════════════════╝\n"
                "```\n"
                f"**Analyzing:** `{name}`\n"
                f"**Symbol picked:** `{symbol}`\n"
                f"**Color picked:** `{color_label}`\n\n"
                "*Creating role…*"
            ),
            color=color
        ))

        try:
            role = await guild.create_role(
                name=aesthetic_name,
                color=discord.Color(color),
                hoist=False,
                mentionable=True,
                permissions=MEMBER_PERMS,
                reason=f"[AestheticRoles] Auto-generated by {ctx.author}"
            )
        except discord.Forbidden:
            await thinking.edit(embed=discord.Embed(
                title="❌ Missing Permissions",
                description="Bot needs **Manage Roles** permission above this role's intended position.",
                color=0xFF3860
            ))
            return
        except Exception as e:
            await thinking.edit(embed=discord.Embed(
                title="❌ Error",
                description=f"Could not create role: `{e}`",
                color=0xFF3860
            ))
            return

        # Success embed
        color_swatch = f"#{color:06X}"
        embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║   ✅  AESTHETIC ROLE CREATED!        ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=color
        )
        embed.add_field(name="🎭 Role", value=role.mention, inline=True)
        embed.add_field(name="🎨 Color", value=f"`{color_swatch}`", inline=True)
        embed.add_field(name="✦ Symbol", value=f"`{symbol}`", inline=True)
        embed.add_field(
            name="🧠 How it was generated",
            value=(
                f"**Input:** `{name}`\n"
                f"**Detected vibe:** `{color_label}`\n"
                f"**Final name:** `{aesthetic_name}`"
            ),
            inline=False
        )
        embed.add_field(
            name="📋 Quick Actions",
            value=(
                f"Give to someone: `.giverole @user {aesthetic_name}`\n"
                f"Edit color: Right-click role → Edit"
            ),
            inline=False
        )
        embed.set_footer(text="AI Aesthetic Role Generator  •  .mkrole <any name>")
        await thinking.edit(embed=embed)
        logger.info(f"Aesthetic role created: '{aesthetic_name}' in {guild.name}")

    @commands.command(name="mkroles", aliases=["makeroles", "bulkroles"])
    @commands.has_permissions(manage_roles=True)
    async def make_bulk_roles(self, ctx: commands.Context, *, names: str):
        """
        Create multiple aesthetic roles at once, comma-separated.
        Usage: .mkroles Gamer, Night Owl, Fire Lord, Chill Vibes
        """
        guild = ctx.guild
        role_names = [n.strip() for n in names.split(",") if n.strip()]

        if not role_names:
            await ctx.send("❌ Provide role names separated by commas. Example: `.mkroles Gamer, Vibe, Night Owl`")
            return

        if len(role_names) > 20:
            await ctx.send("❌ Max 20 roles at once to avoid rate limits.")
            return

        msg = await ctx.send(embed=discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║   ✦  BULK AESTHETIC ROLE GENERATOR  ║\n"
                "╚══════════════════════════════════════╝\n"
                "```\n"
                f"Creating **{len(role_names)}** aesthetic roles…"
            ),
            color=0x5865F2
        ))

        import asyncio
        created = []
        skipped = []
        failed = []

        for raw in role_names:
            symbol, color, color_label = _pick_preset(raw)
            aesthetic_name = _build_aesthetic_name(raw, symbol)

            if discord.utils.get(guild.roles, name=aesthetic_name):
                skipped.append(aesthetic_name)
                continue

            try:
                role = await guild.create_role(
                    name=aesthetic_name,
                    color=discord.Color(color),
                    hoist=False,
                    mentionable=True,
                    permissions=MEMBER_PERMS,
                    reason=f"[BulkAesthetic] Created by {ctx.author}"
                )
                created.append((aesthetic_name, color))
                await asyncio.sleep(0.4)
            except Exception as e:
                failed.append(aesthetic_name)
                logger.warning(f"Failed to create '{aesthetic_name}': {e}")

        result = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║   ✅  BULK CREATION COMPLETE!        ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=0x00E676
        )
        result.add_field(
            name="📊 Results",
            value=(
                f"✅ **Created:** {len(created)}\n"
                f"⏭ **Skipped** (existed): {len(skipped)}\n"
                f"❌ **Failed:** {len(failed)}"
            ),
            inline=False
        )
        if created:
            result.add_field(
                name="🎭 New Roles",
                value="\n".join(f"• `{n}` — `#{c:06X}`" for n, c in created[:15]),
                inline=False
            )
        if skipped:
            result.add_field(
                name="⏭ Already Existed",
                value="\n".join(f"• `{n}`" for n in skipped[:10]),
                inline=False
            )
        result.set_footer(text="AI Aesthetic Role Generator  •  .mkroles <name, name, name>")
        await msg.edit(embed=result)

    @commands.command(name="giverole")
    @commands.has_permissions(manage_roles=True)
    async def give_role(self, ctx: commands.Context, member: discord.Member, *, role_name: str):
        """
        Give a role to a member by name (no @ needed for role).
        Usage: .giverole @user Night Owl
        """
        role = discord.utils.find(
            lambda r: r.name.lower() == role_name.lower() or role_name.lower() in r.name.lower(),
            ctx.guild.roles
        )
        if not role:
            await ctx.send(f"❌ No role found matching `{role_name}`. Check the spelling.")
            return

        if role in member.roles:
            await ctx.send(f"⚠️ {member.mention} already has **{role.name}**.")
            return

        try:
            await member.add_roles(role, reason=f"[GiveRole] Assigned by {ctx.author}")
            embed = discord.Embed(
                title="✅ Role Assigned",
                description=f"{member.mention} now has {role.mention}",
                color=role.color.value or 0x00E676
            )
            embed.add_field(name="Member", value=member.mention, inline=True)
            embed.add_field(name="Role", value=role.mention, inline=True)
            embed.set_footer(text=f"Assigned by {ctx.author}")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ Missing permissions to assign that role.")


def setup(bot: commands.Bot):
    bot.add_cog(AestheticRoles(bot))
