import discord
import asyncio, urllib.request, random, time, sqlite3, pickle

#connection = sqlite3.connect('db.sqlite')
#cursor = connection.cursor()

user_data = {'user1': 0, 'user2' : 1}
user_data_bosang = {'user1': 0, 'user2' : 1}
user_name_id = {'user1' : 123123123123123}
user_item = {'user1': ['items', 'items2']}
user_level = {'user1': 123}
user_coin = {'user1': 0}
coin_quote = [0, 0]
save_time_check = round(time.time())


client = discord.Client()

def Save():
    with open('list.bin', 'wb') as f:
        pickle.dump(user_data, f)
    with open('list2.bin', 'wb') as f:
        pickle.dump(user_data_bosang, f)
    with open('list3.bin', 'wb') as f:
        pickle.dump(user_name_id, f)
    with open('list4.bin', 'wb') as f:
        pickle.dump(user_item, f)
    with open('list5.bin', 'wb') as f:
        pickle.dump(user_level, f)
    with open('list6.bin', 'wb') as f:
        pickle.dump(user_coin, f)
    with open('coin_quote.bin','wb') as f:
        pickle.dump(coin_quote, f)

with open('list.bin', 'rb') as f:
    user_data = pickle.load(f)
with open('list2.bin', 'rb') as f:
    user_data_bosang = pickle.load(f)
with open('list3.bin', 'rb') as f:
    user_name_id = pickle.load(f)
with open('list4.bin', 'rb') as f:
    user_item = pickle.load(f)
with open('list5.bin', 'rb') as f:
    user_level = pickle.load(f)
with open('list6.bin', 'rb') as f:
    user_coin = pickle.load(f)
with open('coin_quote.bin', 'rb') as f:
    coin_quote = pickle.load(f)

#user_level
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    


