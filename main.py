import discord, datetime
from asyncio import sleep
import os
import keep_alive

channel_id = CHANNEL_ID

class Client(discord.Client):
    active = True

    async def pauseBump(self):
        self.active = False
        print("Bump paused.")

    async def clean(self, user_message=None, bot_message=None):
        await sleep(3)
        if user_message is not None:
            await user_message.delete()
        if bot_message is not None:
            await bot_message.delete()
        print("Chat cleaned.")

    async def continueBump(self):
        self.active = True
        print("Bump restored.")

    async def send(self, ctx, content):
        message = await ctx.channel.send(f"{ctx.author.mention} {content}")
        print(f"Sent '{content}' to '{ctx.author}'")
        await self.clean(ctx, message)

    async def bumpCheck(self):
        channel = self.get_channel(channel_id)
        async for message in channel.history(limit=50):
            if str(message.author) == "DISBOARD#2760":
                if "Bump done" in message.embeds[0].description:
                    now = datetime.datetime.utcnow()
                    two = datetime.timedelta(hours=2)
                    min = datetime.timedelta(minutes=1)

                    difference = now - message.created_at
                    difference = two - difference + min
                    print(f"Time until next bump {difference}")

                    return difference.seconds
                    break

    async def bump(self):
        self.diff = await self.bumpCheck()
        await sleep(self.diff)
        channel = self.get_channel(channel_id)
        command = await channel.send("!d bump")
        print("Server bumped")
        return command

    async def on_ready(self):
        print(f"Logged as {self.user}")
        while self.active == True:
            command = await self.bump()
            await self.clean(command)

    async def on_message(self, message):
        if message.author == self.user:
            if message.content == "!pause":
                await self.pauseBump()
                await self.send(message, "Bot is paused :sleeping:")

            elif message.content == "!continue":
                await self.continueBump()
                await self.send(
                    message,
                    f"Bump is activated, next bump in {self.diff} seconds :hourglass_flowing_sand:",
                )

keep_alive.keep_alive()
Client().run(os.getenv("TOKEN"), bot=False)
