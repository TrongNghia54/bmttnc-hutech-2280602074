import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPlainTextEdit, QLineEdit, QPushButton, QSpinBox
from ui.caesar import Ui_MainWindow # Đã sửa thành Ui_MainWindow để khớp với caesar.py của bạn
import requests

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "../platforms"

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow() # Khởi tạo với Ui_MainWindow
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        
        # Lấy giá trị từ txt_key (là QPlainTextEdit theo caesar.ui của bạn)
        key_value = self.ui.txt_key.toPlainText()

        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": key_value
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data["encrypted_message"]) # Sử dụng setPlainText cho QPlainTextEdit
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                error_message = response.text or "Error while calling API"
                QMessageBox.critical(self, "API Error", error_message)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Error: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")


    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        
        # Lấy giá trị từ txt_key (là QPlainTextEdit theo caesar.ui của bạn)
        key_value = self.ui.txt_key.toPlainText()

        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": key_value
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["decrypted_message"]) # Sử dụng setPlainText cho QPlainTextEdit
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                error_message = response.text or "Error while calling API"
                QMessageBox.critical(self, "API Error", error_message)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Error: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())