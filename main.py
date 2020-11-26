# WARNING: DEVELOPMENT VERSION

import discord
import webcolors
import asyncio
from os import environ

client = discord.Client()

@client.event
async def on_ready():
    print(f"DEBUG: {client.user} is now online.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = message.content.split(" ")
    send = message.channel.send

    if command[0] == "$getrole":
        print()
        print(f"DEBUG: \"{message.author}\" sent message \"{message.content}\"")
        roles = message.guild.roles
        if len(command) == 1:
            print(f"400 Bad Request: \"{message.author}\" sent `$getrole` command with no parameters")
            if len(roles) >= 1:
                validroles = []
                for role in roles:
                    if role.name != "Admin" and role.name != "@everyone" and role.name != "CosmicClone's Clone":
                        try:
                            int(role.name[1:], 16)
                        except Exception:
                            validroles.append("* " + role.name)
                await send("GETROLE USAGE: $getrole <role>\nAvailible Roles:\n" + "\n".join(validroles))
            else:
                await send("GETROLE USAGE: $getrole <role>\nNo roles available")
        else:
            role = " ".join(command[1:])
            if role == "Admin" or role == "CosmicClone's Clone":
                print(f"403 Forbidden: Admin access is not allowed for user \"{message.author}\" (requested role \"{role}\")")
                await send("PERMISSION DENIED: You're not allowed to have admin")
            else:
                if role in [role.name for role in roles]:
                    await message.author.add_roles(discord.utils.get(message.guild.roles, name=role))
                    print(f"200 OK: \"{message.author}\" was given the role \"{role}\"")
                    await send("SUCCESS: You have been given the specified role")
                else:
                    print(f"404 Not Found: Role \"{role}\" doesn't exist (requested by \"{message.author}\")")
                    await send("NOT FOUND: That role doesn't exist")
    elif command[0] == "$setcolor":
        print()
        print(f"DEBUG: \"{message.author}\" sent message \"{message.content}\"")
        try:
            color_name = command[1]
            try:
                color_hex = webcolors.name_to_hex(color_name)
                if discord.utils.get(message.guild.roles, name=color_hex) is None:
                    await message.guild.create_role(name=color_hex, colour=discord.Colour(int(color_hex[1:], 16)))
                role = discord.utils.get(message.guild.roles, name=color_hex)
                role_added = False
                while not role_added:
                    try:
                        await message.author.add_roles(role)
                        role_added = True
                    except AttributeError:
                        print("Tried assigning role... failed. Will try again in 0.1 sec.")
                        asyncio.sleep(0.1)
                await role.edit(position=len(message.guild.roles)-2)
                print(f"200 OK: \"{message.author}\" was given the color \"{color_name}\" (hex {color_hex})")
                await send(f"SUCCESS: You have been colored \"{color_name}\"")
            except ValueError:
                print(f"404 Not Found: Color \"{color_name}\" doesn't exist (requested by \"{message.author}\")")
                await send("NOT FOUND: That color doesn't exist in the database")
        except IndexError:
            print(f"400 Bad Request: {message.author} sent `$setcolor` command with no parameters.")
            await send("SETCOLOR USAGE: $setcolor <color_name>\nAny CSS3 color will work.\nIf you don't know what that means, too bad.")

client.run(environ["DISCORD_BOT_TOKEN"])