import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix = 'c;', intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb)
    print('Cat Peach 2 - Anime Chica is online')

@client.event
async def on_member_join(member):
    with open('guilds.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    channel_id = guilds_dict[str(member.guild.id)]
    embed = discord.Embed(title=f"MEMBER JOIN | {member.guild.name}", description=f"**{member.mention}** has joined the server. Hope they enjoy their stay here.", color=(65280))
    embed.set_thumbnail(url=member.avatar)
    embed.set_footer(text="Service provided by Boomerang Rosalina Development.")
    await client.get_channel(int(channel_id)).send(embed=embed)
    if member.guild.id in client.verification:
        guild = member.guild
        role = discord.utils.get(guild.roles, name='Unverified')
        await member.add_roles(role)
    
        embed2 = discord.Embed(title="HI THERE", description=f"Welcome **{member.name}** to **{member.guild.name}**", color=(3140255))
        embed2.add_field(name="How to access the server?", value="In order to access the rest of the server, head to the verify channel and type in **c;verify** with me. If Send Messages permission is off, follow the server instructions to verify yourself.", inline=False)
        embed2.add_field(name="I am having issues verifying myself", value="If you are having issues verifying yourself, Please message a Server Admin", inline=False)
        embed.set_footer(text="Service provided by Boomerang Rosalina Development.")
        await member.send(embed=embed2)

@client.event
async def on_member_remove(member):
    with open('guilds.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    channel_id = guilds_dict[str(member.guild.id)]
    embed = discord.Embed(title=f"MEMBER LEAVE | {member.guild.name}", description=f"**{member.name}** has left the server. How sad", color=(16711680))
    await client.get_channel(int(channel_id)).send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass
    else:
        with open('reactionroles.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == payload.message_id:
                                                           
                    if x['emoji'] == payload.emoji.name:
                        role = discord.utils.get(client.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    with open('reactionroles.json') as react_file:
        data = json.load(react_file)
        for x in data:

            if x['message_id'] == payload.message_id:
                                                        
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])
                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)





@client.command()
async def help(ctx):
    embed = discord.Embed(title="Anime Chica", description="MY PREFIX IS: **c;**", color=(16744191))
    embed.add_field(name="General Commands", value="c;help - This message\nc;botinfo - View information about me\nc;ping - Checks my Latency", inline=False)
    embed.add_field(name="Utility", value="c;say - Make me say stuff\nc;esay - Makes me say stuff in a embed\nc;verify - Verifys the user by removing the Unverified role.\nc;dice - Rolls a 1-6 dice", inline=False)
    embed.add_field(name="Settings", value="c;setwchannel - Set the Welcome logs channel for the server.\nc;reactionrole - Set up a Reaction role message", inline=False)
    embed.add_field(name="Developer Commands", value="c;restart - Restarts the bot", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def botinfo(ctx):
    embed = discord.Embed(title="ANIME CHICA BOT INFO", description="Below you can see more information about me.", color=(16744191))
    embed.add_field(name="General Information", value="Prefix: c;", inline=False)
    embed.add_field(name="Developers", value="Boomerang Mario#5018\nLLoC Eagle Fan Art#1681", inline=False)
    embed.add_field(name="Links", value="Invite the Bot: https://discord.com/api/oauth2/authorize?client_id=995207277286015018&permissions=0&scope=bot\nSupport Server: https://discord.gg/58rnKWTneu\nWebsite: https://animechica.glitch.me/", inline=False)
    embed.add_field(name="Legal", value="Privacy: https://animechica.glitch.me/privacy.html", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'PONG! My Latency is: {round(client.latency * 1000)}ms')

@client.command()
async def say(ctx, *, question: commands.clean_content):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error

@client.command()
async def esay(ctx, *, question):
    embed = discord.Embed(description=f'{question}', color=(16744191))
    await ctx.send(embed=embed)
    await ctx.message.delete()

@esay.error
async def esay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error
    else:
        raise error

@client.command()
async def dice(ctx):
    responses = ["1",
                 "2",
                 "3",
                 "4",
                 "5",
                 "6"]
    await ctx.send(f'{random.choice(responses)}')





@client.command()
@commands.has_permissions(manage_guild=True)
async def setwchannel(ctx, channel: discord.TextChannel):
    with open('guilds.json', 'r', encoding='utf-8') as f:
        guilds_dict = json.load(f)

    guilds_dict[str(ctx.guild.id)] = str(channel.id)
    with open('guilds.json', 'w', encoding='utf-8') as f:
        json.dump(guilds_dict, f, indent=4, ensure_ascii=False)
    
    await ctx.send(f'Set welcome channel for **{ctx.guild.name}** to **{channel.name}**')

@client.command()
async def verify(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Unverified")
    if not role:
        await ctx.send("To use this feature, you need a role called **Unverified**")
        return
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send("YOU HAVE BEEN VERIFIED AND HAVE ACCESS TO THE REST OF THE SERVER.")
        embed = discord.Embed(title="SUCCESSFULLY VERIFIED", description=f"Thank you for verifying yourself into: **{ctx.guild.name}**. You now have access to the rest of the server. Be sure to read the rules channel as well and don't forget to have fun.", color=(65535))
        await ctx.author.send(embed=embed)
        return
    else:
        await ctx.send("YOU ARE ALREADY VERIFIED IN THE SERVER. No need to rerun this command.")
        return

@client.command()
@commands.bot_has_permissions(manage_roles=True)
@commands.has_permissions(manage_roles=True)
async def reactionrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactionroles.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactionroles.json', 'w') as f:
        json.dump(data, f, indent=4)

@setwchannel.error
async def setwchannel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('YOU NEED TO HAVE THE **MANAGE_GUILD** PERMISSION TO USE THIS COMMAND')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("RERUN THIS COMMAND AGAIN but this time, Mention the text channel you want the bot to send it's logs too.")
    else:
        raise error

@reactionrole.error
async def reactionrole_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I NEED THE ``MANAGE_ROLES`` PERMISSION TO CONTINUE")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('YOU NEED TO HAVE THE **MANAGE_ROLES** PERMISSION TO USE THIS COMMAND')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("RERUN THIS COMMAND AGAIN but this time, Please input the correct arguments: c;reactionrole <emoji> <role mention> <Message>")
    else:
        raise error





client.run("BOTTOKENHERE")
