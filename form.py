import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout,
                             QGroupBox, QDialog, QVBoxLayout, QGridLayout, QListWidget, QFileDialog,
                             QTextEdit, QLabel, QFormLayout, QLineEdit, QComboBox, QCheckBox, QMessageBox,
                             QButtonGroup, QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("格式转换")
        ll = self.createLeftLayout()
        ml = self.createMidLayout()
        rl = self.createRightLayout()
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(ll)
        mainLayout.addLayout(ml)
        mainLayout.addLayout(rl)
        self.setLayout(mainLayout)

    def createLeftLayout(self):
        leftLayout = QVBoxLayout()
        fileList = QListWidget()
        leftLayout.addWidget(fileList)
        fileList.currentItemChanged.connect(self.on_SelectFileChange)
        self.lstFile = fileList

        btnAdd = QPushButton("添加")
        btnAdd.clicked.connect(self.on_btnAdd)
        leftLayout.addWidget(btnAdd)
        return leftLayout

    def createRightLayout(self):
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(QLabel("媒体信息"))

        self.mediaInfo = QTextEdit()
        self.mediaInfo.setReadOnly(True)
        rightLayout.addWidget(self.mediaInfo, 1)

        return rightLayout

    def createMidLayout(self):
        midLayout = QVBoxLayout()
        dl = QHBoxLayout()
        self.useDefault = QCheckBox("使用默认配置")
        self.useDefault.stateChanged.connect(self.on_useDefaultState)
        self.useDefault.setChecked(False)
        dl.addWidget(self.useDefault)
        self.editDefault = QPushButton("编辑默认配置")
        self.editDefault.clicked.connect(self.on_EditDefault)
        dl.addWidget(self.editDefault)
        midLayout.addLayout(dl)

        midLayout.addWidget(self.createVideoGroup())
        midLayout.addWidget(self.createAudioGroup())
        midLayout.addWidget(self.createSubtitleGroup())
        midLayout.addWidget(self.createOtherGroup())

        sl = QHBoxLayout()
        self.btnOk = QPushButton("确认")
        self.btnOk.clicked.connect(self.on_Ok)
        sl.addWidget(self.btnOk)
        self.btnHelp = QPushButton("帮助")
        self.btnHelp.clicked.connect(self.on_Help)
        sl.addWidget(self.btnHelp)
        midLayout.addLayout(sl)
        return midLayout

    def createVideoGroup(self):
        vg = QGroupBox("视频")
        vg.setCheckable(True)

        vl = QFormLayout()
        self.vEncoder = QComboBox()
        self.vEncoder.addItem("copy")
        self.vEncoder.addItem("libx264")
        self.vEncoder.addItem("libx265")
        vl.addRow("视频编码", self.vEncoder)

        self.vResolution = QLineEdit()
        vl.addRow("分辨率", self.vResolution)

        self.vCrf = QLineEdit()
        vl.addRow("CRF", self.vCrf)
        vg.setLayout(vl)
        return vg

    def createAudioGroup(self):
        ag = QGroupBox("音频")
        ag.setCheckable(True)
        al = QFormLayout()
        self.aEncoder = QComboBox()
        self.aEncoder.addItem("copy")
        self.aEncoder.addItem("aac")
        al.addRow("音频编码", self.aEncoder)

        self.aBitRate = QLineEdit()
        al.addRow("比特率kbps", self.aBitRate)

        self.aSampRate = QLineEdit()
        al.addRow("采样率", self.aSampRate)

        self.aStream = QLineEdit()
        al.addRow("音频流", self.aStream)
        ag.setLayout(al)
        return ag

    def createSubtitleGroup(self):
        sg = QGroupBox("字幕")
        sg.setCheckable(True)
        sl = QGridLayout()
        self.sFile = QRadioButton("字幕文件")
        sl.addWidget(self.sFile, 0, 0)
        self.sStream = QRadioButton("字幕流")
        sl.addWidget(self.sStream, 1, 0)
        sFileInfo = QLineEdit()
        sFileInfo.setText("视频路径.ass")
        sFileInfo.setReadOnly(True)
        sl.addWidget(sFileInfo, 0, 1)
        self.sStreamNum = QLineEdit()
        sl.addWidget(self.sStreamNum, 1, 1)

        self.sBtnGroup = QButtonGroup()
        self.sBtnGroup.addButton(self.sFile)
        self.sBtnGroup.addButton(self.sStream)
        self.sBtnGroup.buttonToggled.connect(self.on_SwitchSub)
        sg.setLayout(sl)
        return sg

    def createOtherGroup(self):
        og = QGroupBox("其他")
        og.setCheckable(True)
        og.setChecked(False)

        ol = QFormLayout()
        self.timeStart = QLineEdit()
        ol.addRow("开始", self.timeStart)

        self.timeEnd = QLineEdit()
        ol.addRow("结束", self.timeEnd)
        og.setLayout(ol)
        return og

    def on_btnAdd(self):
        ss = QFileDialog.getOpenFileName()
        print(type(ss))
        self.lstFile.addItem(ss[0])
        print("add")

    def on_SelectFileChange(self, cur, prev):
        if cur:
            print(cur.text())

    def on_Ok(self):
        cur = self.lstFile.currentItem()
        if cur:
            info = cur.text()
        else:
            info = "默认配置"
        QMessageBox.information(
            self, "OK", info + " 配置已保存", QMessageBox.Yes)

    def on_useDefaultState(self, state):
        print(state)

    def on_EditDefault(self):
        self.lstFile.setCurrentRow(-1)
        print("edit")

    def on_Help(self):
        print("help")

    def on_SwitchSub(self, obj, checked):
        print(obj.text(), checked)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
