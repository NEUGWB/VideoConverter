import os
import sys
import uuid
import shutil
import platform
import uuid


class FFParam:
    def __init__(self):
        self.uuid = str(uuid.uuid1())[:8]
        self.infile = ""

        self.v = True
        self.vcodec = ""
        self.w = -1
        self.h = -1
        self.nframe = -1
        self.crf = -1
        self.vkbps = -1

        self.a = True
        self.acodec = ""
        self.akbps = 0
        self.ar = 0
        self.ac = 0
        self.astream = -1

        self.s = False
        self.sstream = -1
        self.sfile = ""
        self.sformat = "ass"

        self.clip = False
        self.ss = ""
        self.t = ""

    def cmds(self):
        sscmd = ""
        in_file = os.path.normpath(self.infile)
        cmd = "ffmpeg -y -i \"" + in_file + "\" "
        if self.v:
            if self.vcodec:
                cmd += "-c:v {0} ".format(self.vcodec)
            if self.w > 0 and self.h > 0:
                cmd += "-s {0}x{1} ".format(self.w, self.h)
            if self.nframe > 1:
                cmd += "-r {0} ".format(self.nframe)
            if self.vkbps > 0:
                cmd += "-b:v {0}k ".format(self.vkbps)
            elif self.crf > 0:
                cmd += "-crf {0} ".format(self.crf)
        if self.a:
            if self.acodec:
                cmd += "-c:a {0} ".format(self.acodec)
            if self.astream >= 0:
                cmd += "-map 0:a:{0} -map 0:v:0 ".format(self.astream)
            if self.akbps > 0:
                cmd += "-b:a {0}k ".format(self.akbps)
            if self.ar > 0:
                cmd += "-ar {0} ".format(self.ar)
            if self.ac > 0:
                cmd += "-ac {0} ".format(self.ac)

        if self.s:
            subfile = self.uuid + "." + self.sformat
            if self.sstream >= 0 and self.sformat != 'pgs':
                sscmd = "ffmpeg -y -i \"{0}\" -map 0:s:{1} {2} ".format(
                        in_file, self.sstream, subfile)
            elif self.sfile:
                fn, ext = os.path.splitext(in_file)
                fn += "." + self.sformat
                cpcmd = "copy /y " if platform.system() == "Windows" else "cp -f "
                sscmd = "{0} \"{1}\" \"{2}\" ".format(cpcmd, os.path.normpath(fn), subfile)

            if self.sformat == "ass":
                cmd += "-vf ass={0} ".format(subfile)
            elif self.sformat == "srt":
                cmd += "-vf \"subtitles={0}:force_style='Fontsize=22'\" ".format(
                    subfile)
            elif self.sformat == "pgs":
                cmd += "-filter_complex \"[0:v][0:s:{0}]overlay[v]\" -map \"[v]\" ".format(
                    self.sstream)
        if self.clip:
            if self.ss:
                cmd += "-ss " + self.ss + ' '
            if self.t:
                cmd += "-t " + self.t + ' '

        if not self.outformat:
            if self.v:
                self.outformat = "mp4"
            elif self.a:
                self.outformat = self.acodec
        cmd += "-f " + self.outformat + " "
        


        path, fname = os.path.split(self.infile)
        fname, ext = os.path.splitext(fname)
        out_file = os.path.normpath(fname + "_out." + self.outformat)

        if self.vkbps > 0:
            sysstr = platform.system()
            if sysstr == "Windows":
                nullfile = "NUL"
            else:
                nullfile = "/dev/null"
            passlog_name = self.uuid
            pass1_cmd = cmd + " -pass 1 -passlogfile {0} {1} ".format(passlog_name, nullfile)
            pass2_cmd = cmd + " -pass 2 -passlogfile {0} \"{1}\" ".format(passlog_name, out_file)
            ret = [sscmd, pass1_cmd, pass2_cmd]
        else:
            cmd += '"' + out_file + '"'
            ret = [sscmd, cmd]
        return [s for s in ret if s]


def run():

    sysstr = platform.system()
    if sysstr == "Windows":
        nullfile = "NUL"
    else:
        nullfile = "/dev/null"

    p1_cmd = ff_cmd + \
        " -pass 1 -passlogfile {0} {1}".format(passlog_name, nullfile)
    p2_cmd = ff_cmd + \
        " -pass 2 -passlogfile {0} {1}".format(
            passlog_name, output_name)

    cmd = p1_cmd + "\n" + p2_cmd
    print('.....')
    print(cmd)

    os.system(p1_cmd)
    os.system(p2_cmd)

    try:
        os.rename(output_name, filename+"out.mkv")
        os.remove(subtitle_name)
        os.remove(passlog_name+"-0.log")
        os.remove(passlog_name+"-0.log.mbtree")
    except Exception as e:
        pass
