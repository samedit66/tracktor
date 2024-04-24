# tracktor

`tracktor` это обертка над моделью YOLOv8 для определение объектов из датасета COCO 2017 на видео с динамическом выводом видеопотока на экран.

## Установка
Необходимо склонировать репозиторий:
```bash
> git clone https://github.com/samedit66/tracktor.git
> cd tracktor
```
### Установка в виртуальной среде
По желанию можно создать виртуальную среду, чтобы не загрязнять глобальное пространство пакетов:
```bash
> python -m venv venv
```
#### Активация виртуальной среды
Windows (cmd):
```bash
> venv\Scripts\activate.bat
```
Windows (powershell):
```bash
> venv\Scripts\Activate.ps1
```
Linux и MacOS:
```bash
> source venv/bin/activate
```
Установка зависимостей:
```bash
> pip install -r requirements.txt
```
## Запуск
Для запуска необходимо задать индекс искомого класса через флаг --class и передать путь к видео (класс 15 - коты):
```bash
> python .\tracktor.py --class 15 "путь к видео"
```
