from typing import Union
from typing_extensions import Literal
from tgwindow import TextMessage
from tgwindow.buttons import Inline, Reply


class StaticWindow:
    """
    Класс для создания статической клавиатуры с кнопками, которые могут быть либо
    inline, либо reply, но не оба типа одновременно.

    Этот класс автоматически создает клавиатуру, добавляя все кнопки, определенные как атрибуты класса.
    Локализация поддерживает два языка: русский и английский.
    """

    text: str
    keyboard: list[Union[Inline, Reply, None]]
    dynamic_keyboard = None

    def __new__(cls, lang: Literal["ru", "en"]):
        """
        Создает новый экземпляр StaticWindow и инициализирует клавиатуру.

        :param lang: Язык локализации (ru или en).
        :return: Экземпляр статической клавиатуры.
        """
        _instance = super().__new__(cls)
        _instance.keyboard = []  # Список для хранения кнопок
        _instance.text = None
        _instance.dynamic_keyboard = None
        return _instance

    def __init__(self, lang: Literal["ru", "en"]):
        """
        Инициализирует клавиатуру, добавляя кнопки, определенные как атрибуты класса.

        Кнопки определяются как экземпляры классов Inline или Reply и добавляются
        в соответствующий список клавиатуры.

        :param lang: Язык локализации (ru или en).
        """
        for key, value in self.__class__.__dict__.items():
            # Перебираем все атрибуты класса
            if isinstance(value, TextMessage):
                self.text = value.text.get(lang)
            if isinstance(value, (Inline, Reply)):
                # Добавляем кнопку в клавиатуру для выбранного языка
                self.keyboard.append(value(lang))

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Проверяет, чтобы класс не содержал оба типа кнопок (inline и reply) одновременно.

        Если оба типа кнопок присутствуют, генерируется исключение.

        :raises AttributeError: Если в классе присутствуют оба типа кнопок.
        """
        reply = False
        inline = False
        for value in cls.__dict__.values():
            if isinstance(value, Inline):
                inline = True
            if isinstance(value, Reply):
                reply = True
        if all([inline, reply]):
            raise AttributeError("Клавиатура должна содержать только один вид кнопок.")

    def __repr__(self):
        """
        Возвращает строковое представление статической клавиатуры.

        :return: Строковое представление с текстом и списком кнопок.
        """
        return f"text={self.text}, keyboard={self.keyboard}"
