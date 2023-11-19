from openai import OpenAI
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import speech_recognition as sr

client = OpenAI()

def convert_mp4_to_wav(input_file, output_file):
    # Загружаем видеофайл
    video_clip = VideoFileClip(input_file)

    # Извлекаем аудиодорожку
    audio_clip = video_clip.audio

    # Сохраняем аудио в формате wav
    audio_clip.write_audiofile(output_file, codec='pcm_s16le') #ogg:'libvorbis'

# Функция для распознавания речи в аудиофайле с использованием библиотеки SpeechRecognition
def recognize_audio(audio_file_path, chunk_duration_ms=10000):
    # Загрузка аудио файла
    audio = AudioSegment.from_wav(audio_file_path)

    # Инициализация объекта Recognizer из библиотеки SpeechRecognition
    recognizer = sr.Recognizer()

    # Пустая строка для хранения распознанного текста
    text = ""

    # Определение размера куска аудио в миллисекундах
    chunk_size = int(chunk_duration_ms)

    # Разделение аудио на куски заданного размера
    chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]
    
    # Итерация по каждому куску аудио
    for i, chunk in enumerate(chunks):
        # Создание временного файла для текущего куска
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

        # Использование AudioFile из SpeechRecognition для открытия временного файла
        with sr.AudioFile(chunk_path) as source:
            # Запись аудио из файла
            chunk_audio = recognizer.record(source)

            try:
                # Попытка распознавания речи с использованием Google Speech Recognition
                chunk_text = recognizer.recognize_google(chunk_audio, language="ru-RU")
                
                # Добавление распознанного текста к общему тексту
                text += chunk_text + " "

                # Вывод распознанного текста для текущего куска
                print(chunk_text)
                print("")
            except sr.UnknownValueError:
                # Обработка случая, когда Google Speech Recognition не может распознать аудио
                print(f"Google Speech Recognition не смог распознать аудио для куска {i}")

    # Возврат общего распознанного текста
    return text


def save_to_text_file(result_text, output_file_path):
    with open(output_file_path, "a", encoding="utf-8") as file:
        file.write(result_text)

def split_text(text, max_chunk_size = 2048):
    
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


# Функция для генерации краткого содержания текста с использованием OpenAI GPT-3
def generate_summary(text, max_chunk_size=2048):
    # Разбивка входного текста на куски с заданным максимальным размером
    input_chunks = split_text(text, max_chunk_size)
    print("Text split ")
    print(len(input_chunks))
    
    # Список для хранения сгенерированных кусков текста
    output_chunks = []
    
    # Задание промпта для модели
    #prompt = "напиши важные тезисы из текста "
    prompt = " выдели только самые важные тезисы очень кратко "

    # Итерация по каждому куску входного текста
    for i, chunk in enumerate(input_chunks):
        # Запрос к модели GPT-3 для генерации тезисов на основе текущего куска текста
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt + chunk}
            ],
            temperature=0.1
        )
        
        # Извлечение сгенерированного ответа от модели
        answer = response.choices[0].message.content
        
        # Вывод информации о текущем куске
        print(f"chunk {i+1} from {len(input_chunks)}")
        print(answer)
        
        # Добавление сгенерированного куска в список
        output_chunks.append(answer)
    
    # Объединение сгенерированных кусков в одну строку и возврат результата
    return " ".join(output_chunks)


#convert_mp4_to_wav('input.mp4', 'output.wav')
#text_result = recognize_audio('output.wav')
#save_to_text_file(text_result, "result.txt")

with open("result.txt", 'r', encoding='utf-8') as file:
    text = file.read()

summary = generate_summary(text)
print("Summary")
print(summary)

with open("summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

