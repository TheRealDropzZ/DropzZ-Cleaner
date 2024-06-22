#__/\\\\\\\\\\\\_____________________________________________________________/\\\\\\\\\\\\\\\_        
 #_\/\\\////////\\\__________________________________________________________\////////////\\\__       
  #_\/\\\______\//\\\_______________________________/\\\\\\\\\__________________________/\\\/___      
   #_\/\\\_______\/\\\__/\\/\\\\\\\______/\\\\\_____/\\\/////\\\__/\\\\\\\\\\\_________/\\\/_____     
    #_\/\\\_______\/\\\_\/\\\/////\\\___/\\\///\\\__\/\\\\\\\\\\__\///////\\\/________/\\\/_______    
     #_\/\\\_______\/\\\_\/\\\___\///___/\\\__\//\\\_\/\\\//////________/\\\/________/\\\/_________   
      #_\/\\\_______/\\\__\/\\\_________\//\\\__/\\\__\/\\\____________/\\\/________/\\\/___________  
       #_\/\\\\\\\\\\\\/___\/\\\__________\///\\\\\/___\/\\\__________/\\\\\\\\\\\__/\\\\\\\\\\\\\\\_ 
        #_\////////////_____\///_____________\/////_____\///__________\///////////__\///////////////__

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QLabel
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

def run_command_as_admin(command):
    subprocess.run(f'powershell -Command "Start-Process cmd -ArgumentList \'/c {command}\' -Verb RunAs"', shell=True)

def optimize_all_drives():
    drives = subprocess.check_output("wmic logicaldisk get name", shell=True).decode().split()[1:]
    for drive in drives:
        run_command_as_admin(f'defrag {drive} /O')

class CommandGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DropzZ PC Cleaner')
        self.setFixedSize(400, 600)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.black))
        palette.setColor(QPalette.WindowText, QColor(Qt.white))
        self.setPalette(palette)

        layout = QVBoxLayout()

        heading = QLabel('DropzZ PC Cleaner')
        heading.setFont(QFont('Arial', 20))
        heading.setStyleSheet("color: white;")
        heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading)

        self.explorerButton = self.create_button('Explorer', 'taskkill /f /im explorer.exe && start explorer.exe', self.show_warning_dialog2)
        layout.addWidget(self.explorerButton)

        self.wingetButton = self.create_button('Winget', 'winget upgrade --all --include-unknown', self.show_warning_dialog1)
        layout.addWidget(self.wingetButton)

        self.healthButton = self.create_button('Health', 'DISM.exe /Online /Cleanup-image /RestoreHealth', self.show_warning_dialog3)
        layout.addWidget(self.healthButton)

        self.scanButton = self.create_button('Scan', 'sfc /scannow', self.show_warning_dialog4)
        layout.addWidget(self.scanButton)

        self.tempButton = self.create_button('Temp', 'del /s /q %temp%\\* && del /s /q C:\\Windows\\Temp\\* && del /s /q C:\\Windows\\Prefetch\\*', self.show_warning_dialog5)
        layout.addWidget(self.tempButton)

        self.optimizeButton = self.create_button('Optimieren', 'optimize_all_drives')
        self.optimizeButton.clicked.disconnect()
        self.optimizeButton.clicked.connect(optimize_all_drives)
        layout.addWidget(self.optimizeButton)

        self.restartButton = self.create_button('Neustart', 'shutdown /r /t 0', self.show_warning_dialog6)
        layout.addWidget(self.restartButton)

        self.setLayout(layout)

    def create_button(self, text, command, custom_action=None):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton:pressed {
                background-color: #555;
            }
        """)
        if custom_action:
            button.clicked.connect(lambda: custom_action(command))
        else:
            button.clicked.connect(lambda: run_command_as_admin(command))
        return button

    def show_warning_dialog1(self, command):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Warnung! WINGET FUNKTIONIERT NUR MIT WINDOWS11!!")
        msg.setInformativeText("Bevor du diese Schritte machst, vergewissere dich, dass dein Windows auf dem neuesten Stand ist und du all deine Updates gemacht hast!")
        msg.setWindowTitle("Warnung")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        result = msg.exec_()
        
        if result == QMessageBox.Ok:
            run_command_as_admin(command)

    def show_warning_dialog2(self, command):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Warnung! Dieser Prozess startet den Windows Explorer neu!")
        msg.setInformativeText("Nur ausführen, wenn du Probleme mit dem Windows Explorer hast!")
        msg.setWindowTitle("Warnung")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        result = msg.exec_()
        
        if result == QMessageBox.Ok:
            run_command_as_admin(command)

    def show_warning_dialog3(self, command):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Hier wird folgendes ausgeführt: DISM.exe /Online /Cleanup-image /RestoreHealth")
        msg.setInformativeText("Die Health-Funktion überprüft euren PC nach kaputten Dateien. Sie sorgt dafür, dass alle Windows-Ordner durchsucht werden und auftretende Fehler behoben werden.")
        msg.setWindowTitle("Hinweis")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        result = msg.exec_()
        
        if result == QMessageBox.Ok:
            run_command_as_admin(command)


    def show_warning_dialog4(self, command):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Hier wird folgendes ausgeführt: sfc /scannow")
        msg.setInformativeText("Ähnlich wie die Health-Funktion arbeitet der Scan. Hier werden korrupte Windows-Dateien gesucht, gefunden und für euch repariert.")
        msg.setWindowTitle("Hinweis")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        result = msg.exec_()
        
        if result == QMessageBox.Ok:
            run_command_as_admin(command)


    def show_warning_dialog5(self, command):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Hier werden alle Temporären Dateien auf deinem PC gelöscht!")
        msg.setInformativeText("Die Temp-Funktion leert alle Temp-Pfade von Windows, damit euer PC mehr Speicher hat und Anwendungen wieder flüssig laufen.")
        msg.setWindowTitle("Hinweis")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        result = msg.exec_()
        
        if result == QMessageBox.Ok:
            run_command_as_admin(command)


    def show_warning_dialog6(self, command):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Betätige diesen Button nur, wenn ALLE Schritte davor gemacht und erfolgreich beendet wurden!")
        msg.setInformativeText("Du bist fertig und dein PC wird nun neugestartet")
        msg.setWindowTitle("Warnung")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        result = msg.exec_()
        
        if result == QMessageBox.Ok:
            run_command_as_admin(command)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CommandGUI()
    ex.show()
    sys.exit(app.exec_())
