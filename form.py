import sys, os, traceback
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout,
                             QGroupBox, QDialog, QVBoxLayout, QGridLayout, QListWidget, QFileDialog,
                             QTextEdit, QLabel, QFormLayout, QLineEdit, QComboBox, QCheckBox, QMessageBox,
                             QButtonGroup, QRadioButton, QListWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import  Qt
from c import FFParam
import conf

class App(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()
        try:
            conf.load()
        except Exception as e:
            print('load error', str(e))
            traceback.print_exc()

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
        self.on_Help()

    def createLeftLayout(self):
        leftLayout = QVBoxLayout()
        fileList = QListWidget()
        leftLayout.addWidget(fileList)
        fileList.currentItemChanged.connect(self.on_SelectFileChange)
        self.fileList = fileList

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
        self.useDefault = QPushButton("加载配置")
        self.useDefault.clicked.connect(self.on_loadConf)
        dl.addWidget(self.useDefault)
        self.editDefault = QPushButton("保存配置")
        self.editDefault.clicked.connect(self.on_saveConf)
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
        self.vcodec = QComboBox()
        self.vcodec.addItem("libx264")
        self.vcodec.addItem("libx265")
        self.vcodec.addItem("copy")
        vl.addRow("视频编码", self.vcodec)

        self.vResolution = QLineEdit()
        vl.addRow("分辨率", self.vResolution)

        self.vFrameRate = QLineEdit()
        vl.addRow("帧率", self.vFrameRate)

        self.crf = QLineEdit()
        vl.addRow("CRF", self.crf)

        self.vkbps = QComboBox()
        vkb = ["设置后会覆盖crf", "750", "1000", "1500", "2000", "3000"]
        self.vkbps.addItems(vkb)
        vl.addRow("比特率kbps", self.vkbps)
        vg.setLayout(vl)
        self.vGroup = vg
        return vg

    def createAudioGroup(self):
        ag = QGroupBox("音频")
        ag.setCheckable(True)
        al = QFormLayout()
        self.acodec = QComboBox()
        self.acodec.addItems(["aac", "copy"])
        al.addRow("音频编码", self.acodec)

        self.aBitRate = QComboBox()
        self.aBitRate.addItems(["128", "192", "320"])
        self.aBitRate.setCurrentIndex(1)
        al.addRow("比特率kbps", self.aBitRate)

        self.aSampRate = QComboBox()
        self.aSampRate.addItems(["44100", "48000"])
        al.addRow("采样率", self.aSampRate)

        self.aStream = QLineEdit()
        al.addRow("音频流", self.aStream)
        ag.setLayout(al)
        self.aGroup = ag
        return ag

    def createSubtitleGroup(self):
        sg = QGroupBox("字幕")
        sg.setCheckable(True)
        sg.setChecked(False)
        sl = QGridLayout()
        self.sFile = QRadioButton("字幕文件")
        sl.addWidget(self.sFile, 0, 0)
        self.sStream = QRadioButton("字幕流")
        sl.addWidget(self.sStream, 1, 0)
        sFileInfo = QLabel("与视频同路径同名")
        sl.addWidget(sFileInfo, 0, 1)
        self.sStreamNum = QLineEdit()
        sl.addWidget(self.sStreamNum, 1, 1)

        self.sFormat = QComboBox()
        self.sFormat.addItems(["ass", "pgs"])
        sl.addWidget(QLabel("字幕格式"), 2, 0)
        sl.addWidget(self.sFormat, 2, 1)

        self.sBtnGroup = QButtonGroup()
        self.sBtnGroup.addButton(self.sFile)
        self.sBtnGroup.addButton(self.sStream)
        self.sFile.setChecked(True)
        self.sBtnGroup.buttonToggled.connect(self.on_SwitchSub)
        sg.setLayout(sl)
        self.sGroup = sg
        return sg

    def createOtherGroup(self):
        og = QGroupBox("其他")
        og.setCheckable(True)
        og.setChecked(False)

        ol = QFormLayout()
        self.timeStart = QLineEdit()
        ol.addRow("开始", self.timeStart)

        self.timeSpan = QLineEdit()
        ol.addRow("时长", self.timeSpan)
        og.setLayout(ol)

        self.outFormat = QComboBox()
        formats = ["", "mp4", "avi", "aac", "gif"]
        self.outFormat.addItems(formats)
        ol.addRow("输出格式", self.outFormat)
        self.oGroup = og
        return og

    def on_btnAdd(self):
        ss = QFileDialog.getOpenFileNames(directory=conf.get_path())[0]
        path = ''
        for fs in ss:
            item = QListWidgetItem()
            self.fileList.addItem(item)
            path, fname = os.path.split(fs)
            item.setText(fname)
            item.setData(Qt.UserRole, fs)
            item.setToolTip(fs)
            print(fs)
        if path:
            conf.set_path(path)

    def on_SelectFileChange(self, cur, prev):
        pass

    def on_Ok(self):
        self.mediaInfo.clear()
        ff = self.toFFparam()
        
        infiles = []
        for i in range(0, self.fileList.count()):
            cur = self.fileList.item(i)
            infiles.append(cur.data(Qt.UserRole))
        if not infiles:
            infiles.append("<in-file>")
        for infile in infiles:
            for s in ff.cmds(infile):
                print(s)
                self.mediaInfo.append(s)
            self.mediaInfo.append('\n')

    def toFFparam(self):
        ff = FFParam()
        ff.infile = "<input-file>"
        ff.v = self.vGroup.isChecked()
        ff.vcodec = self.vcodec.currentText()
        ff.resolution = self.vResolution.text()
        ff.nframe = int(self.vFrameRate.text() or -1)
        ff.crf = int(self.crf.text() or -1)
        ff.vkbps = int(self.vkbps.currentText() if
                       self.vkbps.currentIndex() != 0 else "0")

        ff.a = self.aGroup.isChecked()
        ff.astream = int(self.aStream.text() or -1)
        ff.acodec = self.acodec.currentText()
        ff.akbps = int(self.aBitRate.currentText() or 0)
        ff.ar = int(self.aSampRate.currentText() or 0)

        ff.s = self.sGroup.isChecked()
        if self.sFile.isChecked():
            ff.sfile = True
            ff.sstream = -1
        elif self.sStream.isChecked():
            ff.sstream = int(self.sStreamNum.text() or 0)
            ff.sfile = ""
        ff.sformat = self.sFormat.currentText()

        ff.clip = self.oGroup.isChecked()
        ff.ss = self.timeStart.text()
        ff.t = self.timeSpan.text()
        ff.outformat = self.outFormat.currentText()

        return ff

    def fromFFparam(self, ff):
        self.vGroup.setChecked(ff.v)
        vcodecIndex = self.vcodec.findText(ff.vcodec)
        if vcodecIndex < 0:
            vcodecIndex = 0
        self.vcodec.setCurrentIndex(vcodecIndex)

        if ff.resolution:
            self.vResolution.setText(ff.resolution)

        if ff.nframe > 0:
            self.vFrameRate.setText(str(ff.nframe))
        else:
            self.vFrameRate.setText("")
        if ff.crf > 0:
            self.crf.setText(str(ff.crf))

        vkbpsIndex = self.vkbps.findText(str(ff.vkbps))
        if vkbpsIndex > 0:
            self.vkbps.setCurrentIndex(vkbpsIndex)
        else:
            self.vkbps.setCurrentIndex(0)

        self.aGroup.setChecked(ff.a)
        acodecIndex = self.vcodec.findText(ff.acodec)
        if acodecIndex < 0:
            acodecIndex = 0
        self.acodec.setCurrentIndex(acodecIndex)
        if ff.astream >= 0:
            self.aStream.setText(str(ff.astream))
        else:
            self.aStream.setText("")
        arIndex = self.aSampRate.findText(str(ff.ar))
        arIndex = arIndex if arIndex >= 0 else 0
        self.aSampRate.setCurrentIndex(arIndex)
        akbpsIndex = self.aBitRate.findText(str(ff.akbps))
        akbpsIndex = akbpsIndex if akbpsIndex >= 0 else 0
        self.aBitRate.setCurrentIndex(akbpsIndex)

    def on_loadConf(self):
        self.fromFFparam(conf.get_ff())

    def on_saveConf(self):
        conf.set_ff(self.toFFparam())
        conf.save()

    def on_Help(self):
        self.mediaInfo.setText(tips)

    def on_SwitchSub(self, obj, checked):
        print(obj.text(), checked)

tips = '''
·把界面转化成ffmpeg命令
·点确定之后在这里会显示命令，自己粘贴到sh或bat里执行
·分辨率写法：1280x720，1280:720，-2:720，1280:-2，iw*0.5:wh:0.5
·字幕格式自己去看文件后缀名，或者ffmpeg -i查看
·设置视频比特率会采用2-pass压缩，crf无效

·不保证正确，但是不会删你的文件（理论上）
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
