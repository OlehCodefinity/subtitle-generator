import whisper
import sys
from moviepy import *
import os
import ssl


# Виправлення SSL-помилки
ssl._create_default_https_context = ssl._create_unverified_context

class SubtitleGenerator:
    def __init__(self, directory):
        """Ініціалізація класу з вибраною директорією"""
        self.directory = directory
        self.model = whisper.load_model("base")  # Можна замінити на "small", "medium", "large"

    def get_mp4_files(self):
        """Знаходить всі .mp4 файли в директорії"""
        if not os.path.exists(self.directory):
            print(f"Директорія {self.directory} не існує.")
            return []

        return [file for file in os.listdir(self.directory) if file.endswith(".mp4")]

    def extract_audio(self, video_path, audio_path="temp_audio.mp3"):
        """Витягує аудіо з відеофайлу"""
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, codec='mp3')
        return audio_path

    def transcribe_audio(self, video_path):
        """Розпізнає мову та повертає список сегментів тексту"""
        audio_path = self.extract_audio(video_path)
        result = self.model.transcribe(audio_path)
        os.remove(audio_path)  # Видаляємо тимчасове аудіо
        return result["segments"]

    def save_vtt(self, segments, output_vtt):
        """Зберігає субтитри у форматі .vtt"""
        with open(output_vtt, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")  # Обов'язковий заголовок для WebVTT
            for segment in segments:
                start_time = self.format_time_vtt(segment["start"])
                end_time = self.format_time_vtt(segment["end"])
                text = segment["text"]

                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

        print(f"Субтитри збережено у {output_vtt}")

    def format_time_vtt(self, seconds):
        """Конвертує час у формат WebVTT (гг:хх:сс.мс)"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

    def generate_subtitles(self):
        """Генерує субтитри для всіх .mp4 файлів у директорії"""
        mp4_files = self.get_mp4_files()
        
        if not mp4_files:
            print("MP4 файли не знайдено.")
            return

        for file in mp4_files:
            video_path = os.path.join(self.directory, file)
            output_vtt = os.path.join(self.directory, f"{os.path.splitext(file)[0]}.vtt")

            print(f"Обробка: {file}")
            segments = self.transcribe_audio(video_path)
            self.save_vtt(segments, output_vtt)

if __name__ == "__main__":

        generator = SubtitleGenerator(directory="/Users/oleh.lohvyn/Downloads")
        generator.generate_subtitles()