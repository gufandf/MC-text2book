import unicodedata
from tkinter import *
from tkinter import filedialog
import pyperclip as pc

Content = ""


def get_width(Str):
    width = 0
    for c in Str:
        if unicodedata.east_asian_width(c) in ["F", "W", "A"]:
            width += 10
        else:
            width += 5
    return width


def translate(Title: str, Author: str):
    global Content
    Content = Content.split("\n")
    # print(Content)
    lines = []
    pages = []
    for p in Content:
        line = ""
        width = 208
        for c in p:
            if width < 0:
                lines.append(line)
                width = 208
                line = ""
            if unicodedata.east_asian_width(c) in ["F", "W", "A"]:
                width -= 18
            else:
                width -= 7
            line += c
        lines.append(line)
    while len(lines) > 13:
        pages.append(lines[0:14])
        lines = lines[14:]
    pages.append(lines)

    CPages = []
    pageCount = len(pages)
    for i in range(pageCount):
        print("--------------------{0}/{1}".format(i + 1, pageCount))
        text = ""
        for j in pages[i]:
            text += j + "\\n"
            print(j)
        CPages.append(
            '{{"text": "{0}"}}'.format(
                text.replace("'", "\\'")
                .replace('"', '\\"')
                .replace("\t", "\\t")
                .replace("　", "  ")
            )
        )
    return f'give @p written_book{{title:"{Title}",author:"{Author}",pages:{CPages}}}'


root = Tk()
root.title("文本转成书")
root.geometry("230x240")

text0 = Label(root, text="By Gufandf v0.1.0")
text0.pack()

text1 = Label(root, text="书名：")
text1.pack()
BookNameInput = Entry(root)
BookNameInput.pack(padx=5, pady=1, fill="x")

text2 = Label(root, text="署名：")
text2.pack()
AuthorInput = Entry(root)
AuthorInput.pack(padx=5, pady=1, fill="x")


def selectFile():
    global Content
    f = open(filedialog.askopenfilename(), "r", encoding="UTF-8")
    Content = f.read()


def outputFile():
    f = open(filedialog.asksaveasfilename(), "w", encoding="UTF-8")
    f.write(translate(BookNameInput.get(), AuthorInput.get()))
    print("Done")


def copy():
    pc.copy(translate(BookNameInput.get(), AuthorInput.get()))
    print("Done")


selectButton = Button(root, text="选择文件", command=selectFile)
selectButton.pack(padx=5, pady=5, fill="x")

button = Button(root, text="导出指令", command=outputFile)
button.pack(padx=5, pady=5, fill="x")

Copybutton = Button(root, text="复制指令", command=copy)
Copybutton.pack(padx=5, pady=5, fill="x")

root.mainloop()
