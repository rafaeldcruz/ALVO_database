import sys, json, winsound, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer



class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A.L.V.O.")
        self.setGeometry(450, 200, 500, 400)
        self.setWindowIcon(QIcon(resource_path("alvo_icon.png")))
        self.textbox = QLineEdit()
        self.label = QLabel()
        self.pixmap = QPixmap(resource_path("ascii-alvo.png"))
        self.layout = QVBoxLayout()
        self.label_titulo_ano = QLabel()
        self.label_dados_ano = QLabel()
        
        with open(resource_path("catalogo.json"), "r", encoding="utf-8") as arquivo:
            self.log = json.load(arquivo)
        
        self.iniciar()


    def iniciar(self):
        self.setStyleSheet("""QMainWindow {
                            background-color: black;
                            }""")
        self.label.setStyleSheet("background-color: black")
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        self.label.setWordWrap(True)

        central = QWidget()
        self.setCentralWidget(central)
    
        self.layout.addWidget(self.label)
        self.layout.setAlignment(Qt.AlignCenter)
        central.setStyleSheet("""background-color: black;""")

        central.setLayout(self.layout)

        QTimer.singleShot(1000, self.remover_img)


    def remover_img(self):

        winsound.PlaySound(resource_path("ALVO.wav"), winsound.SND_FILENAME)

        self.label.setPixmap(QPixmap())
        self.setStyleSheet("""QLabel{
                           font-size: 30px;
                           font-family: Consolas;
                           color: #3cab30;
                           }""")
        
        self.label.setText("Insira o código da anomalia:")
        self.label.setAlignment(Qt.AlignCenter)

        self.TextBox()


    def TextBox(self):
        self.layout.addWidget(self.textbox)
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setFont(QFont("Consolas", 30))
        self.textbox.setPlaceholderText("____")

        self.textbox.returnPressed.connect(self.enviar)

        self.textbox.setStyleSheet("""color: #3cab30;
                                   border: none;""")
        

    def enviar(self):
        codigo = self.textbox.text().zfill(4)
        print(codigo)
        

        if codigo in self.log:
            
            dados = self.log[codigo]
            self.layout.addWidget(self.label_titulo_ano)
            self.layout.addWidget(self.label_dados_ano)

            self.layout.insertWidget(0, self.label_titulo_ano)
            self.layout.insertWidget(1, self.label_dados_ano)

            self.label_titulo_ano.setScaledContents(True)
            self.label_dados_ano.setWordWrap(True)
            self.label_titulo_ano.setStyleSheet("""font-size: 25px;
                                                padding: 20px""")
            self.label_dados_ano.setStyleSheet("""font-size: 18px;""")
            self.label_dados_ano.setAlignment(Qt.AlignLeft)
            self.label_titulo_ano.setAlignment(Qt.AlignCenter)
            self.label_titulo_ano.setScaledContents(True)
            self.label_dados_ano.setScaledContents(True)
            
            

            self.label_titulo_ano.setText(dados["titulo"])
            self.label_dados_ano.setText(dados["texto"])
            self.label.setText("")
            

        else:
          self.label.setAlignment(Qt.AlignCenter)
          self.label.setText("Anomalia não encontrada.")

        self.textbox.setText("")
        
def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        # Quando estiver rodando como .exe pelo PyInstaller
        base_path = sys._MEIPASS
    else:
        # Quando estiver rodando o .py pelo VSCode
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.showMaximized()
    sys.exit(app.exec_())




if __name__ == "__main__":
    main()

#Por no cmd para criar o executável:
#cd A.L.V.O
#py -3.12 -m PyInstaller --clean --onefile --windowed --icon=alvo_icon.ico  --add-data "catalogo.json;." --add-data "ALVO.wav;." --add-data "ascii-alvo.png;." ALVO.py
#arrumar o de cima para ser uma linha contínua