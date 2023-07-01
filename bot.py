import os
import random
from functools import partial

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from vk_keyboards import keyboards


class Bot:
    def __init__(self):
        self.vk_session = VkApi(token=os.environ["VK_API_TOKEN"])
        self.longpoll = VkBotLongPoll(self.vk_session, os.environ["GROUP_ID"])
        self.is_bool_keyboard = False
        self.is_platform_requested = False
        self.page_number = 1
        self.MAX_PAGES = 2
        self.commands = "Список доступных команд: {}/" + str(self.MAX_PAGES)

    def _send_msg(self, message, keyboard=None):
        self.vk_session.method(
            "messages.send",
            {
                "chat_id": self.chat_id,
                "message": message,
                "random_id": random.getrandbits(32),
                "keyboard": keyboard,
            },
        )

    @staticmethod
    def _parse_message(message):
        return message.lower().replace("[club200532608|@club200532608] ", "")

    def listen(self):
        for event in self.longpoll.listen():
            if event.type != VkBotEventType.MESSAGE_NEW:
                continue

            self.chat_id = event.chat_id  # type: ignore
            message = self._parse_message(event.object["message"]["text"])

            {
                "помощь": self._send_help,
                "информация": self._send_information,
                "случайная игра": self._send_platform_selection,
                "компьютер": partial(self._send_random_game, "компьютер"),
                "смартфон": partial(self._send_random_game, "смартфон"),
                "скрыть": self._send_offer_to_return_keyboard,
                "да": partial(self._send_bool_result, "да"),
                "нет": partial(self._send_bool_result, "нет"),
                "следующая страница": self._send_next_page,
                "предыдущая страница": self._send_previous_page,
                "о проекте": self._send_info_about_bot,
                "создатели": self._send_info_about_creators,
            }.get(message, self._send_reaction_to_unknown_command)()

    def _send_help(self):
        self._send_msg(self.commands.format(1), keyboards[1].get_keyboard())

    def _send_information(self):
        self.page_number = 2
        self._send_msg(self.commands.format(2), keyboards[2].get_keyboard())

    def _send_platform_selection(self):
        self.is_platform_requested = True
        self._send_msg("Чем вы пользуетесь?", keyboards["platform"].get_keyboard())

    def _send_random_game(self, platform):
        if self.is_platform_requested:
            self.is_platform_requested = False
            file_names = {
                "компьютер": "games/pc_games.txt",
                "смартфон": "games/smartphone_games.txt",
            }
            with open(file_names[platform]) as file:
                random_game = random.choice(file.readlines())
            self._send_msg(f"Советую поиграть в: {random_game}")

    def _send_previous_page(self):
        if self.page_number > 1:
            self.page_number -= 1
        self._send_msg(
            self.commands.format(self.page_number),
            keyboards[self.page_number].get_keyboard(),
        )

    def _send_offer_to_return_keyboard(self):
        self.is_bool_keyboard = True
        self._send_msg("Клавиатура закрыта", keyboards[self.page_number].get_empty_keyboard())
        self._send_msg("Вы случайно закрыли?", keyboards["bool"].get_keyboard())

    def _send_bool_result(self, message):
        if self.is_bool_keyboard:
            self.is_bool_keyboard = False
            if message == "нет":
                self._send_msg("Спасибо за внимание. До свидания!")
            else:
                self._send_msg(
                    self.commands.format(self.page_number),
                    keyboards[self.page_number].get_keyboard(),
                )

    def _send_next_page(self):
        if self.page_number < self.MAX_PAGES:
            self.page_number += 1
        self._send_msg(
            self.commands.format(self.page_number),
            keyboards[self.page_number].get_keyboard(),
        )

    def _send_info_about_bot(self):
        self._send_msg("Школьный проект для демонстрации возможностей бота.\nСоздан в 2021 году.")

    def _send_info_about_creators(self):
        self._send_msg("Чуркин Павел, ученик 9Б класса\nСарапов Станислав, ученик 9Б класса")

    def _send_reaction_to_unknown_command(self):
        self._send_msg(
            "Такой команды у меня нет.\nВоспользуйтесь одной из следующих команд.",
            keyboards["help"].get_keyboard(),
        )
