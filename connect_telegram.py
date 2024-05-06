
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# app = ApplicationBuilder().token("YOUR TOKEN HERE").build()

# app.add_handler(CommandHandler("hello", hello))

# app.run_polling()

# import requests

# def send_message(bot_token, chat_id, text):
#     url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#     params = {
#         'chat_id': chat_id,
#         'text': text
#     }
#     response = requests.post(url, data=params)
#     return response.json()

# # Thay thế 'BOT_TOKEN' bằng mã token của bot bạn muốn gửi tin nhắn
# # Thay thế 'CHAT_ID' bằng chat_id của người nhận hoặc nhóm mà bạn muốn gửi tin nhắn
# # Thay thế 'TEXT' bằng nội dung tin nhắn bạn muốn gửi
# bot_token = '5970465385:AAGySp4xbKHLSFl1NDN83_ypc2-2nWN9HFg'
# chat_id = '-4255574897'
# text = '@w909_bot màu đen có bao nhiêu chữ cái'

# send_message(bot_token, chat_id, text)


from telethon.sync import TelegramClient, events
from telethon.tl.types import InputPeerUser

# Sử dụng api_id và api_hash từ my.telegram.org
api_id = '29271881'
api_hash = '63628d4eaa5c2a5bde2e86f62dcc424c'
session_name = 'your_session_name'

# # Tạo một đối tượng client
# with TelegramClient('your_session_name', api_id, api_hash) as client:
#     # Gửi tin nhắn
#     client.send_message('@j2team_gpt_bot', 'Hello, đây là tin nhắn từ telethon!')

import PyPDF2
file_path = "C:/Users/Hi/Desktop/9F9B291C-5A9E-11EE-90B6-F71C97318934.pdf" #cái này bất ổn quá
# file_path = "D:/AI+/Các hệ thống thông minh.pdf"

with open(file_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    
    all_text = "Chỉ trả lời yes hoặc no thôi nhé\n"
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        all_text += page.extract_text()
        if page_number == 0:
            break
      

# Tạo client mới
client = TelegramClient('your_session_name', api_id, api_hash)
message_sent = False
async def send_hello_message():
    await client.send_message('@j2team_gpt_bot', all_text)


# Event handler để lắng nghe tin nhắn mới
@client.on(events.NewMessage())
async def handler(event):
    global message_sent  
    # Lấy username của người gửi tin nhắn
    from_user = await event.get_sender()
    from_username = "@" + from_user.username if from_user.username else from_user.first_name

    # Kiểm tra nếu người gửi là @a hoặc bất kỳ logic nào bạn muốn thêm
    print(from_username)
    if from_username.lower() == '@j2team_gpt_bot':
        # Lưu text vào txt file và in ra console
        # with open("messages.txt", "a") as file:
        #     file.write(f"{event.raw_text}n")

        # Hiển thị ra console
        print(event.raw_text)
        message_sent = True 
        await client.disconnect()

with client:
    client.loop.run_until_complete(send_hello_message())
    while not message_sent:
        pass
    client.run_until_disconnected()
