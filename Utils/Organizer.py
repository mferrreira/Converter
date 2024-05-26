from pathlib import Path
import shutil
import os


class Organizer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.folders = {
            "documentos": ["pdf", "doc", "docx", "txt", "xlsx", "ppt", "pptx"],
            "imagens": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "svg"],
            "audios": ["mp3", "wav", "aac", "flac", "ogg"],
            "videos": ["mp4", "mkv", "flv", "avi", "mov", "wmv"]
        }
        self._create_folders()

    def _create_folders(self):
        for folder in self.folders:
            (self.base_path / folder).mkdir(exist_ok=True)

    def _get_file_type(self, file_extension):
        for folder, extensions in self.folders.items():
            if file_extension in extensions:
                return folder
        return None

    def organize_files(self):
        try:
            for item in self.base_path.iterdir():
                print(item)
                if item.is_file():
                    file_extension = item.suffix[1:].lower()
                    file_type = self._get_file_type(file_extension)
                    if file_type:
                        destination = self.base_path / file_type / item.name
                        shutil.move(str(item), str(destination))
            return True
        except Exception as e:
            return False