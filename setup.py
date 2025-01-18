from setuptools import setup, find_packages

setup(
    name="tgwindow",
    version="0.2.0",
    description="Библиотека для создания простых окон в телеграмм боте.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="PyExecutor",
    author_email="belyankiss@gmail.com",
    url="https://github.com/belyankiss/TelegramWindows.git",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "aiogram"
    ],
)