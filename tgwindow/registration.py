from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from window_base import WindowBase



class Registration:
    """
    Реестр для регистрации классов окон (WindowBase).

    Этот класс управляет единственным экземпляром реестра окон и позволяет добавлять окна
    в реестр по имени класса. Используется для проверки и обеспечения уникальности окон.
    """

    # Единственный экземпляр реестра
    _instance = None

    # Словарь для хранения зарегистрированных окон (имя класса -> сам класс)
    windows: dict[str, "WindowBase"] = {}

    def __new__(cls):
        """
        Создает и возвращает единственный экземпляр реестра окон.

        Если экземпляр еще не создан, то он будет инициализирован. В противном случае возвращается
        уже существующий экземпляр.

        :return: Экземпляр класса Registration.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def add(cls, obj: "WindowBase"):
        """
        Добавляет класс окна в реестр.

        Проверяет, существует ли уже окно с таким именем, и если нет, добавляет его в реестр.
        Если окно с таким именем уже зарегистрировано, генерирует исключение.

        :param obj: Класс окна, который необходимо зарегистрировать.
        :raises ValueError: Если класс с таким именем уже зарегистрирован.
        """
        # Приводим имя класса к нижнему регистру
        name = obj.__name__.lower()

        # Если окно с таким именем уже существует в реестре, выбрасываем исключение
        if name in cls._instance.windows:
            raise ValueError(f"Класс с именем '{obj.name}' уже зарегистрирован! Измените название класса.")

        # Добавляем класс окна в реестр
        cls._instance.windows[name] = obj

    def __repr__(self):
        """
        Возвращает строковое представление реестра окон.

        :return: Строка с информацией о зарегистрированных окнах.
        """
        return f"Registration(windows={self.windows})"
