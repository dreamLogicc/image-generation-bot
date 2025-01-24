import logging

from io import BytesIO
from background import keep_alive
from config import BOT_TOKEN, API_ID, API_HASH, HF_KEY
from telethon.sync import TelegramClient, events, Button
from models.image_generator import IMGGen

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
img_gen = IMGGen(hf_key=HF_KEY)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        'Hi! I am bot for image generation. Type /help for help.')


@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond('**Here is the list of commands:** \n\n'
                        '1. Type /choose_model to choose image generation model from list\n'
                        '2. Type /current_model to see what model you use\n'
                        '3. Type /generate to generate image'
                        )


@bot.on(events.NewMessage(pattern='/choose_model'))
async def set_model(event):

    models = {
        1: "stabilityai/stable-diffusion-3.5-large",
        2: 'strangerzonehf/Flux-Midjourney-Mix2-LoRA',
        3: 'black-forest-labs/FLUX.1-dev',
        4: 'stabilityai/stable-diffusion-xl-base-1.0',
        5: 'stable-diffusion-v1-5/stable-diffusion-v1-5'
    }

    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message('**You can choose model from the following list:**\n\n'
                                '1. stabilityai/stable-diffusion-3.5-large \n'
                                '2. strangerzonehf/Flux-Midjourney-Mix2-LoRA\n'
                                '3. black-forest-labs/FLUX.1-dev\n'
                                '4. stabilityai/stable-diffusion-xl-base-1.0\n'
                                '5. stable-diffusion-v1-5/stable-diffusion-v1-5\n\n'
                                '**Send model number.**')
        response = conv.get_response()
        response = await response
        print(response.message)
        try:
            new_model = models[int(response.message)]
            img_gen.set_model(model=new_model, hf_key=HF_KEY)
            await conv.send_message(f'Model changed to {new_model}')
        except Exception as ex:
            print(ex)


@bot.on(events.NewMessage(pattern='/current_model'))
async def get_model(event):
    await event.respond(
        f'You currently use {img_gen.get_model()}')


@bot.on(events.NewMessage(pattern='/generate'))
async def generate(event):
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message('Type your prompt')
        response = conv.get_response()
        response = await response

        try:
            await conv.send_message('Wait, image is generating...')
            image = img_gen.generate(response.message)
            bio = BytesIO()
            bio.name = 'image.jpeg'
            image.save(bio, 'JPEG')
            bio.seek(0)
            await conv.send_file(bio)
        except Exception as ex:
            await conv.send_message('Something went wrong. Try again.')


def main():
    bot.start()
    bot.run_until_disconnected()


if __name__ == '__main__':
    keep_alive()
    main()
