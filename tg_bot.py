import json
from config import token, user_id
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hitalic, hlink
from main import check_update
import asyncio

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.message):
    start_buttons = ["All articles", "Last 3 articles", "Fresh articles"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Articles", reply_markup=keyboard)


@dp.message_handler(Text(equals="All articles"))
async def get_all_news(message: types.message):
    with open("articles_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        # articles = f"{hbold(v['article_date'])}\n" f"{v['article_title']}\n" f"{v['article_author']}\n" f"{v['article_url']}\n"
        articles = f"{hbold(v['article_date'])}\n" f"{hitalic(v['article_author'])}\n" f"{hlink(v['article_title'], v['article_url'])}\n"

        await message.answer(articles)


@dp.message_handler(Text(equals="Last 3 articles"))
async def get_last_three(message: types.message):
    with open("articles_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-3:]:
        articles = f"{hbold(v['article_date'])}\n" f"{hitalic(v['article_author'])}\n" f"{hlink(v['article_title'], v['article_url'])}\n"

        await message.answer(articles)


@dp.message_handler(Text(equals="Fresh articles"))
async def get_fresh_news(message: types.message):
    fresh_news = check_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            articles = f"{hbold(v['article_date'])}\n" f"{hitalic(v['article_author'])}\n" f"{hlink(v['article_title'], v['article_url'])}\n"

            await message.answer(articles)
    else:
        await message.answer("No fresh articles current time...")


async def send_articles_auto():
    while True:
        fresh_news = check_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                articles = f"{hbold(v['article_date'])}\n" f"{hitalic(v['article_author'])}\n" f"{hlink(v['article_title'], v['article_url'])}\n"

                await bot.send_message(user_id,
                                       articles,
                                       disable_notification=True)
        # else:
        #     await bot.send_message(user_id,
        #                            "No fresh articles current time...")

        await asyncio.sleep(20)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_articles_auto())
    executor.start_polling(dp)