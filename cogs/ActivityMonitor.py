import discord
from discord.ext import commands
import time
from collections import deque

class ActivityMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_times = deque()  # 用於儲存訊息時間戳
        self.threshold = 25  # 設置一個消息數量閾值
        self.time_window = 120  # 设置時間（秒）
        
    @commands.Cog.listener()
    async def on_message(self, message):
        # 忽略機器人自身發送的訊息
        if message.author == self.bot.user:
            return
        
        # 紀錄訊息時間
        current_time = time.time()
        self.message_times.append(current_time)
        
        # 清理過期的訊息時間
        while self.message_times and self.message_times[0] < current_time - self.time_window:
            self.message_times.popleft()
        
        # 判斷是否達到閾值
        if len(self.message_times) >= self.threshold:
            await message.channel.send("做愛")
            self.message_times.clear()

async def setup(bot):
    await bot.add_cog(ActivityMonitor(bot))
