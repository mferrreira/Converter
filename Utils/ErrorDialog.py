from PySide6.QtWidgets import QMessageBox

class ErrorDialog:
    @staticmethod
    def show_error_dialog(title, message, solution=None):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        
        if solution:
            error_dialog.setDetailedText(solution)

        error_dialog.exec_()
