import fitz
import os
import re
import json
path = r'D:\search\input_pdf\input_pdfs'


def pathread(path, pdffiles):
    """path下的pdf文件(每个pdf的根目录）"""
    files = os.listdir(path)
    # 文件夹下的文件
    # print(files)
    for file in files:
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            pdffiles.append(file_path)
        elif os.path.isdir(file_path):
            pathread(file_path)


def textread(filepath):
    """根据pdf的路径,返回text_list（单个pdf的文本列表）,以一页为一个元素"""
    text_list = []
    if os.path.isfile(filepath):
        pdf = fitz.open(filepath)
    else:
        print("path is error!")
        return -1
    for page in pdf:
        text = page.get_text()
        if len(text) != 0:
            text_list.append(text)
    return text_list


def simplify(text):
    """删除空格，换行"""
    tem = re.sub("[\s]*", "", text)
    return tem


def pdfsimplify(text_list):
    """对整个pdf删除空格，换行"""
    for index in range(0, len(text_list)):
        text_list[index] = simplify(text_list[index])
    return 0


def get_abstarct(text):
    """提取摘要"""
    mat = re.search("摘要(.*)关键词.*?", text, flags=0).span()
    # print(text[mat[0]:mat[1]])
    text = text[mat[0]:mat[1]]
    text = re.sub("摘要|关键词", "", text)
    return text


def pdf_address(title, path):
    """构建pdf的主机路径"""
    pdf_name = title+".pdf"
    return os.path.join(path, pdf_name)


def es_pdf_doc(title, author, keyword, abstract, content, images_text, address):
    """构建文档"""
    doc = {
        "title": title,
        "author": author,
        "key_word": keyword,
        "abstract": abstract,
        "content_text": content,
        "images_text": images_text,
        "address": address
    }
    return doc

