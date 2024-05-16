### Саммаризатор
Из длинного разговора в короткое саммари

Факт обо мне. Для прокачки флюента английского я с некоторой периодичностью слушаю подкасты тут [BBC](https://www.bbc.co.uk/programmes/w3ct3bxl). Но вдруг я пропустила что-то важное? Дотошность или педантизм, или профессиональная деформация, можно называть по-разному. 
В общем написала скрипт, который переводит аудиофайл mp3 в текст с помощью [SpeechRecognition](https://github.com/Uberi/speech_recognition/tree/master) и затем делает саммари из текста с помощью API [OpenAI](https://openai.com/). Вдруг кому-то тоже интересно - исходники [тут](https://github.com/MariaKudryashova/V2T-Summarizer/tree/main), описание поподробнее [тут]()

### Алгоритм:
1. В директорию со скриптом сохраняем анализируемый аудио файл под именем `input.mp4`
2. Устанавливаем и активируем виртуальное окружение:
`python -m venv myenv`
Windows: `myenv\Scripts\activate`
Unix: `source myenv/bin/activate`
3. Устанавливаем необходимые библиотеки:
`pip install -r requirements.txt`
4. Подключаем [API OpenAI](https://platform.openai.com/docs/quickstart). Можно токены подключать под каждый проект, а можно разово на систему. Я шла по второму пути.
5. Запускаем скрипт `python v2t.py ru-Ru` или `python v2t.py en-US`
смотря на каком языке аудиофайл.
6. На выходе имеем два файла:
`result.txt` - в целом весь аудио в виде текста
`summary.txt` - саммари текста

### Инструменты: 
Speech Recognition - перевод из аудио в текст
OpenAI gpt-3.5-turbo - саммаризатор (в том числе)
pydub - работа с аудио файлами и их обработка
moviepy - разбивка большого аудио на части и их синхронизация

### Планы для еще больших лентяев:
- можно заставить скрипт самому ходить по ссылкам и скачивать нужные файлы с аудиодорожками в нужном формате (с помощью Selenium)
- можно потренировать ChatGPT под себя, подкрутить настройки, чтобы он акцентировал внимание на нужные именно мне детали, подавал саммари в нужном мне стиле
- ну и вообще этот скрипт можно прикрутить к своему сайту/телеграмм боту и другому сервису в концепте "одной кнопки"
- можно пооптимизировать саммаризацию, сделать несколько подходов к ней для слишком больших текстов, поиграть с размерами единичных блоков аудио и текста
- поиграть с кодеками и видами входных видео и аудио файлов (mp3, mp4, wmv, ogg) и автоматизировать процесс выбора и обработки каждого из этих видов файлов.
- навести красоту с обработкой ошибок

