import asyncio
import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='?',intents=intents)
token = os.getenv("DISCORD_ROLE_ORGANIZER_BOT_TOKEN")

# https://discordpy.readthedocs.io/en/latest/api.html#discord.on_guild_role_create
@bot.event
async def on_guild_role_create(new_role):
    #print('on_guild_role_create ' + bot.user.name)
    await asyncio.sleep(3)
    #find alphabetical position this role should appear in.
    server_role_list = sorted(new_role.guild.roles, key=lambda x:x.name.lower())
    #ignore bot roles for where we insert. They should always be on
    server_role_list = list(filter(lambda x: not x.managed and x.name != "@everyone", server_role_list))
    #never allow anything to be above position admin. higher number means higher position in list.
    #also 0 is reservered for "everyone"
    len_sortable_roles = len(server_role_list)
    new_role_index = min(max(len_sortable_roles - server_role_list.index(new_role),1), len_sortable_roles)
    #colors copied from discord ui
    default_colors = [int("0x1ABC9C",16), int("0x2ECC71",16), int("0x3498DB",16), int("0x9B59B6",16),
                      int("0x9B59B6",16), int("0xC27C0E",16),int("0xE67E22",16), int("0xE67E22",16),
                      int("0x95A5A6",16), int("0x607D8B",16)]
    await new_role.edit(hoist=True, position=new_role_index, colour=default_colors[random.randrange(0,len(default_colors))])

#snarky reply for feature requests
@bot.command(name="botpr")
async def botpr(ctx):
    await ctx.send(f"Now accepting PRs for new features at https://github.com/MollyJameson/RoleOrganizerHelperBot !")


bot.run(token)
