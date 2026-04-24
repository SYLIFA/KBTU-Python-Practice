import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        # Ищем музыку
        try:
            self.playlist = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav'))]
        except Exception:
            self.playlist = []
            
        self.current_index = 0
        self.is_playing = False
        
        # Безопасная загрузка первого трека
        if self.playlist:
            self.load_current_track()

    def load_current_track(self):
        try:
            pygame.mixer.music.load(self.playlist[self.current_index])
        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")
            # Если файл битый, помечаем его
            pass

    def play(self):
        if self.playlist and not self.is_playing:
            try:
                pygame.mixer.music.play()
                self.is_playing = True
            except:
                print("Не удалось воспроизвести файл.")

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.load_current_track()
            if self.is_playing: self.play()

    def prev_track(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.load_current_track()
            if self.is_playing: self.play()
    
    def get_current_track_name(self):
        if self.playlist:
            return os.path.basename(self.playlist[self.current_index])
        return "No tracks found"