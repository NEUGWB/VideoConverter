import os, sys, uuid, shutil, platform

inputfile = sys.argv[1]
out = "juedoushi"

w=854
h=480
bvk=2000

a_stream = 0
s_stream = 0

bak = 96
ar = 44100

class ffparam:
    def __init__(self):
        self.input = ""

        self.w=0
        self.h=0
        self.vkbps=0

        self.a_stream = -1
        self.akbps = 0
        self.ar = 0
        
        self.s_stream = -1

def run():
    p = ffparam()
    p.input = "D:\TDDOWNLOAD\刺客聂隐娘.mp4"
    p.w = 1280
    p.h = 720
    p.vkbps = 2000
    p.a_stream = 0
    p.akbps = 128
    p.ar = 44100
    p.ac = 2
    p.s_stream = 1
    p.start = 0
    p.dur = 0
    
    uid = str(uuid.uuid1())
    
    filepathname = p.input
    filename, fileext = os.path.splitext(filepathname)
    _, filename = os.path.split(filepathname)

    print(filename, fileext)


    subtitle_name = uid+".ass"
    passlog_name = uid+"passlog"
    output_name = uid+"out.mp4"

    v_cmd = " -c:v libx264"
    if (p.w > 0 && p.h > 0):
        v_cmd += " -s {0}*{1}".format(p.w, p.h)
    if (p.vkbps > 0):
        v_cmd += " -b:v {0}k".format(p.vkbps)
    a_cmd = " -c:a acc"
    if (p.a_stream >= 0):
        a_cmd += " -map 0:0 -map 0:a:{0}".format(p.a_stream)
    if (p.akbps > 0)
        a_cmd += " -b:a {0}k".format(p.akbps)
    if (p.ar > 0):
        a_cmd += " -ar {0}".format(p.ar)
    if (p.ac > 0):
        a_cmd += " ac {0}".format(p.ac)
    s_cmd = ""
    if isinstance(p.s_stream, int) and p.s_stream >= 0:
        es_cmd = "ffmpeg -y -i \"{0}\" -map 0:s:{1} {2}".format(p.input, p.s_stream, subtitle_name)
        os.system(es_cmd)
    elif isinstance(p.s_stream, str):
        es_cmd = "ffmpeg -y -i \"{0}\" {1}".format(p.s_stream, subtitle_name)
        os.system(es_cmd)
    if os.path.isfile(subtitle_name):
        s_cmd += " -vf ass=\"{0}\" ".format(subtitle_name)
    
    ff_cmd = "ffmpeg -y -i \"{0}\" {1} {2} {3}".format(filepathname, v_cmd, a_cmd, s_cmd)
    if p.start > 0:
        ff_cmd += " -ss {0}".format(p.start)
    if p.dur > 0:
        ff_cmd += " -t {0}".format(p.dur)

    sysstr = platform.system()
    if sysstr == "Windows":
        nullfile = "NUL"
    else:
        nullfile = "/dev/null"

    p1_cmd = ff_cmd + " -pass 1 -passlogfile {0} -f mp4 {1}".format(passlog_name, nullfile)
    p2_cmd = ff_cmd + " -pass 2 -passlogfile {0} -f mp4 {1}".format(passlog_name, output_name)

    cmd = p1_cmd + "\n" + p2_cmd
    print('.....')
    print(cmd)

    os.system(p1_cmd)
    os.system(p2_cmd)

    try:
        os.rename(output_name, filename+"out.mp4")
        os.remove(subtitle_name)
        os.remove(passlog_name+"-0.log")
        os.remove(passlog_name+"-0.log.mbtree")
    except Exception as e:
        pass
