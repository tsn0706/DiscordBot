import os
import asyncio
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
discord_token = os.getenv("TOKEN")


#讀取json檔
with open("setting.json","r",encoding="utf8")as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = jdata["CommandPrefix"], intents = intents, application_id = 1178686244419551263)

@bot.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', bot.user)
    game = discord.Game('窩ㄞ咩咩 /咩指令')#暱稱欄位文字
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.online, activity=game)
    await bot.tree.sync()
    print('Synced commands to all servers')
    

@bot.event
async def on_command_error(ctx, error):#前綴輸入正確但指令錯誤時
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("無指令\n輸入: \" /咩指令 \" 了解更多噢")

# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(filename)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(discord_token)

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())


# ServerCogs = {}

# #讀取json檔
# with open("setting.json","r",encoding="utf8")as jfile:
#     jdata = json.load(jfile)

# intents = discord.Intents.all()
# bot = commands.Bot(command_prefix = jdata["CommandPrefix"], intents = intents)

# @bot.event
# #當機器人完成啟動時
# async def on_ready():
#     print('目前登入身份：', bot.user)
#     #暱稱欄位文字顯示正在玩的遊戲
#     game = discord.Game('窩ㄞ咩咩')
#     #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
#     await bot.change_presence(status=discord.Status.online, activity=game)

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         # 可以加入一個條件以區分是否為未知指令的錯誤
#         if isinstance(error, commands.CommandOnCooldown):
#             await ctx.send("此指令處於冷卻中，請稍後再試。")
#         else:
#             await ctx.send("無指令\n輸入: \" !咩指令 \" 了解更多噢")
#     # elif isinstance(error, commands.CheckFailure):
#         # await ctx.send("無管理權限")

# # 讓管理員才能觸發load
# # def Administrator(ctx):
# #     return ctx.author.id in jdata["AdministratorId"]

# # 載入指令
# @bot.command()
# # @commands.check(Administrator)
# async def load(ctx, extension):
#     if ctx.guild:# 限定輸入指令的伺服器才執行
#         ServerId = ctx.guild.id
#         if ServerId not in ServerCogs:
#             ServerCogs[ServerId] = {"LoadedCog" : set()}
#         if extension not in ServerCogs[ServerId]["LoadedCog"]:
#             try:
#                 bot.load_extension(f"cogs.{extension}")
#                 await ctx.send(f"Loaded {extension} done.")
#                 ServerCogs[ServerId]["LoadedCog"].add(extension)
#             except Exception as e:
#                 await ctx.send(f"Failed to load {extension}: {e}")
#         else:
#             await ctx.send(f"{extension} is already loaded.")

# # 卸載指令
# @bot.command()
# # @commands.check(Administrator)
# async def unload(ctx, extension):
#     if ctx.guild:
#         ServerId = ctx.guild.id
#         if extension in ServerCogs.get(ServerId, {}).get("LoadedCog", set()):
#             try:
#                 bot.unload_extension(f"cogs.{extension}")
#                 await ctx.send(f"UnLoaded {extension} done.")
#                 ServerCogs[ServerId]["LoadedCog"].remove(extension)
#             except commands.ExtensionNotLoaded:
#                 await ctx.send(f"{extension} is not loaded.")
#             except Exception as e:
#                 await ctx.send(f"Failed to Unload {extension}: {e}")
#         else:
#             await ctx.send(f"{extension} is not loaded.")


# # 重新載入指令
# @bot.command()
# # @commands.check(Administrator)
# async def reload(ctx, extension):
#     if ctx.guild:
#         ServerId = ctx.guild.id
#         if extension in ServerCogs.get(ServerId, {}).get("LoadedCog", set()):
#             try:
#                 bot.reload_extension(f"cogs.{extension}")
#                 await ctx.send(f"ReLoaded {extension} done.")
#             except commands.ExtensionNotLoaded:
#                 await ctx.send(f"{extension} is not loaded.")
#             except Exception as e:
#                 await ctx.send(f"Failed to reload {extension}: {e}")
#         else:
#             await ctx.send(f"{extension} is not loaded.")
# # 一次載入全部指令
# @bot.command()
# # @commands.check(Administrator)
# async def aload(ctx):
#     if ctx.guild:
#         ServerId = ctx.guild.id
#         if ServerId not in ServerCogs:
#             ServerCogs[ServerId] = {"LoadedCog" : set()}
#         for filename in os.listdir("./cogs"):
#             if filename.endswith(".py"):
#                 extension_name = f"cogs.{filename[:-3]}"
#                 if extension_name not in ServerCogs[ServerId]['LoadedCog']:
#                     bot.load_extension(extension_name)
#                     ServerCogs[ServerId]['LoadedCog'].add(extension_name)
#                     await ctx.send(f"Loaded {extension_name} done.")
#                     await asyncio.sleep(1)
#                 else:
#                     bot.reload_extension(f"cogs.{extension_name}")
#                     await ctx.send(f"Loaded {extension_name} done.")
#                     await asyncio.sleep(1)
#         await ctx.send("All Loaded.")

# # 一次卸載全部指令
# @bot.command()
# # @commands.check(Administrator)
# async def unaload(ctx):
#     if ctx.guild:
#         ServerId = ctx.guild.id
#         for extension in ServerCogs.get(ServerId, {}).get('LoadedCog', set()).copy():
#             bot.unload_extension(extension)
#             ServerCogs[ServerId]['LoadedCog'].remove(extension)
#             await ctx.send(f"UnLoaded {extension} done.")
#             await asyncio.sleep(1)
#         await ctx.send("All UnLoaded.")
