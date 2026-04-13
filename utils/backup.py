import json
import discord
from utils.logger import setup_logger

logger = setup_logger("Backup")

backups: dict[int, dict] = {}

async def create_backup(guild: discord.Guild) -> dict:
    backup = {
        "guild_id": guild.id,
        "guild_name": guild.name,
        "roles": []
    }

    for role in guild.roles:
        if role.is_default():
            continue
        backup["roles"].append({
            "id": role.id,
            "name": role.name,
            "color": role.color.value,
            "hoist": role.hoist,
            "mentionable": role.mentionable,
            "permissions": role.permissions.value,
            "position": role.position,
            "members": [m.id for m in role.members]
        })

    backup["roles"].sort(key=lambda r: r["position"])
    backups[guild.id] = backup
    logger.info(f"Backup created for guild {guild.name} ({len(backup['roles'])} roles)")
    return backup


async def restore_backup(guild: discord.Guild, bot_member: discord.Member) -> tuple[bool, str]:
    if guild.id not in backups:
        return False, "No backup found for this server."

    backup = backups[guild.id]
    bot_top = bot_member.top_role.position

    existing_roles = {r.id: r for r in guild.roles}

    for role_data in backup["roles"]:
        role = existing_roles.get(role_data["id"])
        try:
            if role:
                await role.edit(
                    name=role_data["name"],
                    color=discord.Color(role_data["color"]),
                    hoist=role_data["hoist"],
                    mentionable=role_data["mentionable"],
                    permissions=discord.Permissions(role_data["permissions"]),
                    reason="[Rollback] Restoring from backup"
                )
            else:
                role = await guild.create_role(
                    name=role_data["name"],
                    color=discord.Color(role_data["color"]),
                    hoist=role_data["hoist"],
                    mentionable=role_data["mentionable"],
                    permissions=discord.Permissions(role_data["permissions"]),
                    reason="[Rollback] Recreating from backup"
                )
        except discord.Forbidden:
            logger.warning(f"No permission to restore role: {role_data['name']}")
        except Exception as e:
            logger.error(f"Error restoring role {role_data['name']}: {e}")

    logger.info(f"Rollback completed for guild {guild.name}")
    return True, "Rollback complete. All roles restored from backup."

