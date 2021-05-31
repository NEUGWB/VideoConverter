import tkinter as tk
import re
import os

root = tk.Tk()

tk.Label(root, text='目录').grid(row=0, sticky=tk.N)
path = tk.Entry(root)
path.grid(row=0, column=1, sticky=tk.N)

tk.Label(root, text='后缀').grid(row=1, sticky=tk.N)
ext = tk.Entry(root)
ext.grid(row=1, column=1, sticky=tk.N)

tk.Label(root, text='正则').grid(row=2, sticky=tk.N)
reg = tk.Entry(root)
reg.grid(row=2, column=1, sticky=tk.N)

tk.Label(root, text='输出').grid(row=3, sticky=tk.N)
out = tk.Entry(root)
out.grid(row=3, column=1, sticky=tk.N)
out.insert(tk.END, '$0')


def Run():
    try:
        InnerRun()
    except Exception as e:
        print(str(e))
        result.clear()


result = []


def InnerRun():
    result.clear()
    info.delete(1.0, tk.END)
    e, p, r, o = ext.get(), path.get(), reg.get(), out.get()
    unique = {}
    for f in os.listdir(p):
        if f.endswith(e):
            pat = re.compile(r)
            search = pat.search(f)
            print(search, r, pat, f)
            if search:
                sg = search.groups()
                print(search.groups())
            else:
                print('regex search none', f)
                continue
            #result.append((f, search.group(0)))
            oo = o
            try:
                oo = oo.replace("$0", sg[0])
                oo = oo.replace("$1", sg[1])
                oo = oo.replace("$2", sg[2])
            except:
                pass
            print(f, oo)
            if oo in unique:
                raise Exception('not unique')
            else:
                unique[oo] = True

            src = os.path.join(p, f)
            dst = os.path.join(p, oo)
            _, ee = os.path.splitext(src)
            dst += ee
            result.append((src, dst))
    sres = ''
    result.sort(key=lambda x: x[0])
    for r in result:
        sres += r[0] + ' => ' + r[1] + '\n'
    info.insert(tk.END, sres)


def Ok():
    for r in result:
        os.rename(r[0], r[1])
    info.insert(tk.END, 'convert {0} files'.format(len(result)))
    result.clear()


def Clear():
    result.clear()
    info.delete(1.0, tk.END)
    info.insert(tk.END, tip)


btn = tk.Button(root, text='run', command=Run).grid(row=4, column=0, sticky=tk.N)
btn = tk.Button(root, text='ok', command=Ok).grid(row=4, column=1, sticky=tk.N)
btn = tk.Button(root, text='clear', command=Clear).grid(row=4, column=2, sticky=tk.N)

info = tk.Text(root, width=100, height=50, wrap=tk.NONE)
info.grid(row=0, column=2, rowspan=4, sticky=tk.N)

tip = '''帮助：
输出里面填写$i会被替换为正则提取的第i个group
i从0开始，最大为2
Run按钮会在这里显示重命名前后的文件名
点OK会真正执行
'''
Clear()

root.mainloop()
