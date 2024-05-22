from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QPushButton, QHBoxLayout, QGridLayout, QLineEdit, QRadioButton
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QIcon, QPixmap

from PIL import Image, ImageFilter

from Utils.Converter import Converter
from Utils.Downloader import YouTubeDownloader
from gui.NovoLayout_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.dropped_files = []
        self.Converter = {
            'video': Converter().convert_video,
            'audio': Converter().convert_audio,
            'image': Converter().convert_image
        }

        self.ConversionOptions.setCurrentIndex(0)

        self.DroppableAudioArea.setAcceptDrops(True)
        self.DroppableAudioArea.dragEnterEvent = self.handleDragEnterEvent
        self.DroppableAudioArea.dropEvent = self.dropEvent

        self.DroppableVideoArea.setAcceptDrops(True)
        self.DroppableVideoArea.dragEnterEvent = self.handleDragEnterEvent
        self.DroppableVideoArea.dropEvent = self.dropEvent

        self.DroppableImageArea.setAcceptDrops(True)
        self.DroppableImageArea.dragEnterEvent = self.handleDragEnterEvent
        self.DroppableImageArea.dropEvent = self.dropEvent

        self.ConvertVideoButton.clicked.connect(lambda: self.navigate_to(1))
        self.ConvertAudioButton.clicked.connect(lambda: self.navigate_to(2))
        self.ConvertImagesButton.clicked.connect(lambda: self.navigate_to(3))

        self.back_from_audio.clicked.connect(lambda: self.navigate_to(0))
        self.back_from_video.clicked.connect(lambda: self.navigate_to(0))
        self.back_from_image.clicked.connect(lambda: self.navigate_to(0))

        self.ConvertVideo.clicked.connect(lambda: self.convert('video', self.VideoFormats, [self.separateAudio]))
        self.ConvertImage.clicked.connect(lambda: self.convert('image', self.ImageFormats, [self.upscale2x, self.upscale4x]))
        self.ConvertAudio.clicked.connect(lambda: self.convert('audio', self.AudioFormats))

        self.downloadVideoFromYoutube.clicked.connect(self.downloadYoutubeVideo)


    def downloadYoutubeVideo(self):
        url = self.youtubeURL.text()
        options = [o.text().lower() for o in [self.downloadMP4, self.downloadMP3] if o.isChecked()]
        output_path = QFileDialog.getExistingDirectory(caption="Selecione a pasta de destino: ")

        if url and options and output_path:
            res = YouTubeDownloader().download_video(url, output_path, options)
            print(res)
        
        self.wipe_all_fields()

    def navigate_to(self, index):
        self.ConversionOptions.setCurrentIndex(index)

    def handleDragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            print(url)
            file_path = url.toLocalFile()
            self.dropped_files.append(file_path)

    def convert(self, conversion_type, conversion_table, checkboxes=None):
        
        additional_data = None

        if checkboxes:
            additional_data = {checkbox.text(): checkbox.isChecked() for checkbox in checkboxes}
        
        files = self.dropped_files
        convert_to = [conversion_table.itemAt(i).widget().text() for i in range(conversion_table.count()) if conversion_table.itemAt(i).widget().isChecked()][0]

        self.Converter[conversion_type](files, convert_to, additional_data)
            
        self.wipe_all_fields()
    
    def wipe_all_fields(self):
        for i in range(self.VideoFormats.count()):
            self.VideoFormats.itemAt(i).widget().setChecked(False)

        for i in range(self.AudioFormats.count()):
            self.VideoFormats.itemAt(i).widget().setChecked(False)

        for i in range(self.ImageFormats.count()):
            self.VideoFormats.itemAt(i).widget().setChecked(False)
            
        self.dropped_files = []
        self.youtubeURL.setText("")

        self.separateAudio.setChecked(False)
        self.upscale2x.setChecked(False)
        self.upscale4x.setChecked(False)
        self.separateAudio.setChecked(False)
        self.downloadMP3.setChecked(False)
        self.downloadMP4.setChecked(False)



def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
