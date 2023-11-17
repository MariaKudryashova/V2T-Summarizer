from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
import openai

import requests
from urllib3 import disable_warnings

def convert_mp4_to_wav(input_file, output_file):
    # Загружаем видеофайл
    video_clip = VideoFileClip(input_file)

    # Извлекаем аудиодорожку
    audio_clip = video_clip.audio

    # Сохраняем аудио в формате wav
    audio_clip.write_audiofile(output_file, codec='pcm_s16le') #ogg:'libvorbis'

def recognize_audio(audio_file_path, chunk_duration_ms=10000):
    # Загрузка аудио файла
    audio = AudioSegment.from_wav(audio_file_path)

    # Получение длительности аудио в миллисекундах
    audio_duration_ms = len(audio)

    # Разбивка на части и распознавание речи
    recognizer = sr.Recognizer()
    text = ""

    # Расчет общего количества итераций
    total_iterations = audio_duration_ms // chunk_duration_ms + 1

    for i in range(0, audio_duration_ms, chunk_duration_ms):
        
        print(f"Итерация {i // chunk_duration_ms + 1} из {total_iterations}")
        
        # Выборка части аудио
        chunk = audio[i:i + chunk_duration_ms]

        # Сохранение временного файла
        chunk.export("temp_chunk.wav", format="wav")

        # Распознавание речи        
        with sr.AudioFile("temp_chunk.wav") as source:
            audio_chunk = recognizer.record(source)
            try:
                # Попытка распознавания речи
                chunk_text = recognizer.recognize_google(audio_chunk, language="ru-RU")
                text += chunk_text + " "
                
            except sr.UnknownValueError:
                print("Google Speech Recognition не смог распознать аудио")

    return text

def save_to_text_file(result_text, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(result_text)

def summary_text(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Запрос к OpenAI API для выделения главной мысли
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=50  # Выберите количество токенов в зависимости от вашего текста
    )

    # Извлечение ответа сгенерированного моделью
    main_idea = response.choices[0].text.strip()

    # Вывод результата
    print("Главная мысль: ", main_idea)

disable_warnings()

openai.api_host = 'https://api.openai.com'
openai.api_base = openai.api_host
openai.verify_ssl_certs = False

with open("apikey.txt", 'r') as file:
    openai.api_key = file.read().strip()

#convert_mp4_to_wav('input.mp4', 'output.wav')
#text_result = recognize_audio('output.wav')
#save_to_text_file(text_result, "result.txt")

summary_text("result.txt")