@client.event
async def on_message(message):

    
        
    #print(user_data_bosang)
        
    try: print(list(user_data.keys()).index(message.author.id))
    except ValueError : user_data[message.author.id] = 100
    else: user_data[message.author.id] += user_level[message.author.id]
    
    try: print(list(user_name_id.keys()).index(message.author.name))
    except ValueError : user_name_id[message.author.name] = message.author.id
    
    try: print(list(user_data_bosang.keys()).index(message.author.id))
    except ValueError : user_data_bosang[message.author.id] = 0

    try: print(list(user_item.keys()).index(message.author.id))
    except ValueError : user_item[message.author.id] = []
    
    try: print(list(user_level.keys()).index(message.author.id))
    except ValueError : user_level[message.author.id] = 1

    try: print(list(user_coin.keys()).index(message.author.id))
    except ValueError : user_coin[message.author.id] = 0

    if round(time.time()) - user_data_bosang[message.author.id] > 120 and user_data[message.author.id] > 10000:
        user_data[message.author.id] -= round(user_data[message.author.id] / 10)
        await message.channel.send("```"+ message.author.name + "님의 포인트가 10000 이상으로 세금을 징수합니다.\n10%의 세금을 징수하여 " + str(user_data[message.author.id]) + "포인트를 소지하고 계십니다.```")
        user_data_bosang[message.author.id] = round(time.time())
    
    if round(time.time()) - coin_quote[1] >= 20:
        coin_quote[0] = random.randrange(100, 1000)
        coin_quote[1] = round(time.time())
        #await message.channel.send("현재시세: " + str(coin_quote[0]))
    
    if message.content.endswith('!포인트'): 
        await message.channel.send(str(message.author.name) + "님의 포인트는 " + str(user_data[message.author.id]) + "점 입니다.")
    if message.content.startswith('!시세'): 
        await message.channel.send("현재시세: " + str(coin_quote[0]))
    
    if message.content.startswith('!유저삭제') == True and message.author.id == '495170927722496001':
        await message.channel.send(message.content.split('제 ')[1])
        del user_data[user_name_id[message.content.split('제 ')[1]]]
        del user_data_bosang[user_name_id[message.content.split('제 ')[1]]]
        del user_name_id[message.content.split('제 ')[1]]
        del user_item[user_name_id[message.content.split('제 ')[1]]]
        
    if message.content.startswith('!포인트설정') == True and message.author.id == '495170927722496001':
        user_data[str(user_name_id[message.content.split(' ')[1]])] = int(message.content.split(' ')[2])
        await message.channel.send(user_name_id[message.content.split(' ')[1]] + "님께 " + str(message.content.split(' ')[2]) + "포인트를 설정합니다.")
        
    if message.content.startswith('!레벨설정') == True and message.author.id == '495170927722496001':
        user_level[str(user_name_id[message.content.split(' ')[1]])] = int(message.content.split(' ')[2])
        await message.channel.send(user_name_id[message.content.split(' ')[1]] + "님께 " + str(message.content.split(' ')[2]) + "레벨을 설정합니다.")


        
    if message.content.startswith('!베팅'): 
        if str(message.content.split(' ')[1]) == "올인":
            given = user_data[message.author.id]
            random_output = random.randrange(1, 21)
            if random_output == 1:
                user_data[message.author.id] += given * 3
                await message.channel.send("```1등 당첨 ! 배팅하신 포인트의 3배가 당첨되셨습니다.\n" + str(given * 3) +" 포인트가 당첨되셨으며,\n" + message.author.name +"님은 현재 " + str(user_data[message.author.id]) +" 포인트를 소유중입니다.```")
            elif 1 < random_output < 8 : 
                user_data[message.author.id] += given * 2
                await message.channel.send("```2등 당첨 ! 배팅하신 포인트의 2배가 당첨되셨습니다.\n" + str(given * 2) +" 포인트가 당첨되셨으며,\n" + message.author.name +"님은 현재 "  + str(user_data[message.author.id]) +" 포인트를 소유중입니다.```")
            elif 7 < random_output < 15 :
                await message.channel.send("```3등 당첨 ! 포인트에 변동이 없습니다." + "\n"+ message.author.name +"님은 현재 " + str(user_data[message.author.id]) +" 포인트를 소유중입니다.```")
            elif 14 < random_output < 21 :
                user_data[message.author.id] -= given 
                await message.channel.send("```4등 당첨 ! 배팅하신 포인트를 잃었습니다. \n" + str(given)  +" 포인트를 잃으셨으며,\n" + message.author.name +"님은 현재 "  + str(user_data[message.author.id]) +" 포인트를 소유중입니다.```")
        else:
            given = int(message.content.split(' ')[1]) 
            if int(given) > int(user_data[message.author.id]):
                await message.channel.send("포인트가 부족합니다 !")
            elif given < 0:
                await message.channel.send("응")
                await message.channel.send("아니야")
            else:
                random_output = random.randrange(1, 21)
                if random_output == 1:
                    user_data[message.author.id] += given * 3
                    await message.channel.send("```1등 당첨 ! 배팅하신 포인트의 3배가 당첨되셨습니다.\n" + str(given * 3) +" 포인트가 당첨되셨으며,\n" + message.author.name +"님은 현재 " + str(user_data[message.author.id]) +" 포인트를 소유중입니다.```")
                elif 1 < random_output < 8 : 
                    user_data[message.author.id] += given * 2
                    await message.channel.send("```2등 당첨 ! 배팅하신 포인트의 2배가 당첨되셨습니다.\n" + str(given * 2) +" 포인트가 당첨되셨으며,\n" + message.author.name +"님은 현재 "  + str(user_data[message.author.id]) +" 포인트를 소유중입니다.```")
                elif 7 < random_output < 15 :
                    await message.channel.send("```3등 당첨 ! 포인트에 변동이 없습니다." + "\n"+ message.author.name +"님은 현재 " + str(user_data[message.author.id]) +" 포인트를 소유중입니다.```")
                elif 14 < random_output < 21 :
                    user_data[message.author.id] -= given 
                    await message.channel.send("```4등 당첨 ! 배팅하신 포인트를 잃었습니다. \n" + str(given)  +" 포인트를 잃으셨으며,\n" + message.author.name +"님은 현재 "  + str(user_data[message.author.id]) +" 포인트를 소유중입니다.```")
    


