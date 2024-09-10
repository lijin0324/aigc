import pymysql
import os
import requests
import base64
import json
import time
from auth_util import gen_sign_headers
from flask_cors import CORS
from flask import Flask, request, jsonify


app= Flask(__name__)
CORS(app)

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='dbsclab2018',
    charset='utf8')

# 请注意替换APP_ID、APP_KEY
APP_ID = '3031779157'
APP_KEY = 'YPnAPPbxNETDqYMT'
URI = '/api/v1/task_submit'
URI2 = '/api/v1/task_progress'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'
METHOD2 = 'GET'


prompt = ""

@app.route('/receive_data2', methods=['POST', 'GET'])
def receive_data():
    if request.method == 'POST':
        data = request.json  # 获取来自前端的 JSON 数据
        user_input = data.get('message')  # 提取用户输入的消息

        if user_input:
            # 调用与 AI 进行对话的函数
            ai_response = progress(user_input)

            # 将包含对话历史和当前回复的 JSON 数据发送给前端
            return jsonify({'response': ai_response})
        else:
            return jsonify({'error': 'No message provided'}), 400
    else:
        return 'This endpoint only accepts POST requests.', 405


def submit(user_input):
    params = {}
    data = {
        'height': 768,
        'width': 576,
        'prompt': user_input,
        'styleConfig': '55c682d5eeca50d4806fd1cba3628781'
    }

    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    headers['Content-Type'] = 'application/json'

    url = 'http://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        result = response.json()['result']
        if result:
            task_id = result.get('task_id')
            if task_id:
                return task_id
            else:
                print("No task_id found in the response.")
        else:
            print(result)
            print("Empty result dictionary returned.")
    else:
        print(response.status_code, response.text)


def get_task_progress(task_id):
    params = {
        'task_id': task_id
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD2, URI2, params)

    uri_params = '&'.join(f'{key}={value}' for key, value in params.items())
    url = 'http://{}{}?{}'.format(DOMAIN, URI2, uri_params)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code, response.text)
        return None


def progress(user_input):
    task_id = submit(user_input)
    if not task_id:
        print("Task submission failed.")
        return

    max_attempts = 60  # 最大轮询次数，避免死循环
    attempts = 0

    while attempts < max_attempts:
        result = get_task_progress(task_id)
        if result and result['code'] == 200:
            task_result = result['result']
            if task_result['finished']:
                # print("Task finished. Result:", task_result)
                # 提取图片 URL
                images_url = task_result.get('images_url', [])
                if images_url:
                    return images_url
                else:
                    print("No images URL found in the result.")
                break
            else:
                eta = task_result.get('task_eta', 10)
                # print(f"Task not finished. ETA: {eta} seconds")
                time.sleep(min(eta, 5))  # 动态调整等待时间，避免频繁请求
                attempts += 1
        else:
            print("Failed to get task progress.")
            break
    else:
        print("Max attempts reached. Task may not be finished.")


@app.route('/level1',methods=['GET'])
def get_title1():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM one1 ORDER BY RAND() LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)

@app.route('/level2',methods=['GET'])
def get_title2():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM two2 LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)


@app.route('/level3',methods=['GET'])
def get_title3():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM three3 LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)

@app.route('/level4',methods=['GET'])
def get_title4():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM four4 LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)

@app.route('/level5',methods=['GET'])
def get_title5():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM five5 LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)

@app.route('/level6',methods=['GET'])
def get_title6():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM six6 LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)

@app.route('/level7',methods=['GET'])
def get_title7():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM seven7 LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)

@app.route('/level8',methods=['GET'])
def get_title8():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM  eight8 LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)

@app.route('/level9',methods=['GET'])
def get_title9():

        cursor = conn.cursor()
        # 执行 SQL 查询
        cursor.execute("SELECT title FROM nine9 LIMIT 1")

        # 获取查询结果
        results = cursor.fetchall()

        # 将结果转换为字典列表
        data = [{'title': row[0]} for row in results]

        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)