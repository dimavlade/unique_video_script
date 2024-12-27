import subprocess
import sys
import argparse
import random

# Функция для проверки и установки moviepy, если он не установлен
def install_moviepy():
    try:
        import moviepy
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])

# Установка moviepy, если он еще не установлен
install_moviepy()

from moviepy import VideoFileClip, vfx

def adjust_video(input_path, output_path):
    
    # Случайные значения для параметров от 1 до 20%
    speed_factor = 1 + random.uniform(0.01, 0.2)
    brightness_factor = 1 + random.uniform(0.01, 0.2)
    contrast_factor = random.uniform(0.01, 0.2)
    volume_factor = 1 + random.uniform(0.01, 0.2)

    # Процентные значения для лога
    speed_percentage = (speed_factor - 1) * 100
    brightness_percentage = (brightness_factor - 1) * 100
    contrast_percentage = contrast_factor * 100
    volume_percentage = (volume_factor - 1) * 100

    # Вывод сгенерированных параметров
    print(f"Сгенерированные параметры:")
    print(f"Коэффициент ускорения видео: {speed_percentage:.0f}%")
    print(f"Коэффициент увеличения яркости: {brightness_percentage:.0f}%")
    print(f"Коэффициент увеличения контрастности: {contrast_percentage:.0f}%")
    print(f"Коэффициент увеличения громкости: {volume_percentage:.0f}%")

    # Загрузка видеофайла
    video = VideoFileClip(input_path)
    
    # Ускорение видео
    video = video.fx(vfx.speedx, speed_factor)
    
    # Регулировка яркости и контрастности
    video = video.fx(vfx.colorx, brightness_factor)
    video = video.fx(vfx.lum_contrast, lum=0, contrast=contrast_factor)
    
    # Ускорение и увеличение громкости аудио
    video.audio = video.audio.fx(vfx.speedx, speed_factor)
    video.audio = video.audio.volumex(volume_factor)
    
    # Сохранение результата в выходной файл
    video.write_videofile(output_path, codec="libx264")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Уникализация видео через изменение скорости, яркости, контрастности и громкости видео.")
    parser.add_argument("input_video", type=str, help="Путь к входному видеофайлу.")
    parser.add_argument("output_video", type=str, help="Путь к выходному видеофайлу.")
    
    args = parser.parse_args()
    
    adjust_video(args.input_video, args.output_video)