#    if message.content.startswith('!보상'): 
 #       if round(time.time()) - user_data_bosang[message.author.id] > 60:
  #          user_data[message.author.id] += 50
   #         user_data_bosang[message.author.id] = round(time.time())
    #        await message.channel.send("보상을 획득하셨습니다 !")
     #   else: 
      #      await message.channel.send("아직 보상을 받으실 수 없습니다.\n" +"보상 획득까지 " + str(60 - round(time.time()) + user_data_bosang[message.author.id]) +"초 남았습니다.")
        
    if message.content.startswith('!송금'):
        if int(message.content.split(' ')[2]) < 0:
            await message.channel.send("응")
            await message.channel.send("아니야")
        else:
            if user_data[message.author.id] >= int(message.content.split(' ')[2]):
                user_data[str(user_name_id[message.content.split(' ')[1]])] += int(message.content.split(' ')[2])
                user_data[message.author.id] -= int(message.content.split(' ')[2])
                await message.channel.send(message.author.name + "님께서 " + message.content.split(' ')[1] + "님께 " + str(int(message.content.split(' ')[2])) + "포인트를 송금하였습니다." )
            else: 
                await message.channel.send("포인트가 부족합니다 !")
        Save()
        
        #user_data[user_name_id[message.content.split(' ')[1]]] 
    if message.content.startswith('!저장'): Save()

    if message.content.endswith('!레벨'): 
        await message.channel.send("`" + message.author.name + "님의 레벨은 〔" + str(user_level[message.author.id]) + "〕 입니다.`") 
    
    if message.content.startswith('!레벨업'): 
        if user_data[message.author.id] >= user_level[message.author.id] * 300:
            user_data[message.author.id] -= user_level[message.author.id] * 300
            user_level[message.author.id] += 1
            await message.channel.send("```" + message.author.name + "님의 레벨이 " + str(user_level[message.author.id] - 1) + "에서 " + str(user_level[message.author.id]) + "로 상승하였습니다.```")

        else: 
            await message.channel.send("```"+message.author.name + "님, 레벨업을 위해서 " + str(user_level[message.author.id] * 300 - user_data[message.author.id]) +"포인트 남았습니다.```")

    if message.content.startswith('!순위'): 
        New_dict = {}
        Text = "```"
        for key1, value1 in sorted(user_level.items(), key=lambda x: x[1], reverse=True):
            for key2,value2 in user_name_id.items():
                if key1 == value2:
                    New_dict[key2] = value1
        range_one = 1
        for key, value in New_dict.items():
            Text += str(range_one) + "등 : " + str(key) + "님, " + str(value) + "레벨\n"
            range_one +=1
            if range_one == 11:
                break
        Text+="```"
        await message.channel.send(Text)

    if message.content.startswith('!포인트순위'): 
        New_dict = {}
        Text = "```"
        for key1, value1 in sorted(user_data.items(), key=lambda x: x[1], reverse=True):
            for key2,value2 in user_name_id.items():
                if key1 == value2:
                    New_dict[key2] = value1
        range_one = 1
        for key, value in New_dict.items():
            Text += str(range_one) + "등 : " + str(key) + "님, " + str(value) + "포인트\n"
            range_one +=1
            if range_one == 11:
                break
        Text+="```"
        await message.channel.send(Text)
    
    if message.content.startswith('!마루코인'): 
        if message.content.split(' ')[1] == "시세":
            await message.channel.send("`현재 마루코인 시세: " + str(coin_quote[0]) +"`")
        elif message.content.split(' ')[1] == "구매":
            if user_data[message.author.id] - int(message.content.split(' ')[2]) * coin_quote[0] >= 0:
                user_data[message.author.id] -= int(message.content.split(' ')[2]) * coin_quote[0]
                user_coin[message.author.id] += int(message.content.split(' ')[2])
                await message.channel.send("```"+message.content.split(' ')[2] + "개의 마루코인을 구입하셨습니다. \n" + "마루코인 보유량: " +  str(user_coin[message.author.id]) + " 포인트 보유량: " + str(user_data[message.author.id]) + "```")
            elif int(message.content.split(' ')[2]) < 0:
                await message.channel.send("응 아니야")
            else: 
                await message.channel.send("포인트가 부족합니다 !")
        elif message.content.split(' ')[1] == "판매":
            if int(message.content.split(' ')[2]) <= user_coin[message.author.id]:
                user_data[message.author.id] += int(message.content.split(' ')[2]) * coin_quote[0]
                user_coin[message.author.id] -= int(message.content.split(' ')[2])
                await message.channel.send("```"+message.content.split(' ')[2] + "개의 마루코인을 판매하셨습니다. \n" + "마루코인 보유량: " +  str(user_coin[message.author.id]) + " 포인트 보유량: " + str(user_data[message.author.id]) + "```")
            elif int(message.content.split(' ')[2]) < 0:
                await message.channel.send("응 아니야")

        elif message.content.split(' ')[1] == "보유":
            await message.channel.send("`현재 "+ message.author.name + "님께서 보유중인 마루코인: " + str(user_coin[message.author.id]) + "`")


    
    
    
    
    Save()
    
        
    


        
    #if message.content.startswith():
        #asd
    # 

        
        


    


        

    #if message.content.startswith('!초기지원금'):
        #asd
        #qwe
    #if message.content.startswith('!봄마루'):
        #
    #if message.content.find('용혁키'):
        #await message.channel.send("정보)) 용혁키 : 158cm")
 

client.run('Njk2Mjg0NTAyNTUyNjA4Nzkw.XomfiA.2nMJy1jhJDrFriGEu3W1qcnkJUw')



