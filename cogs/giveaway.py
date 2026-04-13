import asyncio
import random
import re
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from utils.logger import setup_logger

logger = setup_logger("Giveaway")

# guild_id → {message_id: giveaway_data}
active_giveaways: dict[int, dict] = {}


def _parse_duration(text: str) -> int | None:
    """Parse '1h30m', '2d', '45m', '1h' → total seconds. Returns None if invalid."""
    pattern = re.compile(r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")
    m = pattern.fullmatch(text.strip().lower())
    if not m or not any(m.groups()):
        return None
    days    = int(m.group(1) or 0)
    hours   = int(m.group(2) or 0)
    minutes = int(m.group(3) or 0)
    seconds = int(m.group(4) or 0)
    total = days * 86400 + hours * 3600 + minutes * 60 + seconds
    return total if total > 0 else None


def _fmt_duration(seconds: int) -> str:
    parts = []
    if seconds >= 86400:
        parts.append(f"{seconds // 86400}d")
        seconds %= 86400
    if seconds >= 3600:
        parts.append(f"{seconds // 3600}h")
        seconds %= 3600
    if seconds >= 60:
        parts.append(f"{seconds // 60}m")
        seconds %= 60
    if seconds:
        parts.append(f"{seconds}s")
    return " ".join(parts) or "0s"


def _giveaway_embed(
    prize: str,
    host: discord.Member,
    ends_at: datetime,
    winners_count: int,
    ended: bool = False,
    winners: list[discord.Member] | None = None,
) -> discord.Embed:
    remaining = max(0, int((ends_at - datetime.now(timezone.utc)).total_seconds()))
    time_str = f"<t:{int(ends_at.timestamp())}:R>"

    if ended:
        color = 0x00E676
        header = (
            "```\n"
            "╔══════════════════════════════════════════╗\n"
            "║   🎉  G I V E A W A Y — E N D E D !    ║\n"
            "╚══════════════════════════════════════════╝\n"
            "```"
        )
        status = "**ENDED**"
    else:
        color = 0xFFD700
        bar_filled = max(0, min(16, 16 - round((remaining / max(remaining, 1)) * 0)))
        header = (
            "```\n"
            "╔══════════════════════════════════════════╗\n"
            "║   🎉  G I V E A W A Y  A C T I V E !   ║\n"
            "╚══════════════════════════════════════════╝\n"
            "```"
        )
        status = f"Ends {time_str}"

    embed = discord.Embed(title="", description=header, color=color)
    embed.add_field(
        name="🎁 Prize",
        value=f"**{prize}**",
        inline=True
    )
    embed.add_field(
        name="🏆 Winners",
        value=f"**{winners_count}**",
        inline=True
    )
    embed.add_field(
        name="👑 Hosted by",
        value=host.mention,
        inline=True
    )
    embed.add_field(
        name="⏰ Status",
        value=status,
        inline=False
    )

    if ended and winners:
        embed.add_field(
            name="🎊 Winner(s)",
            value=" ".join(w.mention for w in winners),
            inline=False
        )
    elif ended:
        embed.add_field(
            name="😢 No Winner",
            value="Not enough participants entered.",
            inline=False
        )

    if not ended:
        embed.set_footer(text="React with 🎉 to enter!")
    else:
        embed.set_footer(text="Giveaway has ended  •  Run .greroll to reroll winner")

    return embed


class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _run_giveaway(
        self,
        channel: discord.TextChannel,
        message: discord.Message,
        prize: str,
        host: discord.Member,
        duration: int,
        winners_count: int,
        ends_at: datetime,
    ):
        guild_id = channel.guild.id
        msg_id = message.id

        # Store in active giveaways
        if guild_id not in active_giveaways:
            active_giveaways[guild_id] = {}
        active_giveaways[guild_id][msg_id] = {
            "channel_id": channel.id,
            "prize": prize,
            "host_id": host.id,
            "ends_at": ends_at,
            "winners_count": winners_count,
            "ended": False,
        }

        await asyncio.sleep(duration)
        await self._end_giveaway(channel.guild, msg_id, channel, prize, host, ends_at, winners_count)

    async def _end_giveaway(
        self,
        guild: discord.Guild,
        msg_id: int,
        channel: discord.TextChannel,
        prize: str,
        host: discord.Member,
        ends_at: datetime,
        winners_count: int,
        reroll: bool = False,
    ):
        try:
            message = await channel.fetch_message(msg_id)
        except Exception:
            return

        reaction = discord.utils.get(message.reactions, emoji="🎉")
        entrants = []
        if reaction:
            async for user in reaction.users():
                if not user.bot:
                    entrants.append(user)

        winners = random.sample(entrants, min(winners_count, len(entrants))) if entrants else []

        # Update embed
        ended_embed = _giveaway_embed(prize, host, ends_at, winners_count, ended=True, winners=winners)
        try:
            await message.edit(embed=ended_embed)
        except Exception:
            pass

        # Mark ended
        guild_id = guild.id
        if guild_id in active_giveaways and msg_id in active_giveaways[guild_id]:
            active_giveaways[guild_id][msg_id]["ended"] = True

        # Announce result
        action = "🔁 **Rerolled!**" if reroll else "🎉 **Giveaway Ended!**"
        if winners:
            winner_mentions = " ".join(w.mention for w in winners)
            result_embed = discord.Embed(
                title="",
                description=(
                    "```\n"
                    "╔══════════════════════════════════════════╗\n"
                    f"║   🎊  GIVEAWAY WINNER{'S' if len(winners) > 1 else ' '} SELECTED!        ║\n"
                    "╚══════════════════════════════════════════╝\n"
                    "```"
                ),
                color=0x00E676
            )
            result_embed.add_field(name="🎁 Prize", value=f"**{prize}**", inline=True)
            result_embed.add_field(
                name=f"🏆 Winner{'s' if len(winners) > 1 else ''}",
                value=winner_mentions,
                inline=True
            )
            result_embed.add_field(
                name="📊 Entries",
                value=f"**{len(entrants)}** participants",
                inline=True
            )
            result_embed.set_footer(text="Congratulations! Contact the host to claim your prize.")
            await channel.send(
                content=f"{action} {winner_mentions} won **{prize}**! 🎉",
                embed=result_embed
            )
        else:
            await channel.send(
                embed=discord.Embed(
                    title="😢 No Valid Entries",
                    description=f"Nobody entered the **{prize}** giveaway. Better luck next time!",
                    color=0xFF3860
                )
            )

    # ── Commands ─────────────────────────────────────────────────────────

    @commands.command(name="giveaway", aliases=["gcreate", "gstart"])
    @commands.has_permissions(manage_guild=True)
    async def start_giveaway(self, ctx: commands.Context, duration: str, winners: str = "1", *, prize: str = None):
        """
        Start a giveaway.
        Usage: .giveaway <time> [winners] <prize>
        Examples:
          .giveaway 1h Steam Game
          .giveaway 30m 2w Nitro Classic
          .giveaway 2d10m Rare Role
        """
        # Allow .giveaway 1h prize OR .giveaway 1h 2w prize (with winner count)
        if prize is None:
            # winners arg is actually the prize
            prize = winners
            winners = "1"

        # Parse winner count
        winner_count = 1
        if winners.lower().endswith("w"):
            try:
                winner_count = max(1, int(winners[:-1]))
                winner_count = min(winner_count, 20)
            except ValueError:
                prize = f"{winners} {prize}" if prize else winners
        else:
            prize = f"{winners} {prize}" if prize else winners

        if not prize or not prize.strip():
            await ctx.send("❌ Please specify a prize. Example: `.giveaway 1h Steam Game`")
            return

        seconds = _parse_duration(duration)
        if seconds is None:
            await ctx.send(
                "❌ Invalid duration format.\n"
                "Examples: `30m`, `1h`, `2d`, `1h30m`, `2d12h`"
            )
            return

        if seconds > 7 * 86400:
            await ctx.send("❌ Giveaway duration cannot exceed 7 days.")
            return

        ends_at = datetime.now(timezone.utc) + timedelta(seconds=seconds)

        embed = _giveaway_embed(prize, ctx.author, ends_at, winner_count)
        embed.add_field(
            name="⏱️ Duration",
            value=f"`{_fmt_duration(seconds)}`",
            inline=True
        )

        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction("🎉")

        try:
            await ctx.message.delete()
        except Exception:
            pass

        # Kick off the timer in the background
        asyncio.create_task(
            self._run_giveaway(
                ctx.channel, msg, prize, ctx.author,
                seconds, winner_count, ends_at
            )
        )

        logger.info(f"Giveaway started: '{prize}' in {ctx.guild.name} for {_fmt_duration(seconds)}")

    @commands.command(name="gend", aliases=["gendgiveaway", "endgiveaway"])
    @commands.has_permissions(manage_guild=True)
    async def end_giveaway(self, ctx: commands.Context, message_id: int = None):
        """End an active giveaway early. Usage: .gend <message_id>"""
        guild_id = ctx.guild.id

        if message_id is None:
            # Try to find the most recent active giveaway in this channel
            giveaways = active_giveaways.get(guild_id, {})
            channel_giveaways = {
                mid: data for mid, data in giveaways.items()
                if data["channel_id"] == ctx.channel.id and not data["ended"]
            }
            if not channel_giveaways:
                await ctx.send("❌ No active giveaways found in this channel. Provide a message ID.")
                return
            message_id = max(channel_giveaways.keys())

        giveaway_data = active_giveaways.get(guild_id, {}).get(message_id)
        if not giveaway_data or giveaway_data["ended"]:
            await ctx.send("❌ That giveaway doesn't exist or has already ended.")
            return

        channel = ctx.guild.get_channel(giveaway_data["channel_id"])
        host = ctx.guild.get_member(giveaway_data["host_id"]) or ctx.author

        await ctx.send("⏩ Ending giveaway early…")
        await self._end_giveaway(
            ctx.guild, message_id, channel,
            giveaway_data["prize"], host,
            giveaway_data["ends_at"], giveaway_data["winners_count"]
        )

    @commands.command(name="greroll", aliases=["reroll"])
    @commands.has_permissions(manage_guild=True)
    async def reroll_giveaway(self, ctx: commands.Context, message_id: int = None):
        """Reroll a giveaway winner. Usage: .greroll <message_id>"""
        guild_id = ctx.guild.id

        if message_id is None:
            # Find most recent ended giveaway in this channel
            giveaways = active_giveaways.get(guild_id, {})
            ended = {
                mid: data for mid, data in giveaways.items()
                if data["channel_id"] == ctx.channel.id and data["ended"]
            }
            if not ended:
                await ctx.send("❌ No ended giveaways found in this channel. Provide a message ID.")
                return
            message_id = max(ended.keys())

        giveaway_data = active_giveaways.get(guild_id, {}).get(message_id)
        if not giveaway_data:
            await ctx.send("❌ That giveaway was not found. It may have been from a previous session.")
            return

        if not giveaway_data["ended"]:
            await ctx.send("❌ That giveaway is still running! Use `.gend` to end it first.")
            return

        channel = ctx.guild.get_channel(giveaway_data["channel_id"])
        host = ctx.guild.get_member(giveaway_data["host_id"]) or ctx.author

        await ctx.send("🔁 Rerolling…")
        await self._end_giveaway(
            ctx.guild, message_id, channel,
            giveaway_data["prize"], host,
            giveaway_data["ends_at"], giveaway_data["winners_count"],
            reroll=True
        )

    @commands.command(name="glist")
    @commands.has_permissions(manage_guild=True)
    async def list_giveaways(self, ctx: commands.Context):
        """List all active giveaways in this server."""
        giveaways = active_giveaways.get(ctx.guild.id, {})
        active = {mid: d for mid, d in giveaways.items() if not d["ended"]}

        embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║       🎉  ACTIVE GIVEAWAYS           ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=0xFFD700
        )

        if not active:
            embed.add_field(name="😴 None Active", value="No giveaways running right now.", inline=False)
        else:
            for mid, data in active.items():
                ch = ctx.guild.get_channel(data["channel_id"])
                ends_at = data["ends_at"]
                time_left = max(0, int((ends_at - datetime.now(timezone.utc)).total_seconds()))
                embed.add_field(
                    name=f"🎁 {data['prize']}",
                    value=(
                        f"**Channel:** {ch.mention if ch else 'unknown'}\n"
                        f"**Time Left:** `{_fmt_duration(time_left)}`\n"
                        f"**Winners:** {data['winners_count']}\n"
                        f"**ID:** `{mid}`"
                    ),
                    inline=True
                )

        embed.set_footer(text=f"{len(active)} active giveaway(s)  •  .gend <id> to end early")
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Giveaway(bot))
