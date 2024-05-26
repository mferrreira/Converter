from moviepy.editor import VideoFileClip, AudioFileClip
from Utils.ErrorDialog import ErrorDialog
from pydub import AudioSegment

from docx import Document
from docx.shared import Inches
from pdf2docx import Converter as PDF2DocxConverter

from fpdf import FPDF

from PIL import Image

from PySide6.QtWidgets import QFileDialog

import os

class Converter:
    def __init__(self):
        ...

    def convert_image(self, files, convert_to, additional_data=None, *args):
        print(convert_to)
        for file_path in files:
            try:
                original_image = Image.open(file_path)

                if additional_data:
                    upscale_factor = 1
                    if "upscale 2x" in additional_data:
                        upscale_factor = 2
                    elif "upscale 4x" in additional_data:
                        upscale_factor = 4

                    new_size = (original_image.width * upscale_factor, original_image.height * upscale_factor)
                    resized_image = original_image.resize(new_size, Image.BICUBIC)
                else:
                    resized_image = original_image

                file_name, file_ext = os.path.splitext(file_path)
                output_file_path = f"{file_name}_{convert_to}{file_ext}"

                resized_image.save(output_file_path + f'.{convert_to.lower()}', format=convert_to.lower())

            except Exception as e:
                ErrorDialog.show_error_dialog("Erro", f"Erro ao converter a imagem {file_path}: {e}", "tente novamente!")
                return False
        
        return True
    
    def convert_video(self, files, convert_to, additional_data=None, *args):
        codec_mapping = {
            'mp4': 'libx264',
            'avi': 'libxvid',
            'webm': 'libvpx',
            'ogv': 'libtheora',
            'mov': 'libx264'
        }

        audio_codec_mapping = {
            'mp4': 'aac',
            'avi': 'libmp3lame',
            'webm': 'libvorbis',
            'ogv': 'libvorbis',
            'mov': 'aac'
        }
        
        for file_path in files:
            try:
                video_clip = VideoFileClip(file_path)
                
                file_name, file_ext = os.path.splitext(file_path)
                output_file_path = f"{file_name}_converted.{convert_to.lower()}"
                
                codec = codec_mapping.get(convert_to.lower(), None)
                audio_codec = audio_codec_mapping.get(convert_to.lower(), 'aac')

                if codec is None:
                    raise ValueError(f"Formato de vídeo não suportado: {convert_to}")
                
                video_clip.write_videofile(
                    output_file_path,
                    codec=codec,
                    audio_codec=audio_codec,
                    temp_audiofile=f"{file_name}_temp_audio.m4a",
                    remove_temp=False,
                    verbose=True,
                    threads=4
                )
                
                if additional_data and additional_data.get('Render Audio Separately', False):
                    audio_output_path = f"{file_name}_audio.mp3"
                    video_clip.audio.write_audiofile(audio_output_path)

            except Exception as e:
                ErrorDialog.show_error_dialog("Erro", f"Erro ao converter o vídeo {file_path}: {e}", "Tente Novamente")
                return False
        
        return True

    def convert_audio(self, files, convert_to, additional_data=None, *args):
        format_mapping = {
            'mp3': 'mp3',
            'wav': 'wav',
            'ogg': 'ogg',
            'flac': 'flac',
            'aac': 'aac'
        }

        for file_path in files:
            try:
                audio = AudioSegment.from_file(file_path)
                
                file_name, file_ext = os.path.splitext(file_path)
                output_file_path = f"{file_name}_converted.{convert_to.lower()}"
                
                format_to = format_mapping.get(convert_to.lower(), None)
                if format_to is None:
                    raise ValueError(f"Formato de áudio não suportado: {convert_to}")
                audio.export(output_file_path, format=format_to)

            except Exception as e:
                ErrorDialog.show_error_dialog("Erro", f"Erro ao converter o áudio {file_path}: {e}", "Verifique se o programa FFMPEG está corretamente instalado")
                return False

        return True
    
    def convert_document(self, files, convert_to, additional_data, output_path):
        try:
            if not files:
                ErrorDialog.show_error_dialog("Error", "No files provided for conversion.")
                return

            conversion = {
                'PDF': FPDF,
                'DOCX': Document,
            }

            document = conversion[convert_to]()

            # Handle image files
            if any(file.endswith((".png", ".jpg", ".jpeg", ".webp")) for file in files):
                if convert_to == 'PDF':
                    for file in files:
                        document.add_page()
                        document.image(file, x=10, y=10, w=190)  # Adjust as needed
                    output_file = os.path.join(output_path, f"{additional_data}.pdf")
                    document.output(output_file)
                elif convert_to == 'DOCX':
                    for file in files:
                        document.add_picture(file, width=Inches(2.0))  # Adjust as needed
                    output_file = os.path.join(output_path, f"{additional_data}.docx")
                    document.save(output_file)

            # Handle document file conversion
            elif all(file.endswith(".pdf") for file in files) and convert_to == 'DOCX':
                docx = Document()
                for pdf_file in files:
                    # This is a placeholder; PDF to DOCX conversion needs proper handling
                    docx.add_paragraph(f"Content from {pdf_file}")
                output_file = os.path.join(output_path, f"{additional_data}.docx")
                docx.save(output_file)
            elif all(file.endswith(".docx") for file in files) and convert_to == 'PDF':
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for docx_file in files:
                    doc = Document(docx_file)
                    pdf.add_page()
                    for para in doc.paragraphs:
                        pdf.multi_cell(0, 10, para.text)
                output_file = os.path.join(output_path, f"{additional_data}.pdf")
                pdf.output(output_file)
            else:
                ErrorDialog.show_error_dialog("Error", "Unsupported file types or conversion types.")
                return
            
        except Exception as e:
            ErrorDialog.show_error_dialog("Conversion Error", str(e))