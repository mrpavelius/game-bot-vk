from vk_api.keyboard import VkKeyboard, VkKeyboardColor

keyboards = {}

first_keyboard = VkKeyboard()
first_keyboard.add_button("Топ игр", VkKeyboardColor.PRIMARY)
first_keyboard.add_button("Статистика", VkKeyboardColor.PRIMARY)
first_keyboard.add_line()
first_keyboard.add_button("Случайная игра", VkKeyboardColor.PRIMARY)
first_keyboard.add_line()
first_keyboard.add_button("Следующая страница", VkKeyboardColor.POSITIVE)
first_keyboard.add_line()
first_keyboard.add_button("Скрыть", VkKeyboardColor.NEGATIVE)
keyboards[1] = first_keyboard

second_keyboard = VkKeyboard()
second_keyboard.add_button("О проекте", VkKeyboardColor.PRIMARY)
second_keyboard.add_button("Создатели", VkKeyboardColor.PRIMARY)
second_keyboard.add_line()
second_keyboard.add_openlink_button(
    "Репозиторий на GitHub", "https://github.com/mrpavchu/GameBot"
)
second_keyboard.add_line()
second_keyboard.add_button("Предыдущая страница", VkKeyboardColor.POSITIVE)
second_keyboard.add_line()
second_keyboard.add_button("Скрыть", VkKeyboardColor.NEGATIVE)
keyboards[2] = second_keyboard

boolean_keyboard = VkKeyboard(inline=True)
boolean_keyboard.add_button("Да", VkKeyboardColor.POSITIVE)
boolean_keyboard.add_button("Нет", VkKeyboardColor.NEGATIVE)
keyboards["bool"] = boolean_keyboard

help_keyboard = VkKeyboard(inline=True)
help_keyboard.add_button("Помощь", VkKeyboardColor.PRIMARY)
help_keyboard.add_button("Информация", VkKeyboardColor.PRIMARY)
keyboards["help"] = help_keyboard

platform_choice = VkKeyboard(inline=True)
platform_choice.add_button("Компьютер", VkKeyboardColor.POSITIVE)
platform_choice.add_button("Смартфон", VkKeyboardColor.POSITIVE)
keyboards["platform"] = platform_choice
