import vlc
import time


class AudioController():

    def __init__(self):
        self.sounds_path = "sounds/"

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.audio_set_volume(100)
        self.media_notes = {}
        self.setup_media()

    # настроить все музыкальные файлы
    def setup_media(self):
        self.media_tuning = self.instance.media_new(self.sounds_path + "tuning.m4a")
        self.media_notes["до"] = self.instance.media_new(self.sounds_path + "1 до.m4a")
        self.media_notes["ре"] = self.instance.media_new(self.sounds_path + "2 ре.m4a")
        self.media_notes["ми"] = self.instance.media_new(self.sounds_path + "3 ми.m4a")
        self.media_notes["фа"] = self.instance.media_new(self.sounds_path + "4 фа.m4a")
        self.media_notes["соль"] = self.instance.media_new(self.sounds_path + "5 соль.m4a")
        self.media_notes["ля"] = self.instance.media_new(self.sounds_path + "6 ля.m4a")
        self.media_notes["си"] = self.instance.media_new(self.sounds_path + "7 си.m4a")
        # настроить остальные 8 файлов

    # сыграть настройку
    def play_tuning(self):
        self.player.set_media(self.media_tuning)
        self.player.play()
        time.sleep(10)

    def play_note(self, note_name):
        self.player.set_media(self.media_notes[note_name])
        self.player.play()