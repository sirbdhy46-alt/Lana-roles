import discord
from discord.ext import commands
from utils.logger import setup_logger

logger = setup_logger("VoiceSystem")

VC_ROLES = [
    {"name": "☁ Active Voice",      "color": 0x4FC3F7},
    {"name": "☁ Private VC Owner",  "color": 0x29B6F6},
    {"name": "☁ Gaming VC",         "color": 0x039BE5},
    {"name": "☁ Chill VC",          "color": 0x0277BD},
]


class VoiceSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="setupvc")
    @commands.has_permissions(manage_roles=True)
    async def setup_vc(self, ctx: commands.Context):
        guild = ctx.guild
        created = []
        for data in VC_ROLES:
            existing = discord.utils.get(guild.roles, name=data["name"])
            if existing:
                continue
            try:
                await guild.create_role(
                    name=data["name"],
                    color=discord.Color(data["color"]),
                    hoist=False,
                    mentionable=False,
                    permissions=discord.Permissions(
                        connect=True, speak=True, stream=True, use_voice_activation=True
                    ),
                    reason="[AutoSetup] VC role"
                )
                created.append(data["name"])
            except Exception as e:
                logger.error(f"Error creating VC role {data['name']}: {e}")

        embed = discord.Embed(
            title="🎤 VC Roles Setup",
            color=0x4FC3F7,
            description=(
                f"**{len(created)}** VC roles created:\n" +
                "\n".join(f"• {n}" for n in created) if created else "All VC roles already exist!"
            )
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        active_role = discord.utils.get(member.guild.roles, name="☁ Active Voice")
        if not active_role:
            return

        try:
            if after.channel and not before.channel:
                await member.add_roles(active_role, reason="[VoiceSystem] Joined VC")
            elif not after.channel and before.channel:
                await member.remove_roles(active_role, reason="[VoiceSystem] Left VC")
        except Exception as e:
            logger.warning(f"Voice role update failed for {member}: {e}")


def setup(bot: commands.Bot):
    bot.add_cog(VoiceSystem(bot))
