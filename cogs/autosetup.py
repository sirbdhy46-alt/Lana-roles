import asyncio
import discord
from discord.ext import commands
from utils.backup import create_backup
from utils.logger import setup_logger
from cogs.role_templates import CATEGORY_ORDER, CATEGORY_LABELS

logger = setup_logger("AutoSetup")

PROGRESS_STEPS = [
    ("📦", "Backup",           "Creating a full backup of all existing roles…"),
    ("💥", "Nuclear Wipe",     "Deleting ALL existing roles for a clean slate…"),
    ("🎭", "Role Creation",    "Building 121 aesthetic roles across 15 categories…"),
    ("🔄", "Reorder",          "Sorting all roles into proper category order…"),
    ("🧠", "Member Analysis",  "Analyzing every member & auto-assigning roles by power…"),
    ("⭐", "Systems Setup",    "Configuring Starboard, Voice roles & Server Guide…"),
]


def _progress_bar(step: int, total: int, width: int = 16) -> str:
    filled = round((step / total) * width)
    return "█" * filled + "░" * (width - filled)


class AutoSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _update_progress(self, msg: discord.Message, step: int, guild: discord.Guild):
        total = len(PROGRESS_STEPS)
        icon, name, detail = PROGRESS_STEPS[step]
        pct = round((step / total) * 100)
        bar = _progress_bar(step, total)

        steps_display = ""
        for i, (ic, nm, _) in enumerate(PROGRESS_STEPS):
            if i < step:
                steps_display += f"✅ {ic} {nm}\n"
            elif i == step:
                steps_display += f"⏳ {ic} **{nm}** ← *running*\n"
            else:
                steps_display += f"⬜ {ic} {nm}\n"

        embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   🚀  AI SERVER MANAGER — AUTO SETUP    ║\n"
                f"║   {bar}  {pct:3d}%  ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```"
            ),
            color=0x5865F2
        )
        embed.add_field(
            name=f"{icon} Currently: {name}",
            value=f"*{detail}*",
            inline=False
        )
        embed.add_field(name="📋 Progress", value=steps_display, inline=False)
        embed.add_field(
            name="🏠 Server",
            value=f"`{guild.name}` — {guild.member_count} members",
            inline=True
        )
        embed.add_field(
            name="📊 Roles",
            value=f"`{len(guild.roles) - 1}` active",
            inline=True
        )
        embed.set_footer(text="Do not close this message — setup is running…")
        try:
            await msg.edit(embed=embed)
        except Exception:
            pass

    @commands.command(name="autosetup")
    @commands.has_permissions(administrator=True)
    async def autosetup(self, ctx: commands.Context, starboard_channel: discord.TextChannel = None):
        """
        Full server nuclear rebuild.
        Usage: .autosetup            — auto-creates ⭐・starboard channel
               .autosetup #channel  — uses an existing channel for starboard
        """
        guild = ctx.guild

        start_embed = discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   🚀  AI SERVER MANAGER — AUTO SETUP    ║\n"
                "║   ░░░░░░░░░░░░░░░░  0%               ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```\n"
                f"**Full nuclear rebuild for `{guild.name}`**\n\n"
                f"👥 **Members:** {guild.member_count}\n"
                f"🎭 **Current Roles:** {len(guild.roles) - 1}\n"
                f"📋 **Steps:** {len(PROGRESS_STEPS)}\n"
                f"⭐ **Starboard:** {starboard_channel.mention if starboard_channel else 'will create `⭐・starboard`'}\n\n"
                "⚠️ *ALL roles will be wiped and rebuilt fresh. Backup saved first.*"
            ),
            color=0x5865F2
        )
        msg = await ctx.send(embed=start_embed)
        await asyncio.sleep(2)

        role_manager = self.bot.cogs.get("RoleManager")

        # ── Step 0: Backup ──────────────────────────────────────────────
        await self._update_progress(msg, 0, guild)
        await create_backup(guild)
        await asyncio.sleep(1)

        # ── Step 1: Nuclear wipe ────────────────────────────────────────
        await self._update_progress(msg, 1, guild)
        deleted = 0
        if role_manager:
            deleted = await role_manager._nuke_roles(guild)
        await asyncio.sleep(0.5)

        # ── Step 2: Create all 121 roles + assign owner (once) ──────────
        await self._update_progress(msg, 2, guild)
        created = 0
        failed = 0
        owner_role = None
        if role_manager:
            created, failed, owner_role = await role_manager._create_all_roles(guild)
            # Assign owner role exactly ONCE right here
            owner_assigned = await role_manager._assign_owner_role(guild, owner_role)

            owner_label = "✅ Assigned" if owner_assigned else "⚠️ Skipped"
            await ctx.send(embed=discord.Embed(
                title="♛ Owner Role",
                description=(
                    f"**{owner_role.name if owner_role else '♛ Server Owner'}** → "
                    f"{guild.owner.mention if guild.owner else 'unknown'}\n"
                    f"Status: {owner_label}"
                ),
                color=0xFFD700
            ))
        await asyncio.sleep(1)

        # ── Step 3: Reorder ─────────────────────────────────────────────
        await self._update_progress(msg, 3, guild)
        positioned = 0
        if role_manager:
            positioned = await role_manager._reorder_all_roles(guild)
        await asyncio.sleep(1)

        # ── Step 4: Auto-assign members by power ────────────────────────
        await self._update_progress(msg, 4, guild)
        role_counts: dict[str, int] = {}
        total_assignments = 0
        if role_manager:
            role_counts = await role_manager._auto_assign_member_roles(guild)
            total_assignments = sum(role_counts.values())

            top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:6]
            assign_embed = discord.Embed(
                title="🧠 Member Analysis Complete",
                description=(
                    f"✅ **{total_assignments}** role assignments across **{guild.member_count}** members\n\n"
                    + "\n".join(f"• `{n}` — {c} member(s)" for n, c in top_roles)
                ),
                color=0x00E676
            )
            await ctx.send(embed=assign_embed)
        await asyncio.sleep(1)

        # ── Step 5: Systems setup ───────────────────────────────────────
        await self._update_progress(msg, 5, guild)

        starboard_cog = self.bot.cogs.get("Starboard")
        if starboard_cog:
            await starboard_cog.setup_starboard(ctx, starboard_channel)

        vc_cog = self.bot.cogs.get("VoiceSystem")
        if vc_cog:
            await vc_cog.setup_vc(ctx)

        guide_cog = self.bot.cogs.get("GuideSystem")
        if guide_cog:
            await guide_cog.setup_guide(ctx)

        await asyncio.sleep(1)

        # ── Final summary ───────────────────────────────────────────────
        final_embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   🚀  AI SERVER MANAGER — AUTO SETUP    ║\n"
                "║   ████████████████  100%  COMPLETE!  ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```"
            ),
            color=0x00E676
        )
        final_embed.add_field(
            name="✅ All Done!",
            value="\n".join(f"✅ {ic} **{nm}**" for ic, nm, _ in PROGRESS_STEPS),
            inline=False
        )
        final_embed.add_field(
            name="📊 Final Stats",
            value=(
                f"💥 **Roles Wiped:** {deleted}\n"
                f"🎭 **Roles Created:** {created}\n"
                f"🔄 **Roles Reordered:** {positioned}\n"
                f"🧠 **Assignments Made:** {total_assignments}\n"
                f"📋 **Total Roles:** {len(guild.roles) - 1}\n"
                f"👥 **Members:** {guild.member_count}"
            ),
            inline=True
        )
        final_embed.add_field(
            name="🛡️ Safety",
            value="Backup saved at start.\nRun `.rollback` to undo everything.",
            inline=True
        )
        final_embed.set_footer(text="AI Server Manager  •  Run .help to see all commands")
        await msg.edit(embed=final_embed)
        logger.info(f"AutoSetup complete for {guild.name}")


def setup(bot: commands.Bot):
    bot.add_cog(AutoSetup(bot))
