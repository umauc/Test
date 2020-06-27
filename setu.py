import asyncio
from mirai import Mirai, Plain, GroupMessage, Group, Image, Member
from PIL import Image as Images
from PIL import ImageDraw
from io import BytesIO
import time
import regex
import urllib
import aiohttp

qq = 1743234087  # 字段 qq 的值
authKey = '1234567890'  # 字段 authKey 的值
# httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.
mirai_api_http = '120.79.196.188:8080/ws'

app = Mirai(f"mirai://{mirai_api_http}?authKey={authKey}&qq={qq}")

def antishield(url, pid): #反腾讯图片和谐，原理是在图片的四角加上１ｘ１的透明像素
    try:
        r = requests.get(url)
        i = Images.open(BytesIO(r.content))
        i.save(str(pid) + '.png', "PNG")
        return str(pid) + '.png'
    except:
        return '0'

@app.receiver('GroupMessage')
async def event_gm(app: Mirai, gm: GroupMessage, group: Group, member: Member):
    async with aiohttp.ClientSession() as session:
        if str(type(gm.messageChain.__root__[1])) == "<class 'mirai.event.message.components.Plain'>":
            message = gm.messageChain.__root__[1].text
            if regex.compile('^#?(RWKK)?(?<keyword>.*)$', regex.I).match(message)[1] == 'RWKK':
                print('开始处理')
                keyword=regex.compile('^#?(RWKK)?(?<keyword>.*)$', regex.I).match(message)[2]
                if keyword == 'None':
    			    async with session.get('https://api.lolicon.app/setu/?apikey=408800685e6e285c17f744&size1200=true') as r:
                    data =await r.json()['data'][0]
                else:
    		        async with session.get('https://api.lolicon.app/setu/?apikey=408800685e6e285c17f744&size1200=true&keyword=' + keyword) as r:
                    data =await r.json()['data'][0]
                if await r.json()['code'] == '404':
                    await app.sendGroupMessage(group,[Plain(text='弟啊你XP咋那么奇怪啊?')])
                else:
                    pid =data.get('pid')
                    url = data.get('url')
                    title = data.get('title')
                    file = antishield(url, pid)
                    if file == '0':
                        await app.sendGroupMessage(group,[Plain(text='图片获取失败!')])
                    else:
                        await app.sendGroupMessage(group, [Plain(text=f'标题:{title},ID:{pid}')])
                        message1 = urllib.parse.quote(f'[CQ:image,file={url}]')
    		   			async with session.get(f"http://120.79.196.188:5700/send_group_msg?group_id={group.id}&message={message1}") as send:
                    	    if await send.json().get('status') == 'ok':
                        	    print('ok')
                                await asyncio.sleep(15)
                                async with session.get(f"http://120.79.196.188:5700/delete_msg?message_id={await send.json().get('data').get('message_id')}") as send1:
                                    print (send1.json())
    elif str(type(gm.messageChain.__root__[1])) == "<class 'mirai.event.message.components.Image'>":
        imageID = gm.messageChain.__root__[1].imageId
        if imageID == 'B407F708-A2C6-A506-3420-98DF7CAC4A57':
            print('开始处理')
    	    async with session.get('https://api.lolicon.app/setu/?apikey=408800685e6e285c17f744&size1200=true') as r:
            data =await r.json()['data'][0]
            if await r.json()['code'] == '404':
                await app.sendGroupMessage(group,[Plain(text='弟啊你XP咋那么奇怪啊?')])
            else:
                pid =data.get('pid')
                url = data.get('url')
                title = data.get('title')
                file = antishield(url, pid)
                if file == '0':
                    await app.sendGroupMessage(group,[Plain(text='图片获取失败!')])
                else:
                    await app.sendGroupMessage(group, [Plain(text=f'标题:{title},ID:{pid}')])
                    message1 = urllib.parse.quote(f'[CQ:image,file={url}]')
     	   			async with session.get(f"http://120.79.196.188:5700/send_group_msg?group_id={group.id}&message={message1}") as send:
                   	    if await send.json().get('status') == 'ok':
                       	    print('ok')
                            await asyncio.sleep(15)
                            async with session.get(f"http://120.79.196.188:5700/delete_msg?message_id={await send.json().get('data').get('message_id')}") as send1:
                                print (send1.json())
if __name__ == "__main__":
    app.run()
