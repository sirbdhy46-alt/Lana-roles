import discord
from discord.ext import commands
from discord import ui
from utils.logger import setup_logger

logger = setup_logger("TicketSystem")

TICKET_CATEGORIES = {
    "support": {"label": "🛠️ Support",     "emoji": "🛠️", "color": 0x5865F2, "desc": "General server support"},
    "report":  {"label": "🚨 Report",      "emoji": "🚨", "color": 0xFF3860, "desc": "Report a user or issue"},
    "partner": {"label": "🤝 Partnership", "emoji": "🤝", "color": 0x00E676, "desc": "Partnership applications"},
    "help":    {"label": "❓ Help",        "emoji": "❓", "color": 0xFFD740, "desc": "Quick questions & help"},
    "appeal":  {"label": "⚖️ Appeal",      "emoji": "⚖️", "color": 0xAB47BC, "desc": "Ban or mute appeals"},
}


class TicketTypeSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=v["label"],
                value=k,
                emoji=v["emoji"],
                description=v["desc"]
            )
            for k, v in TICKET_CATEGORIES.items()
        ]
        super().__init__(
            placeholder="🎫  Select a ticket category…",
            options=options,
            min_values=1,
            max_values=1,
            custom_id="ticket_type_select"
        )

    async def callback(self, interaction: discord.Interaction):
        ticket_type = self.values[0]
        guild = interaction.guild
        user = interaction.user
        meta = TICKET_CATEGORIES[ticket_type]

        category_name = "━ 🎫 Tickets ━"
        cat_obj = discord.utils.get(guild.categories, name=category_name)
        if not cat_obj:
            try:
                cat_obj = await guild.create_category(
                    category_name,
                    reason="[TicketSystem] Auto-created ticket category"
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    "❌ I can't create the ticket category — missing permissions.", ephemeral=True
                )
                return

        channel_name = f"🎫│{user.name[:12]}-{ticket_type}"
        existing = discord.utils.get(guild.text_channels, name=channel_name)
        if existing:
            await interaction.response.send_message(
                f"⚠️ You already have an open ticket: {existing.mention}", ephemeral=True
            )
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(
                view_channel=True, send_messages=True,
                read_message_history=True, attach_files=True, embed_links=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True, send_messages=True,
                manage_channels=True, manage_messages=True, embed_links=True
            ),
        }

        mod_role = discord.utils.find(
            lambda r: r.permissions.manage_messages and not r.is_default() and not r.is_bot_managed(),
            guild.roles
        )
        if mod_role:
            overwrites[mod_role] = discord.PermissionOverwrite(
                view_channel=True, send_messages=True,
                manage_messages=True, read_message_history=True
            )

        try:
            channel = await guild.create_text_channel(
                name=channel_name,
                category=cat_obj,
                overwrites=overwrites,
                topic=f"{meta['label']} ticket opened by {user} ({user.id})",
                reason=f"[TicketSystem] Opened by {user}"
            )
        except discord.Forbidden:
            await interaction.response.send_message("❌ Can't create ticket channel.", ephemeral=True)
            return

        embed = discord.Embed(
            title="",
            description=(
                f"```\n"
                f"╔═══════════════════════════════════════╗\n"
                f"║    {meta['emoji']}  {meta['label'].upper():<33}║\n"
                f"╚═══════════════════════════════════════╝\n"
                f"```\n"
                f"Hey {user.mention}! 👋 A staff member will assist you shortly.\n\n"
                f"**📋 Ticket Info**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"**Type:** {meta['label']}\n"
                f"**Opened by:** {user.mention}\n"
                f"**Channel:** {channel.mention}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📝 Please **describe your issue** in detail below.\n"
                f"Our team will respond as soon as possible."
            ),
            color=meta["color"]
        )
        embed.set_footer(text="Use the button below to close this ticket when resolved")
        embed.set_thumbnail(url=user.display_avatar.url)

        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(
            f"✅ Ticket created! {channel.mention}", ephemeral=True
        )
        logger.info(f"Ticket opened: {channel.name} by {user}")


class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketTypeSelect())

    @ui.button(
        label="Open a Ticket",
        style=discord.ButtonStyle.blurple,
        emoji="🎫",
        custom_id="open_ticket_btn"
    )
    async def open_ticket_btn(self, button: ui.Button, interaction: discord.Interaction):
        pass


class CloseTicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒",
        custom_id="close_ticket_btn"
    )
    async def close_ticket(self, button: ui.Button, interaction: discord.Interaction):
        channel = interaction.channel
        embed = discord.Embed(
            title="🔒 Ticket Closed",
            description=(
                f"**Closed by:** {interaction.user.mention}\n"
                f"**Channel:** {channel.name}\n\n"
                "This ticket will be deleted in **5 seconds.**"
            ),
            color=0xFF3860
        )
        await channel.send(embed=embed)
        import asyncio
        await asyncio.sleep(5)
        try:
            await channel.delete(reason=f"[TicketSystem] Closed by {interaction.user}")
        except Exception:
            pass


class TicketSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ticketpanel")
    @commands.has_permissions(manage_channels=True)
    async def ticket_panel(self, ctx: commands.Context):
        embed = discord.Embed(
            title="",
            description=(
                "```\n"
                "╔═══════════════════════════════════════════╗\n"
                "║    🎫   S U P P O R T   C E N T E R      ║\n"
                "║         Open a ticket to get help         ║\n"
                "╚═══════════════════════════════════════════╝\n"
                "```\n"
                "**Need help? Select a category below to open a private ticket.**\n"
                "Our staff team will assist you as quickly as possible.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "🛠️ **Support** — General issues & questions\n"
                "🚨 **Report** — Report a player or problem\n"
                "🤝 **Partnership** — Apply for a partnership\n"
                "❓ **Help** — Quick help needed\n"
                "⚖️ **Appeal** — Contest a ban or mute\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "*Tickets are private — only you and staff can see them.*"
            ),
            color=0x5865F2
        )
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_footer(text=f"{ctx.guild.name}  •  Support Center  •  Response time: < 24h")
        await ctx.send(embed=embed, view=TicketView())
        try:
            await ctx.message.delete()
        except Exception:
            pass


def setup(bot: commands.Bot):
    bot.add_cog(TicketSystem(bot))
