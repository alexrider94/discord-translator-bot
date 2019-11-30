import discord
import logging
import pymongo
import requests
from discord.ext import commands

#logger for info and Debug events
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#connect mongodb
connect = pymongo.MongoClient('localhost',27017)

database = connect.Discord
collection = database.DiscrodTextData 
database = connect.get_database('Discord')
collection = database.get_collection('DiscrodTextData')

#define discord bot
class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        getContent = message.content
        getTime = message.created_at

        print(getContent,getTime)

        collection.insert({"content":getContent,"time":getTime})



        if message.author.bot == False and message.content.startswith('!'):
            try:
                request_url = "https://openapi.naver.com/v1/papago/n2mt"
                headers= {"X-Naver-Client-Id": "LYIBlmpElX3XTNXly0tU", "X-Naver-Client-Secret":"kKoQRx13bH"}
                params = {"source": "ko", "target": "en", "text": message.content}
                response = requests.post(request_url, headers=headers, data=params)
                result = response.json()
                await message.channel.send(result['message']['result']['translatedText'])
            except:
                await message.channel.send('번역 실패')

            if message.content == '안녕':
                try:
                    await message.channel.send('ㅗ')
                except:
                    await message.channel.send("에러입니다.")

            if message.content.startswith('!help'):
                await message.channel.send('{0.author.mention}'.format(message))

        # don't respond to ourselves
        if message.author == self.user:
            return


client = MyClient()
client.run('NjM4NTc2MjgyMzA0Nzc0MTQ2.Xbe8UA.LXfWPiJ-UrJnimyy75uHrQXWDvc')