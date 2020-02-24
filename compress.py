#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "shangjinglong"
import wx
from PIL import Image
import os
from shutil import copyfile
from math import ceil


class Luban(object):
    def __init__(self, ignoreBy=102400, quality=60):
        self.ignoreBy = ignoreBy
        self.quality = quality

    def setPath(self, path):
        self.path = path

    def setTargetDir(self, foldername="target"):
        self.dir, self.filename = os.path.split(self.path)
        self.targetDir = os.path.join(self.dir, foldername)

        if not os.path.exists(self.targetDir):
            os.makedirs(self.targetDir)

        self.targetPath = os.path.join(self.targetDir, self.filename)

    def load(self):
        self.img = Image.open(self.path)
        if self.img.mode == "RGB":
            self.type = "JPEG"
        elif self.img.mode == "RGBA":
            self.type = "PNG"
        else:
            # 其他的图片就转成JPEG
            self.img == self.img.convert("RGB")
            self.type = "JPEG"

    def computeScale(self):
        # 计算缩小的倍数
        srcWidth, srcHeight = self.img.size
        srcWidth = srcWidth + 1 if srcWidth % 2 == 1 else srcWidth
        srcHeight = srcHeight + 1 if srcHeight % 2 == 1 else srcHeight

        longSide = max(srcWidth, srcHeight)
        shortSide = min(srcWidth, srcHeight)

        scale = shortSide / longSide
        if (scale <= 1 and scale > 0.5625):
            if (longSide < 1664):
                return 1
            elif (longSide < 4990):
                return 2
            elif (longSide > 4990 and longSide < 10240):
                return 4
            else:
                return max(1, longSide // 1280)
        elif (scale <= 0.5625 and scale > 0.5):
            return max(1, longSide // 1280)

        else:
            return ceil(longSide / (1280.0 / scale))

    def compress(self, targetPath="target"):
        self.setTargetDir(targetPath)
        # 先调整大小，再调整品质
        if os.path.getsize(self.path) <= self.ignoreBy:
            copyfile(self.path, self.targetPath)
        else:
            self.load()
            scale = self.computeScale()
            srcWidth, srcHeight = self.img.size
            cache = self.img.resize((srcWidth // scale, srcHeight // scale),
                                    Image.ANTIALIAS)
            cache.save(self.targetPath, self.type, quality=self.quality)


class Message:
    @staticmethod
    def show(word):
        dlg = wx.MessageDialog(None, word, u"操作提示", wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            pass
        dlg.Destroy()


class FileDrop(wx.FileDropTarget):
    def __init__(self, panel):
        wx.FileDropTarget.__init__(self)
        self.panel = panel

    def OnDropFiles(self, x, y, files):  # 当文件被拖入后，会调用此方法
        self.fileList = files

        dlg = wx.MessageDialog(None, '确定开始压缩选中图片吗？', "消息提示", wx.YES_NO | wx.ICON_QUESTION)
        tc = wx.TextCtrl(self.panel, -1, size=(350, 120), pos=(20, 100), value="", style=wx.TE_MULTILINE)
        tc.SetValue('\n'.join(str(n) for n in files))

        if dlg.ShowModal() == wx.ID_YES:
            try:
                dlg.Destroy()
                dialog = wx.DirDialog(None, '选择文件保存目录: ',
                                      style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

                if dialog.ShowModal() == wx.ID_OK:
                    dialog.Destroy()
                    compress = Luban(1024)
                    for file in self.fileList:
                        compress.setPath(file)
                        compress.compress(dialog.GetPath())

                Message.show("图片压缩完成")

            except Exception as e:
                Message.show(str(e))

        return True


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="图片压缩工具V1", size=(400, 300))
        panel = wx.Panel(self, -1)

        self.st = wx.StaticText(panel, label="把图片文件拖这里🤩")
        font = self.st.GetFont()
        font.PointSize += 20
        font = font.Bold()
        self.st.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.st, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 25))
        panel.SetSizer(sizer)

        self.fileDrop = FileDrop(panel)
        panel.SetDropTarget(self.fileDrop)

        self.CreateStatusBar()
        self.SetStatusText("Welcome to the new world!")


class MainApp(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show()
        self.frame.Center()
        return True


if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()
