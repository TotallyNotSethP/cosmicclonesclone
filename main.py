# WARNING: DEVELOPMENT VERSION

import discord
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
        print(f"DEBUG: {message.author} sent message \"{message.content}\"")
        roles = message.guild.roles
        if len(command) == 1:
            print(f"400 Bad Request: {message.author} sent `$getrole` command with no parameters.")
            await send("GETROLE USAGE: $getrole <role>")
            if len(roles) >= 1:
                await send("Availible Roles:")
                validroles = []
                for role in roles:
                    if role.name != "Admin" and role.name != "@everyone" and role.name != "CosmicClone's Clone":
                        validroles.append("* " + role.name)
                await send("\n".join(validroles))
            else:
                await send("No roles available.")
        else:
            role = " ".join(command[1:])
            if role == "Admin" or role == "CosmicClone's Clone":
                print(f"403 Forbidden: Admin access is not allowed for user \"{message.author}\" (requested role \"{role}\")")
                await send("PERMISSION DENIED: You're not allowed to have admin.")
            else:
                if role in [role.name for role in roles]:
                    await message.author.add_roles(discord.utils.get(message.guild.roles, name=role))
                    print(f"200 OK: \"{message.author}\" was given the role \"{role}\"")
                    await send("SUCCESS: You have been given the specified role.")
                else:
                    print(f"404 Not Found: Role \"{role}\" doesn't exist (requested by \"{message.author}\")")
                    await send("NOT FOUND: That role doesn't exist.")

client.run(environ["DISCORD_BOT_TOKEN"])