import discord
from discord.ext import commands
from utils.logger import setup_logger

logger = setup_logger("Starboard")

STAR_THRESHOLD = 3
STAR_EMOJI = "⭐"

# guild_id → starboard channel_id
starboard_channels: dict[int, int] = {}
# message_id → starboard message_id
starboard_messages: dict[int, int] = {}


class Starboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _get_starboard_channel(self, guild: discord.Guild) -> discord.TextChannel | None:
        # Check stored channel first
        channel_id = starboard_channels.get(guild.id)
        if channel_id:
            ch = guild.get_channel(channel_id)
            if ch:
                return ch
        # Fall back to name search
        return discord.utils.find(
            lambda c: "starboard" in c.name.lower(),
            guild.text_channels
        )

    @commands.command(name="setupstarboard")
    @commands.has_permissions(manage_channels=True)
    async def setup_starboard(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel = None
    ):
        """
        Set up the starboard.
        Usage: .setupstarboard           — creates a new ⭐・starboard channel
               .setupstarboard #channel  — uses an existing channel you choose
        """
        guild = ctx.guild

        if channel:
            # Use the provided existing channel
            starboard_channels[guild.id] = channel.id

            # Post the pinned welcome banner
            banner = discord.Embed(
                title="",
                description=(
                    "```\n"
                    "╔══════════════════════════════════════╗\n"
                    "║    ⭐   S T A R B O A R D           ║\n"
                    "║    Hall of Fame — Best Messages      ║\n"
                    "╚══════════════════════════════════════╝\n"
                    "```\n"
                    f"React with ⭐ on any message **{STAR_THRESHOLD}+ times** to feature it here.\n\n"
                    "The best moments from your server, preserved forever."
                ),
                color=0xFFD700
            )
            banner.set_footer(text=f"Threshold: {STAR_THRESHOLD} ⭐ reactions required")
            try:
                await channel.send(embed=banner)
            except Exception:
                pass

            result = discord.Embed(
                title="⭐ Starboard Configured!",
                description=(
                    f"Starboard set to {channel.mention}.\n"
                    f"Messages reaching **{STAR_THRESHOLD}+ ⭐** reactions will appear there."
                ),
                color=0xFFD700
            )
            result.add_field(name="Channel", value=channel.mention, inline=True)
            result.add_field(name="Threshold", value=f"{STAR_THRESHOLD} ⭐", inline=True)
            await ctx.send(embed=result)
            return

        # No channel provided — check if one already exists
        existing = self._get_starboard_channel(guild)
        if existing:
            starboard_channels[guild.id] = existing.id
            embed = discord.Embed(
                title="⭐ Starboard Already Exists",
                description=(
                    f"Starboard is already set up: {existing.mention}\n"
                    f"To use a different channel: `.setupstarboard #your-channel`"
                ),
                color=0xFFD700
            )
            await ctx.send(embed=embed)
            return

        # Create a brand new channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                send_messages=False, add_reactions=False,
                read_message_history=True, view_channel=True
            ),
            guild.me: discord.PermissionOverwrite(
                send_messages=True, embed_links=True, read_message_history=True
            )
        }
        try:
            channel = await guild.create_text_channel(
                "⭐・starboard",
                overwrites=overwrites,
                topic=f"Messages with {STAR_THRESHOLD}+ ⭐ reactions appear here — hall of fame!",
                reason="[AutoSetup] Starboard channel created"
            )
            starboard_channels[guild.id] = channel.id

            banner = discord.Embed(
                title="",
                description=(
                    "```\n"
                    "╔══════════════════════════════════════╗\n"
                    "║    ⭐   S T A R B O A R D           ║\n"
                    "║    Hall of Fame — Best Messages      ║\n"
                    "╚══════════════════════════════════════╝\n"
                    "```\n"
                    f"React with ⭐ on any message **{STAR_THRESHOLD}+ times** to feature it here.\n\n"
                    "The best moments from your server, preserved forever."
                ),
                color=0xFFD700
            )
            banner.set_footer(text=f"Threshold: {STAR_THRESHOLD} ⭐ reactions required")
            await channel.send(embed=banner)

            result = discord.Embed(
                title="⭐ Starboard Created!",
                description=(
                    f"Messages reaching **{STAR_THRESHOLD}+ ⭐** reactions will appear in {channel.mention}.\n\n"
                    f"💡 *Tip: Next time use `.setupstarboard #channel` to pick any channel.*"
                ),
                color=0xFFD700
            )
            await ctx.send(embed=result)
        except discord.Forbidden:
            await ctx.send("❌ Missing permissions to create the starboard channel.")

    @commands.command(name="setstarboard")
    @commands.has_permissions(manage_channels=True)
    async def set_starboard_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """Point the starboard at any existing channel. Usage: .setstarboard #channel"""
        starboard_channels[ctx.guild.id] = channel.id
        embed = discord.Embed(
            title="⭐ Starboard Updated",
            description=f"Starboard is now pointing to {channel.mention}.",
            color=0xFFD700
        )
        embed.add_field(name="Channel", value=channel.mention, inline=True)
        embed.add_field(name="Threshold", value=f"{STAR_THRESHOLD} ⭐", inline=True)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != STAR_EMOJI:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        channel = guild.get_channel(payload.channel_id)
        if not channel:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except Exception:
            return

        star_reaction = discord.utils.get(message.reactions, emoji=STAR_EMOJI)
        count = star_reaction.count if star_reaction else 0

        if count < STAR_THRESHOLD:
            return

        starboard = self._get_starboard_channel(guild)
        if not starboard or channel == starboard:
            return

        if message.id in starboard_messages:
            try:
                sb_msg = await starboard.fetch_message(starboard_messages[message.id])
                await sb_msg.edit(content=f"⭐ **{count}** | {channel.mention}")
            except Exception:
                pass
            return

        star_display = "⭐" * min(count, 5) + (f" **×{count}**" if count > 5 else f" **{count}**")

        embed = discord.Embed(
            description=message.content or "*[Media or embed — no text content]*",
            color=0xFFD700,
            timestamp=message.created_at
        )
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.display_avatar.url
        )
        embed.add_field(
            name="📌 Source",
            value=f"[Jump to message]({message.jump_url}) in {channel.mention}",
            inline=False
        )
        if message.attachments:
            embed.set_image(url=message.attachments[0].url)

        try:
            sb_msg = await starboard.send(
                content=f"{star_display} | {channel.mention}",
                embed=embed
            )
            starboard_messages[message.id] = sb_msg.id
            logger.info(f"Starboarded message {message.id} with {count} stars")
        except Exception as e:
            logger.error(f"Starboard post failed: {e}")


def setup(bot: commands.Bot):
    bot.add_cog(Starboard(bot))
