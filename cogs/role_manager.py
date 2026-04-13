import asyncio
import discord
from discord.ext import commands
from utils.logger import setup_logger
from utils.backup import create_backup, restore_backup
from cogs.role_templates import ROLE_TEMPLATES, CATEGORY_ORDER, CATEGORY_LABELS, CATEGORY_COLORS

logger = setup_logger("RoleManager")

MAX_ROLES = 150

# ── Progression tiers keyed by days in server ──────────────────────────────
PROGRESSION_TIERS = [
    (730, "✺ Legend",       "❖ Level 100"),
    (365, "✺ Legend",       "❖ Level 75"),
    (180, "✹ Expert",       "❖ Level 50"),
    (90,  "✸ Pro",          "❖ Level 25"),
    (30,  "✷ Rising Star",  "❖ Level 10"),
    (7,   "✷ Rising Star",  "❖ Level 5"),
    (0,   "✶ Noob",         "❖ Newcomer"),
]


def _is_admin_like(role: discord.Role) -> bool:
    p = role.permissions
    return p.administrator or p.manage_guild or p.manage_roles


def _is_bot_role(role: discord.Role) -> bool:
    return role.is_bot_managed() or role.is_integration()


def _fancy_bar(value: int, total: int, length: int = 10) -> str:
    filled = round((value / max(total, 1)) * length)
    return "█" * filled + "░" * (length - filled)


class RoleManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── Internal helpers ────────────────────────────────────────────────

    async def _nuke_roles(self, guild: discord.Guild) -> int:
        """Delete ALL non-default, non-bot-managed roles. Returns count deleted."""
        deleted = 0
        bot_top = guild.me.top_role

        roles_to_kill = [
            r for r in guild.roles
            if not r.is_default()
            and not _is_bot_role(r)
            and r != bot_top
            and r < bot_top
        ]

        for role in sorted(roles_to_kill, key=lambda r: r.position):
            try:
                await role.delete(reason="[NukeBuild] Full role wipe — fresh rebuild")
                deleted += 1
                await asyncio.sleep(0.3)
            except Exception as e:
                logger.warning(f"Could not delete {role.name}: {e}")

        return deleted

    async def _create_all_roles(self, guild: discord.Guild) -> tuple[int, int, discord.Role | None]:
        """
        Create ALL 121 roles from templates (assumes roles were nuked first).
        Returns (created, failed, owner_role).
        Owner role is returned so caller can assign it once.
        """
        created = 0
        failed = 0
        owner_role: discord.Role | None = None

        for template in ROLE_TEMPLATES:
            if created >= MAX_ROLES:
                break
            try:
                role = await guild.create_role(
                    name=template["name"],
                    color=discord.Color(template["color"]),
                    hoist=template["hoist"],
                    mentionable=template["mentionable"],
                    permissions=template["permissions"],
                    reason="[NukeBuild] Fresh role creation"
                )
                if template.get("auto_assign_owner"):
                    owner_role = role
                created += 1
                await asyncio.sleep(0.35)
            except discord.Forbidden:
                logger.warning(f"Forbidden: could not create {template['name']}")
                failed += 1
            except Exception as e:
                logger.error(f"Error creating {template['name']}: {e}")
                failed += 1

        return created, failed, owner_role

    async def _assign_owner_role(self, guild: discord.Guild, owner_role: discord.Role | None) -> bool:
        """Assign the owner role to the guild owner. Returns True on success."""
        if not owner_role or not guild.owner:
            return False
        try:
            await guild.owner.add_roles(owner_role, reason="[NukeBuild] Auto-assigning ♛ Server Owner")
            return True
        except Exception as e:
            logger.warning(f"Could not assign owner role: {e}")
            return False

    async def _reorder_all_roles(self, guild: discord.Guild) -> int:
        """Sort all roles into category order. Returns count positioned."""
        template_names = {t["name"]: t["category"] for t in ROLE_TEMPLATES}
        categorized: dict[str, list[discord.Role]] = {c: [] for c in CATEGORY_ORDER}
        uncategorized: list[discord.Role] = []

        for role in guild.roles:
            if role.is_default():
                continue
            cat = template_names.get(role.name)
            if cat and cat in categorized:
                categorized[cat].append(role)
            else:
                uncategorized.append(role)

        ordered: list[discord.Role] = []
        for cat in CATEGORY_ORDER:
            ordered.extend(categorized[cat])
        ordered.extend(uncategorized)

        positions = {}
        pos = max(1, guild.me.top_role.position - 1)
        for role in ordered:
            if role < guild.me.top_role:
                positions[role] = max(1, pos)
                pos = max(1, pos - 1)

        try:
            await guild.edit_role_positions(positions=positions, reason="[NukeBuild] Reorder by category")
            return len(positions)
        except Exception as e:
            logger.warning(f"Reorder failed: {e}")
            return 0

    async def _auto_assign_member_roles(self, guild: discord.Guild) -> dict[str, int]:
        """
        Analyze every member by power level and join date, then assign
        the appropriate template roles automatically.
        Returns a dict of role_name → count assigned.
        """
        role_lookup = {r.name: r for r in guild.roles}
        assigned_counts: dict[str, int] = {}

        def get(name: str) -> discord.Role | None:
            return role_lookup.get(name)

        for member in guild.members:
            if member.bot:
                continue

            roles_to_add: list[discord.Role] = []

            def queue(name: str):
                r = get(name)
                if r and r not in member.roles and r not in roles_to_add:
                    roles_to_add.append(r)

            # Base member role — everyone gets this
            queue("➤ Member")

            perms = member.guild_permissions

            # ── Power tier ──────────────────────────────────────────
            if member.id == guild.owner_id:
                queue("♛ Server Owner")

            elif perms.administrator:
                queue("✦ Administrator")

            elif perms.kick_members and perms.ban_members:
                if perms.view_audit_log and perms.manage_channels:
                    queue("⚡ Head Moderator")
                else:
                    queue("✩ Senior Moderator")

            elif perms.kick_members or perms.ban_members:
                queue("✧ Moderator")

            elif perms.manage_messages:
                queue("⟡ Junior Moderator")

            # ── Server booster ──────────────────────────────────────
            if member.premium_since:
                queue("♡ Server Booster")

            # ── Join-date progression ───────────────────────────────
            if member.joined_at:
                days = (discord.utils.utcnow() - member.joined_at).days
                for threshold, prog_role, level_role in PROGRESSION_TIERS:
                    if days >= threshold:
                        queue(prog_role)
                        queue(level_role)
                        break

            # ── Assign in bulk ──────────────────────────────────────
            if roles_to_add:
                try:
                    await member.add_roles(*roles_to_add, reason="[AutoAssign] Power-based analysis")
                    for r in roles_to_add:
                        assigned_counts[r.name] = assigned_counts.get(r.name, 0) + 1
                    await asyncio.sleep(0.2)
                except discord.Forbidden:
                    logger.warning(f"Forbidden assigning roles to {member.display_name}")
                except Exception as e:
                    logger.warning(f"Could not assign roles to {member.display_name}: {e}")

        return assigned_counts

    # ── Commands ────────────────────────────────────────────────────────

    @commands.command(name="nukebuild")
    @commands.has_permissions(administrator=True)
    async def nuke_build(self, ctx: commands.Context):
        """Full nuclear rebuild: wipe all roles, create 121 fresh, reorder, assign members."""
        guild = ctx.guild

        embed = discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   💥  NUCLEAR REBUILD — INITIATED        ║\n"
                "║   All roles will be wiped & recreated    ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```\n"
                "⚠️ **This will delete every non-bot role and rebuild from scratch.**\n"
                "Creating backup first…"
            ),
            color=0xFF1744
        )
        msg = await ctx.send(embed=embed)
        await create_backup(guild)
        await asyncio.sleep(1)

        # Step 1: Nuke
        await msg.edit(embed=discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   💥  STEP 1/4 — WIPING ALL ROLES…      ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```"
            ),
            color=0xFF1744
        ))
        deleted = await self._nuke_roles(guild)
        await asyncio.sleep(0.5)

        # Step 2: Create
        await msg.edit(embed=discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   🎭  STEP 2/4 — CREATING 121 ROLES…    ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```"
            ),
            color=0x5865F2
        ))
        created, failed, owner_role = await self._create_all_roles(guild)
        assigned = await self._assign_owner_role(guild, owner_role)
        await asyncio.sleep(0.5)

        # Step 3: Reorder
        await msg.edit(embed=discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   🔄  STEP 3/4 — REORDERING…            ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```"
            ),
            color=0x00BCD4
        ))
        positioned = await self._reorder_all_roles(guild)
        await asyncio.sleep(0.5)

        # Step 4: Auto-assign
        await msg.edit(embed=discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   🧠  STEP 4/4 — ANALYZING MEMBERS…     ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```"
            ),
            color=0x00E676
        ))
        role_counts = await self._auto_assign_member_roles(guild)
        total_assigned = sum(role_counts.values())

        # Final report
        top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        top_str = "\n".join(f"• `{n}` — {c} member(s)" for n, c in top_roles) or "None"

        final = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   ✅  NUCLEAR REBUILD — COMPLETE!        ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```"
            ),
            color=0x00E676
        )
        final.add_field(
            name="💥 Rebuild Summary",
            value=(
                f"🗑️ **Roles Deleted:** {deleted}\n"
                f"🎭 **Roles Created:** {created}\n"
                f"❌ **Failed:** {failed}\n"
                f"🔄 **Roles Reordered:** {positioned}\n"
                f"♛ **Owner Role Assigned:** {'✅' if assigned else '⚠️ skipped'}"
            ),
            inline=True
        )
        final.add_field(
            name="🧠 Member Auto-Assignment",
            value=(
                f"👥 **Members Processed:** {guild.member_count}\n"
                f"✅ **Total Assignments:** {total_assigned}\n\n"
                f"**Top Roles:**\n{top_str}"
            ),
            inline=True
        )
        final.set_footer(text="Run .rollback anytime to restore from backup  •  AI Server Manager")
        await msg.edit(embed=final)

    @commands.command(name="assignroles")
    @commands.has_permissions(administrator=True)
    async def assign_member_roles(self, ctx: commands.Context):
        """Analyze all members by power and join date, auto-assign matching roles."""
        guild = ctx.guild
        msg = await ctx.send(embed=discord.Embed(
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   🧠  MEMBER POWER ANALYSIS              ║\n"
                "║   Scanning every member & assigning…     ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```\n"
                f"Processing **{guild.member_count}** members — this may take a moment…"
            ),
            color=0x5865F2
        ))

        role_counts = await self._auto_assign_member_roles(guild)
        total_assigned = sum(role_counts.values())
        top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:12]

        embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════════╗\n"
                "║   ✅  MEMBER ANALYSIS COMPLETE!          ║\n"
                "╚══════════════════════════════════════════╝\n"
                "```"
            ),
            color=0x00E676
        )
        embed.add_field(
            name="📊 Overview",
            value=(
                f"👥 **Members Scanned:** {guild.member_count}\n"
                f"✅ **Role Assignments:** {total_assigned}\n"
                f"📋 **Unique Roles Given:** {len(role_counts)}"
            ),
            inline=False
        )

        if top_roles:
            embed.add_field(
                name="🏆 Top Assigned Roles",
                value="\n".join(
                    f"`{_fancy_bar(c, top_roles[0][1], 8)}` **{n}** — {c}"
                    for n, c in top_roles
                ),
                inline=False
            )

        embed.add_field(
            name="🧠 Logic Used",
            value=(
                "• **Owner** → ♛ Server Owner\n"
                "• **Admin perm** → ✦ Administrator\n"
                "• **Kick + Ban** → ⚡ Head / ✩ Senior Mod\n"
                "• **Kick or Ban** → ✧ Moderator\n"
                "• **Manage Msgs** → ⟡ Junior Mod\n"
                "• **Booster** → ♡ Server Booster\n"
                "• **Join date** → Progression + Level role\n"
                "• **Everyone** → ➤ Member"
            ),
            inline=False
        )
        embed.set_footer(text="Run .assignroles again anytime to catch new members")
        await msg.edit(embed=embed)

    # ── Reorder command ─────────────────────────────────────────────────

    @commands.command(name="reorderroles")
    @commands.has_permissions(manage_roles=True)
    async def reorder_roles(self, ctx: commands.Context):
        """Sort all roles into proper category order."""
        guild = ctx.guild
        msg = await ctx.send("🔄 **Reordering roles by category…** This may take a moment.")
        positioned = await self._reorder_all_roles(guild)

        template_names = {t["name"]: t["category"] for t in ROLE_TEMPLATES}
        categorized: dict[str, list[discord.Role]] = {c: [] for c in CATEGORY_ORDER}
        for role in guild.roles:
            cat = template_names.get(role.name)
            if cat:
                categorized[cat].append(role)

        embed = discord.Embed(
            title="🔄 Roles Reordered",
            description=(
                f"**{positioned}** roles sorted into **{len(CATEGORY_ORDER)}** categories.\n\n"
                + "\n".join(
                    f"**{CATEGORY_LABELS[c]}** — {len(categorized[c])} roles"
                    for c in CATEGORY_ORDER if categorized[c]
                )
            ),
            color=0x00BCD4
        )
        await msg.edit(content=None, embed=embed)

    # ── Clean command (remove non-template roles) ───────────────────────

    @commands.command(name="cleanroles")
    @commands.has_permissions(manage_roles=True)
    async def clean_roles(self, ctx: commands.Context):
        """Delete roles that are NOT in the template (unused/junk roles)."""
        guild = ctx.guild
        msg = await ctx.send("🧹 **Scanning for non-template roles to remove…**")

        template_names = {t["name"] for t in ROLE_TEMPLATES}
        bot_top = guild.me.top_role
        removed: list[str] = []
        kept: list[str] = []

        for role in sorted(guild.roles, key=lambda r: -r.position):
            if role.is_default() or _is_bot_role(role) or role == bot_top:
                continue
            if role >= bot_top:
                kept.append(role.name)
                continue
            if role.name in template_names:
                continue

            try:
                await role.delete(reason="[CleanRoles] Non-template role removed")
                removed.append(role.name)
                await asyncio.sleep(0.3)
            except Exception as e:
                logger.warning(f"Could not delete {role.name}: {e}")

        embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║       🧹  CLEANUP COMPLETE!          ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=0x00BCD4
        )
        embed.add_field(
            name="📊 Summary",
            value=(
                f"🗑️ **Removed:** {len(removed)} non-template roles\n"
                f"📋 **Remaining:** {len(guild.roles) - 1} roles"
            ),
            inline=False
        )
        if removed:
            embed.add_field(
                name="🗑️ Deleted Roles",
                value="\n".join(f"• `{n}`" for n in removed[:20]) + ("…" if len(removed) > 20 else ""),
                inline=False
            )
        else:
            embed.add_field(name="✅ All Clear", value="No non-template roles found!", inline=False)

        await msg.edit(content=None, embed=embed)

    # ── Analyze command ─────────────────────────────────────────────────

    @commands.command(name="analyze")
    @commands.has_permissions(manage_roles=True)
    async def analyze_roles(self, ctx: commands.Context):
        guild = ctx.guild
        total = len(guild.roles) - 1
        members_with_roles = sum(1 for m in guild.members if len(m.roles) > 1)
        template_names = {t["name"] for t in ROLE_TEMPLATES}

        non_template = [r for r in guild.roles if not r.is_default() and r.name not in template_names and not _is_bot_role(r)]
        empty_roles = [r for r in guild.roles if not r.is_default() and len(r.members) == 0 and not _is_bot_role(r)]

        embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║       🧠  ROLE ANALYSIS REPORT       ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=0x5865F2
        )
        embed.add_field(
            name="📊 Server Overview",
            value=(
                f"**Guild:** {guild.name}\n"
                f"**Total Roles:** {total}\n"
                f"**Members with Roles:** {members_with_roles}/{guild.member_count}\n"
                f"**Role Usage:** `{_fancy_bar(members_with_roles, guild.member_count)}` "
                f"{round(members_with_roles / max(guild.member_count, 1) * 100)}%"
            ),
            inline=False
        )
        issues = []
        if non_template:
            issues.append(f"⚠️ **{len(non_template)} non-template** roles exist (run `.cleanroles` to purge)")
        if empty_roles:
            issues.append(f"🗑️ **{len(empty_roles)} empty** roles detected")
        if not issues:
            issues.append("✅ Roles look clean — all match templates!")

        embed.add_field(name="🔍 Issues", value="\n".join(issues), inline=False)

        if non_template:
            embed.add_field(
                name="⚠️ Non-Template Roles",
                value="\n".join(f"• `{r.name}`" for r in non_template[:12]) + ("…" if len(non_template) > 12 else ""),
                inline=False
            )
        embed.set_footer(text="Run .nukebuild to do a complete fresh rebuild")
        await ctx.send(embed=embed)

    # ── Role Guide ──────────────────────────────────────────────────────

    @commands.command(name="roleguide")
    async def role_guide(self, ctx: commands.Context):
        template_map = {t["name"]: t["category"] for t in ROLE_TEMPLATES}

        embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔══════════════════════════════════════╗\n"
                "║       📖  SERVER ROLE GUIDE          ║\n"
                "╚══════════════════════════════════════╝\n"
                "```"
            ),
            color=0x5865F2
        )
        for cat in CATEGORY_ORDER:
            roles_in_cat = [r for r in ctx.guild.roles if template_map.get(r.name) == cat]
            if roles_in_cat:
                label = CATEGORY_LABELS[cat]
                embed.add_field(
                    name=f"{label} ({len(roles_in_cat)})",
                    value=" ".join(r.mention for r in roles_in_cat[:6]) + ("…" if len(roles_in_cat) > 6 else ""),
                    inline=False
                )
        embed.set_footer(text=f"{ctx.guild.name}  •  Roles sorted highest → lowest authority")
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    # ── Rollback ────────────────────────────────────────────────────────

    @commands.command(name="rollback")
    @commands.has_permissions(administrator=True)
    async def rollback(self, ctx: commands.Context):
        embed = discord.Embed(
            description=(
                "```\n"
                "╔════════════════════════════════╗\n"
                "║   ⏪  ROLLBACK INITIATED...    ║\n"
                "╚════════════════════════════════╝\n"
                "```\n"
                "Restoring all roles from last backup…"
            ),
            color=0xFF9900
        )
        msg = await ctx.send(embed=embed)
        success, result_msg = await restore_backup(ctx.guild, ctx.guild.me)
        result_embed = discord.Embed(
            title="⏪ Rollback Complete" if success else "❌ Rollback Failed",
            description=result_msg,
            color=0x00E676 if success else 0xFF3860
        )
        result_embed.set_footer(text="All role data has been restored from your last backup snapshot")
        await msg.edit(embed=result_embed)

    # ── Assign owner command ────────────────────────────────────────────

    @commands.command(name="assignowner")
    @commands.has_permissions(administrator=True)
    async def assign_owner(self, ctx: commands.Context):
        guild = ctx.guild
        owner_template = next((t for t in ROLE_TEMPLATES if t.get("auto_assign_owner")), None)
        if not owner_template:
            await ctx.send("❌ No owner template found.")
            return

        role = discord.utils.get(guild.roles, name=owner_template["name"])
        if not role:
            await ctx.send("❌ Owner role doesn't exist yet — run `.nukebuild` first.")
            return

        if guild.owner and role not in guild.owner.roles:
            try:
                await guild.owner.add_roles(role, reason="[AssignOwner] Manual owner assignment")
            except Exception as e:
                await ctx.send(f"❌ Could not assign: `{e}`")
                return

        embed = discord.Embed(
            title="♛ Server Owner Role",
            description=(
                "```\n"
                "  ╔═══════════════════════════╗\n"
                "  ║   ♛  OWNER ROLE UPDATE    ║\n"
                "  ╚═══════════════════════════╝\n"
                "```\n"
                f"Role **{role.name}** is assigned to {guild.owner.mention}."
            ),
            color=0xFFD700
        )
        embed.add_field(name="Role", value=role.mention, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(RoleManager(bot))
