import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.foldername = ''        # 분해된 파일을 저장할 위치
        self.filename = ''          # 분해할 파일의 이름
        self.max_name_len = 55      # 파일 이름이 길 경우 줄여주기 위한 최대 파일 길이

    def initUI(self):
        self.setWindowTitle("txt divider - 광운대 소프트 18 박우성")
        self.select_file_button.clicked.connect(self.fileopen)
        self.select_folder_button.clicked.connect(self.folderopen)
        self.divide_file_button.clicked.connect(self.divide_txt)


    def fileopen(self):
        """
        파일을 열어 해당 디렉토리를 self.filename에 저장한다
        파일의 길이에 따라 줄일지 말지를 결정하여 filename을 label 에 출력한다
        """
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', "", "txt file (*.txt)")[0]
        if self.filename:
            filename_len = len(self.filename)
            if filename_len > self.max_name_len:
                self.filename_label.setText('...' + self.filename[-self.max_name_len:])
            else:
                self.filename_label.setText(self.filename)
            self.get_line_num(self.filename)
            self.line_num_label.setText('Line : ' + str(self.line_num))

    def folderopen(self):
        """
        폴더를 열어 해당 디렉토리를 self.foldername에 저장한다
        폴더의 길이에 따라 줄일지 말지를 결정하여 foldername을 label 에 출력한다
        """
        self.foldername = QFileDialog.getExistingDirectory(self, "Select Directory")
        foldername_len = len(self.foldername)
        if foldername_len > self.max_name_len:
            self.foldername_label.setText('...' + self.foldername[-self.max_name_len:])
        else:
            self.foldername_label.setText(self.foldername[-self.max_name_len:])

    def get_line_num(self, filename):
        """
        파일을 얻어 그 파일이 몇개의 줄로 이루어져있는지 얻어내어
        self.line_num 에 저장한다
        """
        f_r = open(filename, encoding='utf-8')
        text = f_r.read()
        lines = text.split('\n')
        f_r.close()
        self.line_num = len(lines)

    def divide_txt(self):
        """
        파일을 얻어 해당 파일의 line들을 line별로 분류하여 XXX_XXXX.txt 형식으로 저장한다.
        """

        # 파일 혹은 폴더를 선택하지 않았을 경우 확인 팝업을 내보낸다.
        if not self.filename or not self.foldername:
            self.show_popup('Wrong', '파일과 폴더를 선택했는지 확인해주세요.', icon=QMessageBox.Icon.Warning)
            return

        # 확인을 요구하는 팝업으로 파일이 덮어씌워지는 불상사를 방지한다 Ok 버튼을 클릭하면 진행된다
        notice_str = '해당 폴더에 만들어질 파일과 같은 이름의 파일이 있는지 확인해주세요.\n해당 파일을 덮어버릴 수 있습니다. (빈 폴더를 추천합니다)\n해당 사항을 확인하였으면 Ok\n다시 확인이 필요하면 Cancel 버튼을 눌러주세요.'
        result = self.show_popup('Notice', notice_str, standard_button=QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
        if result == QMessageBox.StandardButton.Cancel:
            return

        # 파일을 open하여 line별로 지정된 형식에 따라 txt파일을 만든다.
        f_r = open(self.filename, encoding='utf-8')
        file_num = self.file_number_spin.value()
        start_num = self.start_number_spin.value()
        text = f_r.read()
        lines = text.split('\n')

        for line in lines:
            f_w = open(self.foldername + '/' + str(file_num).zfill(3)+'_'+str(start_num).zfill(4)+'.txt', 'w')
            f_w.write(line)
            f_w.close()
            start_num += 1
        f_r.close()
        self.show_popup('Finish', str(self.line_num) +'줄의 txt 파일 분해가 완료되었습니다.')

    def show_popup(self, title:str, content:str, icon=QMessageBox.Icon.NoIcon, standard_button=QMessageBox.StandardButton.Ok):
        """
        팝업을 내보내는 함수
        :param title: 팝업 제목
        :param content: 팝업 내용
        :param icon: 팝업에 사용될 아이콘
        :param standard_button: 팝업에 사용될 버튼
        :return: 눌러진 버튼
        """
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.setStandardButtons(standard_button)
        return msg.exec()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec()