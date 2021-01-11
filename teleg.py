from pyowm import OWM
from pyowm.owm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
import telebot

import configparser
config_raw = configparser.ConfigParser()
config_raw.read("config.ini")
config = config_raw["DEFAULT"]

telegram_token = config.get("telegram_token")
weather_token = config.get("weather_token")

config_dict = get_default_config()
config_dict['language'] = 'ru'


bot = telebot.TeleBot(telegram_token, parse_mode=None)
owm = OWM(weather_token , config_dict)
mgr = owm.weather_manager()


@bot.message_handler(content_types=['text'])
def send_welcome(message):

	observation = mgr.weather_at_place(message.text)
	w = observation.weather

	temp = w.temperature('celsius')['temp']

	answer = 'У Місті ' + message.text + ' зараз ' + w.detailed_status + '\n'
	answer += 'Температура близько ' + str(temp) + '\n \n'

	if temp < -5:
		answer += 'Зараз капєц як холодно, одівай шубу'

	elif temp < 0:
		answer += 'Зараз прохолодно, одівай куртку'

	elif temp < 15:
		answer += 'Зараз нормально, одівай вітровку'

	else:
		answer += 'Зараз жарко, одівай футболку'

	bot.send_message(message.chat.id, answer)

bot.polling(none_stop = True)