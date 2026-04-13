import discord

MEMBER_PERMS = discord.Permissions(
    send_messages=True, read_message_history=True, add_reactions=True,
    connect=True, speak=True
)
REGULAR_PERMS = discord.Permissions(
    send_messages=True, read_message_history=True, add_reactions=True,
    embed_links=True, attach_files=True, use_external_emojis=True,
    connect=True, speak=True
)

ROLE_TEMPLATES = [
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ♛  OWNER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "♛ Server Owner",
        "color": 0xFFD700,
        "hoist": True,
        "mentionable": True,
        "permissions": discord.Permissions(administrator=True),
        "category": "owner",
        "auto_assign_owner": True,
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ✦  ADMINISTRATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "✦ Administrator",
        "color": 0xFFC200,
        "hoist": True,
        "mentionable": True,
        "permissions": discord.Permissions(administrator=True),
        "category": "admin",
    },
    {
        "name": "✧ Co-Administrator",
        "color": 0xE8B400,
        "hoist": True,
        "mentionable": True,
        "permissions": discord.Permissions(
            manage_guild=True, manage_roles=True, manage_channels=True,
            kick_members=True, ban_members=True, manage_messages=True,
            view_audit_log=True, mention_everyone=True, manage_webhooks=True,
            manage_emojis=True
        ),
        "category": "admin",
    },
    {
        "name": "⚜ Server Manager",
        "color": 0xD4AC0D,
        "hoist": True,
        "mentionable": True,
        "permissions": discord.Permissions(
            manage_guild=True, manage_roles=True, manage_channels=True,
            kick_members=True, ban_members=True, manage_messages=True,
            view_audit_log=True, manage_webhooks=True
        ),
        "category": "admin",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ✧  MODERATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "⚡ Head Moderator",
        "color": 0xFF4500,
        "hoist": True,
        "mentionable": True,
        "permissions": discord.Permissions(
            kick_members=True, ban_members=True, manage_messages=True,
            mute_members=True, deafen_members=True, move_members=True,
            view_audit_log=True, manage_channels=True, mention_everyone=True
        ),
        "category": "mod",
    },
    {
        "name": "✩ Senior Moderator",
        "color": 0xFF6347,
        "hoist": True,
        "mentionable": True,
        "permissions": discord.Permissions(
            kick_members=True, ban_members=True, manage_messages=True,
            mute_members=True, deafen_members=True, move_members=True,
            view_audit_log=True
        ),
        "category": "mod",
    },
    {
        "name": "✧ Moderator",
        "color": 0xFF7F50,
        "hoist": True,
        "mentionable": True,
        "permissions": discord.Permissions(
            kick_members=True, manage_messages=True,
            mute_members=True, move_members=True, view_audit_log=True
        ),
        "category": "mod",
    },
    {
        "name": "⟡ Junior Moderator",
        "color": 0xFFA07A,
        "hoist": True,
        "mentionable": True,
        "permissions": discord.Permissions(
            manage_messages=True, mute_members=True, move_members=True
        ),
        "category": "mod",
    },
    {
        "name": "☄ Trial Moderator",
        "color": 0xFFB6A3,
        "hoist": False,
        "mentionable": True,
        "permissions": discord.Permissions(manage_messages=True, mute_members=True),
        "category": "mod",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ⟡  BOTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "⟡ Bot Manager",
        "color": 0x7289DA,
        "hoist": True,
        "mentionable": False,
        "permissions": discord.Permissions(
            manage_roles=True, manage_webhooks=True, manage_channels=True,
            manage_messages=True, send_messages=True, embed_links=True,
            attach_files=True, read_message_history=True
        ),
        "category": "bot",
    },
    {
        "name": "⟡ Bots",
        "color": 0x5865F2,
        "hoist": True,
        "mentionable": False,
        "permissions": discord.Permissions(
            send_messages=True, embed_links=True, attach_files=True,
            read_message_history=True, use_external_emojis=True, add_reactions=True
        ),
        "category": "bot",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ♛  ROYALTY / FANTASY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "♛ Queen",
        "color": 0xFF69B4,
        "hoist": True,
        "mentionable": True,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "♚ King",
        "color": 0x8B0000,
        "hoist": True,
        "mentionable": True,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "✦ Princess",
        "color": 0xFFB7C5,
        "hoist": False,
        "mentionable": True,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "♝ Bishop",
        "color": 0x6A0DAD,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "♞ Knight",
        "color": 0x708090,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "♜ Rook",
        "color": 0x4A4A4A,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "royalty",
    },
    {
        "name": "༄ Fairy",
        "color": 0xFFAEDD,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "⟡ Mermaid",
        "color": 0x00CED1,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "❂ Dragon Tamer",
        "color": 0xFF4500,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "⌘ Wizard",
        "color": 0x483D8B,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "⚔ Warrior",
        "color": 0xB22222,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },
    {
        "name": "🏹 Archer",
        "color": 0x556B2F,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "royalty",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ✺  VIP & SPECIAL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "♡ Server Booster",
        "color": 0xFF73FA,
        "hoist": True,
        "mentionable": True,
        "permissions": REGULAR_PERMS,
        "category": "vip",
    },
    {
        "name": "✦ Server Legend",
        "color": 0xFFD700,
        "hoist": True,
        "mentionable": True,
        "permissions": REGULAR_PERMS,
        "category": "vip",
    },
    {
        "name": "✺ VIP",
        "color": 0xE040FB,
        "hoist": True,
        "mentionable": True,
        "permissions": REGULAR_PERMS,
        "category": "vip",
    },
    {
        "name": "✸ Elite Member",
        "color": 0xAB47BC,
        "hoist": False,
        "mentionable": True,
        "permissions": REGULAR_PERMS,
        "category": "vip",
    },
    {
        "name": "⚝ Starborn",
        "color": 0xCE93D8,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "vip",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🎨  TALENT / SKILL ROLES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "✹ Artist",
        "color": 0xFF6B6B,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "♡ Singer",
        "color": 0xFF85C0,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "✧ Writer",
        "color": 0x6495ED,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "✺ Rapper",
        "color": 0x9400D3,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "❉ DJ",
        "color": 0x1E90FF,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "❋ Musician",
        "color": 0x228B22,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "༻ Storyteller",
        "color": 0xDC143C,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "⌬ Designer",
        "color": 0xFF8C00,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "⌗ Coder",
        "color": 0x00FF7F,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "❈ Content Creator",
        "color": 0xFFA500,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "✭ Performer",
        "color": 0xFF1493,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },
    {
        "name": "⌁ Photographer",
        "color": 0x708090,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "talent",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 📈  PROGRESSION (Noob → Mythic)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "♛ Mythic",
        "color": 0xFF0000,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "progression",
    },
    {
        "name": "❂ Diamond",
        "color": 0xB9F2FF,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "progression",
    },
    {
        "name": "✺ Legend",
        "color": 0xFF4500,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "progression",
    },
    {
        "name": "✹ Expert",
        "color": 0x1E90FF,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "progression",
    },
    {
        "name": "✸ Pro",
        "color": 0x32CD32,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "progression",
    },
    {
        "name": "✷ Rising Star",
        "color": 0x87CEEB,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "progression",
    },
    {
        "name": "✶ Noob",
        "color": 0xD3D3D3,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "progression",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ❖  LEVEL SYSTEM
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "❖ Level 100",
        "color": 0xFF1744,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "level",
    },
    {
        "name": "❖ Level 75",
        "color": 0xFF5252,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "level",
    },
    {
        "name": "❖ Level 50",
        "color": 0xFF6E40,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "level",
    },
    {
        "name": "❖ Level 25",
        "color": 0xFFAB40,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "level",
    },
    {
        "name": "❖ Level 10",
        "color": 0xFFD740,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "level",
    },
    {
        "name": "❖ Level 5",
        "color": 0xFFFF00,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "level",
    },
    {
        "name": "❖ Newcomer",
        "color": 0xE6EE9C,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "level",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ☁  VOICE ROLES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "☁ Active Voice",
        "color": 0x4FC3F7,
        "hoist": False,
        "mentionable": False,
        "permissions": discord.Permissions(
            connect=True, speak=True, stream=True,
            use_voice_activation=True, send_messages=True, read_message_history=True
        ),
        "category": "voice",
    },
    {
        "name": "☁ Private VC Owner",
        "color": 0x29B6F6,
        "hoist": False,
        "mentionable": False,
        "permissions": discord.Permissions(
            connect=True, speak=True, stream=True, move_members=True,
            mute_members=True, deafen_members=True, manage_channels=True,
            send_messages=True, read_message_history=True
        ),
        "category": "voice",
    },
    {
        "name": "☁ Gaming VC",
        "color": 0x039BE5,
        "hoist": False,
        "mentionable": False,
        "permissions": discord.Permissions(
            connect=True, speak=True, stream=True,
            use_voice_activation=True, send_messages=True, read_message_history=True
        ),
        "category": "voice",
    },
    {
        "name": "☁ Chill VC",
        "color": 0x0277BD,
        "hoist": False,
        "mentionable": False,
        "permissions": discord.Permissions(
            connect=True, speak=True, use_voice_activation=True,
            send_messages=True, read_message_history=True
        ),
        "category": "voice",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ♡  FRIENDS ROLES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "♡ Best Friend",
        "color": 0xFF69B4,
        "hoist": False,
        "mentionable": True,
        "permissions": REGULAR_PERMS,
        "category": "friends",
    },
    {
        "name": "✩ Homie",
        "color": 0xFFA500,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "friends",
    },
    {
        "name": "✪ Squad",
        "color": 0x00FF7F,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "friends",
    },
    {
        "name": "∞ Ride or Die",
        "color": 0xFF1493,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "friends",
    },
    {
        "name": "➤ Party Starter",
        "color": 0xFFD700,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "friends",
    },
    {
        "name": "༒ Comedian",
        "color": 0xFF6347,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "friends",
    },
    {
        "name": "≋ Chatterbox",
        "color": 0x00CED1,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "friends",
    },
    {
        "name": "⌁ Silent One",
        "color": 0x696969,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "friends",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ♡  COMMUNITY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "☼ Early Bird",
        "color": 0xFFF176,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "☽ Night Owl",
        "color": 0x7E57C2,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "♡ Friendly",
        "color": 0xF48FB1,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "∞ Loyal",
        "color": 0x80CBC4,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "➤ Regular",
        "color": 0x81C784,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "✪ Veteran",
        "color": 0x4DB6AC,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "community",
    },
    {
        "name": "✫ Trusted",
        "color": 0x26A69A,
        "hoist": False,
        "mentionable": False,
        "permissions": REGULAR_PERMS,
        "category": "community",
    },
    {
        "name": "⸷ Helper",
        "color": 0x00897B,
        "hoist": False,
        "mentionable": True,
        "permissions": discord.Permissions(
            send_messages=True, add_reactions=True, embed_links=True,
            attach_files=True, read_message_history=True, manage_messages=True
        ),
        "category": "community",
    },
    {
        "name": "༄ Supporter",
        "color": 0x00796B,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "✹ Enthusiast",
        "color": 0x00695C,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "➣ Pioneer",
        "color": 0x558B2F,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "➜ Explorer",
        "color": 0x689F38,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },
    {
        "name": "❋ Wildcard",
        "color": 0x8D6E63,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "community",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ✮  COSMIC / COOL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "✮ Stardust",
        "color": 0xB39DDB,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "✯ Shooting Star",
        "color": 0x9575CD,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "✭ Supernova",
        "color": 0x7E57C2,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "✬ Quantum",
        "color": 0x673AB7,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "❂ Solar",
        "color": 0xFF8F00,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "❈ Crystal",
        "color": 0x80DEEA,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "❊ Nebula",
        "color": 0xCE93D8,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "☾ Moonchild",
        "color": 0xB0BEC5,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "⚘ Bloom",
        "color": 0xF06292,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "≋ Ripple",
        "color": 0x4DD0E1,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "≈ Wavelength",
        "color": 0x26C6DA,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "⚚ Alchemist",
        "color": 0xA5D6A7,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "✯ Galaxy Brain",
        "color": 0x7B2FBE,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "≀ Shapeshifter",
        "color": 0xFF6B9D,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },
    {
        "name": "⚝ Aura",
        "color": 0xFFE4B5,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "cool",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ⌁  WILD CARDS / CRAZY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "⌁ Glitch",
        "color": 0x00FF41,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "𓆩 Ancient One",
        "color": 0xD4AC0D,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "༒ Chaos Agent",
        "color": 0xFF0000,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "༻ Harmony",
        "color": 0x76FF03,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "✸ Spark",
        "color": 0xFFEA00,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "⚡ Thunderclap",
        "color": 0xFFFF00,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "𓆩♡𓆪 Heartbeam",
        "color": 0xFF4081,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "⚝ Comet Rider",
        "color": 0x69FFFA,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "☄ Cosmic Drift",
        "color": 0xBB86FC,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "❉ Vortex",
        "color": 0x03DAC6,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "⌗ Phantom",
        "color": 0x37474F,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "☁ Cloudburst",
        "color": 0x90CAF9,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "⌘ Time Traveler",
        "color": 0x00FFFF,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "❖ Void Walker",
        "color": 0x1A1A2E,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "⚚ Sorcerer",
        "color": 0x800080,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "≋ Surge",
        "color": 0xFF6D00,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "✷ Static",
        "color": 0x69F0AE,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "✶ Atom",
        "color": 0x40C4FF,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "∞ Eternal",
        "color": 0xE040FB,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "≈ Surfer",
        "color": 0x00BFFF,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "⚘ Cactus",
        "color": 0x228B22,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "𓆪 Duck",
        "color": 0xFFFF00,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "𓆩 Frog Gang",
        "color": 0x00CC44,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "☼ Sunbeam",
        "color": 0xFFFF00,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "⌁ Glitch Lord",
        "color": 0xFF00FF,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },
    {
        "name": "❖ Pizza Lord",
        "color": 0xFF8C00,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "crazy",
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ➤  MEMBERS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "name": "➤ Member",
        "color": 0x9E9E9E,
        "hoist": False,
        "mentionable": False,
        "permissions": MEMBER_PERMS,
        "category": "member",
    },
]

