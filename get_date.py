from flask import Flask, render_template, request, redirect, url_for, jsonify, app
import os
from time import sleep
import pdfread
import es_pdf
import ES_init
from werkzeug.utils import secure_filename
from flask import send_file, send_from_directory
from flask import make_response
import json
from flask import send_from_directory

# 文件存放路径
PATH_UPLOAD = './static/upload'
# 限制上传文件格式
ALLOWED_EXTENSIONS = set(['pdf', 'PDF'])  

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 连接ES
es = ES_init.es_connect()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/up')
def upload():
    return render_template('up.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        # 取文件名,返回一个列表
        filename_list = list(request.files.keys())
        # print(filename)
        # 获得file
        for filename in filename_list:
            # print(filename)

            if allowed_file(filename):
                file = request.files[filename]
                # 默认的路径[要改的]
                # save_path = r'D:\search\input_pdf\out_pdfs'
                # filepath = os.path.split(os.path.realpath(__file__))[0]
                filepath = os.path.join(PATH_UPLOAD, filename)
                # filepath = './static/upload/'+filename
                file.save(filepath)
                sleep(1)
                text_list = []
                # 提取文本
                text_list = (pdfread.textread(filepath))
                # 提取摘要
                pdfread.pdfsimplify(text_list)
                abstract = pdfread.get_abstarct(text_list[0])
                # 组成doc
                doc = pdfread.es_pdf_doc(filename, '', '', abstract, text_list, '', '')
                # 向ES提供数据
                # es.index(index='pdf', document = doc)
                # print(doc)
                es_pdf.add_pdf_date(es, doc)
    return jsonify({'result': 'success'})


@app.route('/search', methods=['GET', 'POST'])
def get_search_str():
    if request.method == 'GET':
        # 获得GET方式提交的search_str
        search_str = (request.args.get('search_str'))
        # print(search_str)
        # 连接ES
        # es = ES_init.es_connect()
        # print(es)
        # 返回查找文档
        doc_list = es_pdf.pdfsearch_keyword(es, search_str)
        # print(type(doc_list))
        # print(doc_list)
        # 提取主机地址[下载地址]
        address = []
        for doc in doc_list:
            # print(doc)
            pdf_doc = doc['_source']
            # print(pdf_doc)
            address.append(pdf_doc['title'])
            # print(address)
            # ret_json = jsonify({"data": address})
            # print(type(ret_json))
        return jsonify({"data": address})


# @app.route("/download/<filename>", methods=['GET'])
# def download_file(filename):
#     # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
#     directory = os.getcwd()  # 假设在当前目录
#     response = make_response(send_from_directory(excel_path,
#                                                  filename.encode('utf-8').decode('utf-8'),
#                                                  as_attachment=True))response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
#     return response


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    print(filename)
    return app.send_static_file('upload/'+filename)

# @app.route('/upload/<filename>', methods=['GET'])
# def download(filename):
#     if request.method == "GET":
#         path = os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         print(path)
#         if path:
#             return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# @app.route('/download')
# def download():
#     filename = 'ENSITE_NAVX和双LAS_省略_左心房线性消融治疗阵发性心房颤动_陈明龙.pdf'
#     rv = send_file('./static/upload/ENSITE_NAVX和双LAS_省略_左心房线性消融治疗阵发性心房颤动_陈明龙.pdf', as_attachment=True, attachment_filename=filename)
#     rv.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
#     return rv


if __name__ == '__main__':
    app.run(debug=False, port=5000)
