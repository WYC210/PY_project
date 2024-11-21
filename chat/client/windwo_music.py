import threading
import pygame
import time

class MusicPlayer:
    def __init__(self):
        self.music_folder = "D:/code/chat/music"
        pygame.mixer.init()
        self.current_song = None

    def play_music(self, song_file):
        """
        播放音乐文件（使用线程避免阻塞主线程）。
        """
        self.current_song = song_file
        thread = threading.Thread(target=self._play_music_thread, args=(song_file,))
        thread.start()

    def _play_music_thread(self, song_file):
        """
        实际播放音乐的线程方法。
        """
        try:
            pygame.mixer.music.load(f"{self.music_folder}/{song_file}")
            pygame.mixer.music.play()
            print(f"正在播放: {song_file}")

            # 等待音乐播放完成
            while pygame.mixer.music.get_busy():
                time.sleep(1)

            print(f"{song_file} 播放完毕")
        except pygame.error as e:
            print(f"播放出错: {e}")

    def stop_music(self):
        """
        停止音乐播放。
        """
        pygame.mixer.music.stop()
        print("音乐播放已停止")

if __name__ == "__main__":
    # 设置音乐文件夹路径


    # 初始化音乐播放器
    player = MusicPlayer()

    # 播放音乐文件
    player.play_music("123.mp3")

    # 模拟其他操作
    for i in range(5):
        print(f"主线程执行任务 {i}")
        time.sleep(2)


