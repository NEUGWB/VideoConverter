def File2Utf8(src, dest):
    import os, chardet
    tt = open(src, 'rb')
    enc = chardet.detect(tt.read())['encoding']
    if enc.lower().find('gb2312') != -1:
        enc = 'gbk'
    print(enc)
    tt.close()

    destTmp = dest + "tmp"
    t2 = open(src, 'r', encoding=enc, )
    tw = open(destTmp, 'w', encoding='utf-8')
    tw.write(t2.read(1024))

    t2.close()
    tw.close()
    if src == dest:
        os.remove(src)
    if os.path.isfile(dest):
        os.remove(dest)
    os.rename(destTmp, dest)

File2Utf8("d:\\tddownload\\aa1.ssa", "d:\\tddownload\\aa1.ssa")
