from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QPushButton, QHBoxLayout, QGridLayout, QLineEdit
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QIcon, QPixmap

from PIL import Image, ImageFilter
# from gui.untitled_ui import Ui_MainWindow

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

        print(url, options, output_path)

    def navigate_to(self, index):
        self.ConversionOptions.setCurrentIndex(index)

    def handleDragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.dropped_files.append(file_path)

    def convert(self, conversion_type, conversion_table, checkboxes=None):
        
        additional_data = None

        if checkboxes:
            additional_data = {checkbox.text(): checkbox.isChecked() for checkbox in checkboxes}
        
        files = self.dropped_files
        convert_to = [conversion_table.itemAt(i).widget().text() for i in range(conversion_table.count()) if conversion_table.itemAt(i).widget().isChecked()][0]

        resp = self.Converter[conversion_type](files, convert_to, additional_data)

        if resp:
            self.dropped_files = []

        return
        

# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         self.droppable_area.setAcceptDrops(True)
#         self.droppable_area.dragEnterEvent = self.dragEnterEvent
#         self.droppable_area.dropEvent = self.dropEvent
#         self.pushButton.clicked.connect(self.convert_files)
#         self.Upscale.clicked.connect(self.upscale_images)

#         self.dropped_files = []
#         self.dropped_files_upscale = []

#         self.dropped_items.setLayout(QGridLayout())
#         self.dropped_items.layout().addWidget(QLabel("Drop files here"))

#         self.dropped_items_upscale.setLayout(QGridLayout())
#         self.dropped_items_upscale.layout().addWidget(QLabel("Drop files here"))

#         self.converter = Converter()

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.accept()
#         else:
#             event.ignore()

#     def dropEvent(self, event):
#         for url in event.mimeData().urls():
#             file_path = url.toLocalFile()
#             if file_path.endswith(('.mp4', '.avi', '.mkv')):
#                 self.dropped_files.append(file_path)
#                 self.add_file_button(file_path)

#             if file_path.endswith(('.png', '.jpg', '.jpeg')):
#                 self.dropped_files_upscale.append(file_path)
#                 self.add_file_button_upscale(file_path)

#     def add_file_button(self, file_path):
        
#         button = QPushButton(self)
#         button.setText(file_path.split('/')[-1])
#         icon = QIcon(QPixmap(":/icons/video_icon.png"))  
#         button.setIcon(icon)
#         button.setIconSize(QSize(100, 100))
#         button.setFlat(True)  

        
#         button.setStyleSheet(
#             """
#             QPushButton {
#                 background-color: #ddd; /* Light gray background */
#                 border: none; /* No border */
#                 padding: 5px; /* Add some padding */
#                 margin: 5px; /* Add some margin */
#                 text-align: left; /* Align text to the left */
#             }
#             QPushButton:hover {
#                 background-color: #ccc; /* Darker gray background on hover */
#             }
#             """
#         )

        
#         layout = self.dropped_items.layout()
#         row = layout.rowCount()
#         layout.addWidget(button, row, 0)

#     def add_file_button_upscale(self, file_path):
        
#         button = QPushButton(self)
#         button.setText(file_path.split('/')[-1])
#         icon = QIcon(QPixmap(":/icons/image_icon.png"))  
#         button.setIcon(icon)
#         button.setIconSize(QSize(100, 100))
#         button.setFlat(True)  

        
#         button.setStyleSheet(
#             """
#             QPushButton {
#                 background-color: #ddd; /* Light gray background */
#                 border: none; /* No border */
#                 padding: 5px; /* Add some padding */
#                 margin: 5px; /* Add some margin */
#                 text-align: left; /* Align text to the left */
#             }
#             QPushButton:hover {
#                 background-color: #ccc; /* Darker gray background on hover */
#             }
#             """
#         )

        
#         layout = self.dropped_items_upscale.layout()
#         row = layout.rowCount()
#         layout.addWidget(button, row, 0)

#     def convert_files(self):
#         output_folder = self.select_output_folder()
#         if not output_folder:
#             return

#         for file_path in self.dropped_files:
            
#             file_name = file_path.split('/')[-1]
#             output_file = f"{output_folder}/{file_name}.mp3"  
#             success, error_message = self.converter.convert_video_to_audio(file_path, output_file)
#             if success:
#                 print(f"Conversion successful: {file_path} -> {output_file}")
                
#             else:
#                 print(f"Conversion failed: {error_message}")
                

#     def select_output_folder(self):
#         folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
#         return folder_path  

#     def upscale_images(self):
#         output_folder = self.select_output_folder()
#         if not output_folder:
#             return

#         for file_path in self.dropped_files_upscale:
            
#             file_name = file_path.split('/')[-1]
#             output_file = f"{output_folder}/{file_name}_upscaled.png"  
#             success, error_message = self.converter.upscale_image(file_path, output_file, int(self.width.text()), int(self.height.text()))
#             if success:
#                 print(f"Upscaling successful: {file_path} -> {output_file}")
                
#             else:
#                 print(f"Upscaling failed: {error_message}")
                

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
