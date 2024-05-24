from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from PIL import Image, ImageFilter
from threading import Thread

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
            'image': Converter().convert_image,
            'document': Converter().convert_document,
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

        self.DroppableDocumentArea.setAcceptDrops(True)
        self.DroppableDocumentArea.dragEnterEvent = self.handleDragEnterEvent
        self.DroppableDocumentArea.dropEvent = self.dropEvent

        self.ConvertVideoButton.clicked.connect(lambda: self.navigate_to(1))
        self.ConvertAudioButton.clicked.connect(lambda: self.navigate_to(2))
        self.ConvertImagesButton.clicked.connect(lambda: self.navigate_to(3))
        self.ConvertDocumentButton.clicked.connect(lambda: self.navigate_to(4))

        self.back_from_audio.clicked.connect(lambda: self.navigate_to(0))
        self.back_from_video.clicked.connect(lambda: self.navigate_to(0))
        self.back_from_image.clicked.connect(lambda: self.navigate_to(0))
        self.back_from_document.clicked.connect(lambda: self.navigate_to(0))

        self.ConvertVideo.clicked.connect(lambda: self.convert('video', self.VideoFormats, [self.separateAudio]))
        self.ConvertImage.clicked.connect(lambda: self.convert('image', self.ImageFormats, [self.upscale2x, self.upscale4x]))
        self.ConvertAudio.clicked.connect(lambda: self.convert('audio', self.AudioFormats))
        self.convertDocument.clicked.connect(lambda: self.convert('document', self.documentFormats, [self.document_file_name]))

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

        if checkboxes is None:
            additional_data = None
            output_path = None
        
        elif any(isinstance(x, QLineEdit) for x in checkboxes):
            output_path = QFileDialog.getExistingDirectory(caption="Selecione a pasta de destino: ")
            additional_data = checkboxes[0].text()

        elif checkboxes:
            additional_data = {checkbox.text(): checkbox.isChecked() for checkbox in checkboxes}
            output_path = None


        files = self.dropped_files
        convert_to = [conversion_table.itemAt(i).widget().text() for i in range(conversion_table.count()) if conversion_table.itemAt(i).widget().isChecked()][0]

        res = self.Converter[conversion_type](files, convert_to, additional_data, output_path)

        if res:
            dialog = QMessageBox()
            dialog.setIcon(QMessageBox.Information)
            dialog.setWindowTitle("Sucesso")
            dialog.setText("Operação concluída!")
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.exec_()

        self.wipe_all_fields()
    
    def wipe_all_fields(self):
        for i in range(self.VideoFormats.count()):
            self.VideoFormats.itemAt(i).widget().setChecked(False)

        for i in range(self.AudioFormats.count()):
            self.AudioFormats.itemAt(i).widget().setChecked(False)

        for i in range(self.ImageFormats.count()):
            self.ImageFormats.itemAt(i).widget().setChecked(False)

        for i in range(self.documentFormats.count()):
            self.documentFormats.itemAt(i).widget().setChecked(False)
            
        self.dropped_files = []

        self.youtubeURL.setText("")
        self.document_file_name.setText("")

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
