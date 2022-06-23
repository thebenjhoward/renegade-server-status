import threading, queue
from time import sleep
from .conf import get_config
from .server import get_message_text
import discord

timerQueue = queue.Queue()

bot = discord.Client()

def timerWorker():
    # wait for bot to come online before starting
    timerQueue.get()
    timerQueue.task_done()
    shouldRun = True
    while shouldRun:
        # do thing here
        print("Thread did something")
        bot.dispatch("update_message")
        for _ in range(get_config().update_frequency):
            if not timerQueue.empty():
                shouldRun = False
                timerQueue.get()
                timerQueue.task_done()
                break
            sleep(1)
        




@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # start timer thread
    timerQueue.put(True)
    


@bot.event
async def on_update_message():
    print("Got update message event")
    channel = bot.get_channel(get_config().channel_id)
    message = await channel.fetch_message(channel.last_message_id)

    new_content = get_message_text()

    if(message.author.id != bot.user.id):
        print("Sending new message")
        await channel.send(content=new_content)
    else:
        print("Editing old message")
        await message.edit(content=new_content)








def run_bot():
    thread = threading.Thread(target=timerWorker, daemon=True)
    thread.start()
    bot.run(get_config().get_token())
    print("exiting bot")
    timerQueue.put(False)
    thread.join()