CATEGORY_ORDER = [
    "owner", "admin", "mod", "bot", "royalty", "vip",
    "talent", "progression", "level", "voice",
    "friends", "community", "cool", "crazy", "member"
]

CATEGORY_LABELS = {
    "owner":       "♛ Server Owner",
    "admin":       "✦ Administration",
    "mod":         "✧ Moderation",
    "bot":         "⟡ Bots",
    "royalty":     "♛ Royalty & Fantasy",
    "vip":         "✺ VIP & Special",
    "talent":      "🎨 Talent & Skills",
    "progression": "📈 Progression",
    "level":       "❖ Level System",
    "voice":       "☁ Voice",
    "friends":     "♡ Friends",
    "community":   "✩ Community",
    "cool":        "✮ Cosmic",
    "crazy":       "⌁ Wild Cards",
    "member":      "➤ Members",
}

CATEGORY_COLORS = {
    "owner":       0xFFD700,
    "admin":       0xFFC200,
    "mod":         0xFF4500,
    "bot":         0x5865F2,
    "royalty":     0xFF69B4,
    "vip":         0xE040FB,
    "talent":      0xFF6B6B,
    "progression": 0x32CD32,
    "level":       0xFF1744,
    "voice":       0x4FC3F7,
    "friends":     0xFF69B4,
    "community":   0x26A69A,
    "cool":        0x9575CD,
    "crazy":       0x00FF41,
    "member":      0x9E9E9E,
}
