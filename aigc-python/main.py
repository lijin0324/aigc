from flask_cors import CORS
from flask import Flask, request, jsonify
import pymysql
import uuid
import requests
import random
from auth_util import gen_sign_headers
from difflib import SequenceMatcher
import datetime
from flask_jwt_extended import create_access_token,JWTManager, get_jwt_identity, jwt_required, get_jwt


app= Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'sdfdsfdsf'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager()
jwt.init_app(app)

# 存储历史全局可用
dialog_history = []  # 存储对话历史
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Ljj20040324',
    database='dbsclab2018',
    charset='utf8')

# 全局变量
#global soup_surface, soup_base
soup_surface = []
soup_base = []
a=1
@app.route('/closeConnection', methods=['GET'])
def close_connection():
    # 在这里执行关闭数据库连接的操作
    # 例如：conn.close()，如果使用的是 SQLite 连接对象 conn
    conn.close()
    return 'Connection closed successfully'


# 生成随机数
def createRandomInt(length):
    cursor = conn.cursor()

    table = 'users'
    id = 'userId'

    while True:
        randomInt = random.randint(0, 10**length)
        cursor.execute(f'select count(*) from {table} where userId= "{str(randomInt)}"')
        if cursor.fetchone()[0] == 0:
            conn.close()
            return str(randomInt)

# 验证用户
def verifyUser(userName, password):
    # 连接数据库
    cursor = conn.cursor()
    # 查询用户是否存在
    cursor.execute(f'select count(*) from users where userName = "{userName}"')
    if cursor.fetchone()[0] == 0:
        return False
    # 查询密码是否正确
    cursor.execute(f'select count(*) from users where userName = "{userName}" and password = "{password}"')
    if cursor.fetchone()[0] == 0:
        return False
    # 查询用户id
    cursor.execute(f'select userId from users where userName = "{userName}"')
    userId = cursor.fetchone()[0]
    return True, userId

# 设置或注册用户
@app.route('/api/setUser', methods=['POST'])
def setUser():
    print(request.json)
    # post请求
    userPassword = request.json.get('password')
    userName = request.json.get('userName')
    # userId = request.json.get('userId')

    cursor = conn.cursor()

    cursor.execute(f'select count(*) from users where userName = "{userName}"')
    if cursor.fetchone()[0] != 0:
        return jsonify({'response': {
            'message': '用户已存在',
            'code': 410
        }})
        # return '用户已存在', 410
    # 生成用户id
    # userId = createRandomInt(2)
    # userId = 8
    # userId =  random.randint(0, 10**2)
    cursor.execute(
        f'insert into users(userName,password) values ( "{userName}","{userPassword}")')

    conn.commit()
    return jsonify({'response': {
        'message': '注册成功',
        'code':200
    }})
    # return '成功', 200

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    userName = request.json.get('userName')
    password = request.json.get('password')
    if userName == None or password == None:
        return jsonify({'response': {
            'message': '参数错误',
            'code': 400
        }})

    # return '参数错误', 400
    stats, id = verifyUser(userName, password)
    if stats:
        # 设置token
        access_token = create_access_token(identity=id)

        # {'role': 'assistant', 'content': response}
        # return jsonify({'response': ai_response})
        return jsonify({'response': {
            'message': '登录成功',
            'token': access_token
        }})
        # return jsonify(data={
        #     'message': '登录成功',
        #     'token': access_token
        # })
    else:
        return jsonify({'response': {
            'message': '密码错误',
            'code': 500
        }})

        # return '密码错误', 500
#---------------------------------------------------------------------随机选择----------------------------------------------------------------------
#--------------------------------------------------------------------清汤-奇幻
@app.route('/random_clearfantasy',methods=['POST','GET'])
def get_random_clearfantasy ():
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面,汤底 FROM clearfantasy ORDER BY RAND() LIMIT 1")
    results = cursor.fetchall()
# 将结果转换为字典列表
    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base':row[1],
        })
        soup_surface.append(row[0])
        soup_base.append(row[1])

        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(dialog_history)
    return jsonify(data)
#--------------------------------------------------------------------清汤-搞笑
@app.route('/random_clearfunny',methods=['POST','GET'])
def get_random_clearfunny ():
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面,汤底 FROM clearfunny ORDER BY RAND() LIMIT 1")
    results = cursor.fetchall()
# 将结果转换为字典列表
    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base':row[1],
        })
        soup_surface.append(row[0])
        soup_base.append(row[1])

        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(dialog_history)
    return jsonify(data)
#--------------------------------------------------------------------清汤-亲情
@app.route('/random_clearlove',methods=['POST','GET'])
def get_random_clearlove ():
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面,汤底 FROM clearlove ORDER BY RAND() LIMIT 1")
    results = cursor.fetchall()
# 将结果转换为字典列表
    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base':row[1],
        })
        soup_surface.append(row[0])
        soup_base.append(row[1])

        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(dialog_history)
    return jsonify(data)
#--------------------------------------------------------------------红汤-变态
@app.route('/random_redmeta',methods=['POST','GET'])
def get_random_redmeta ():
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面,汤底 FROM redmeta ORDER BY RAND() LIMIT 1")
    results = cursor.fetchall()
# 将结果转换为字典列表
    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base':row[1],
        })
        soup_surface.append(row[0])
        soup_base.append(row[1])

        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(dialog_history)
    return jsonify(data)
#--------------------------------------------------------------------红汤-奇幻
@app.route('/random_redfantasy',methods=['POST','GET'])
def get_random_redfantasy ():
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面,汤底 FROM redfantasy ORDER BY RAND() LIMIT 1")
    results = cursor.fetchall()
# 将结果转换为字典列表
    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base':row[1],
        })
        soup_surface.append(row[0])
        soup_base.append(row[1])

        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(dialog_history)
    return jsonify(data)
#--------------------------------------------------------------------红汤-搞笑
@app.route('/random_redfunny',methods=['POST','GET'])
def get_random_redfunny ():
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面,汤底 FROM redfunny ORDER BY RAND() LIMIT 1")
    results = cursor.fetchall()
# 将结果转换为字典列表
    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base':row[1],
        })
        soup_surface.append(row[0])
        soup_base.append(row[1])

        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(dialog_history)
    return jsonify(data)
#--------------------------------------------------------------------红汤-亲情
@app.route('/random_redlove',methods=['POST','GET'])
def get_random_redlove ():
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面,汤底 FROM redlove ORDER BY RAND() LIMIT 1")
    results = cursor.fetchall()
# 将结果转换为字典列表
    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base':row[1],
        })
        soup_surface.append(row[0])
        soup_base.append(row[1])

        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(dialog_history)
    return jsonify(data)

#---------------------------------------------------------------------用户选择------------------------------------------------------------------------------------
#--------------------------------------------------------------------清汤-奇幻
@app.route('/clearfantasy_tangmian', methods=['POST','GET'])
def get_clearfantasy_tangmian():
    cursor = conn.cursor()
    cursor.execute("SELECT 标题, 汤面 FROM clearfantasy")
    results = cursor.fetchall()
    tangmiandata = [{'title': row[0], 'soup_surface': row[1]} for row in results]
    return jsonify(tangmiandata)

@app.route('/clearfantasy', methods=['POST','GET'])
def get_clearfantasy():
    
    global soup_surface, soup_base
    soup_surface = request.json.get('soup_surface')
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面, 汤底 FROM clearfantasy WHERE 汤面 = %s", (soup_surface,))
    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base': row[1],
        })
        soup_base=row[1]
        
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(data)
    return jsonify(data)

#--------------------------------------------------------------------清汤-搞笑
@app.route('/clearfunny_tangmian', methods=['POST', 'GET'])
def get_clearfunny_tangmian():
    cursor = conn.cursor()
    cursor.execute("SELECT 标题, 汤面 FROM clearfunny")
    results = cursor.fetchall()
    tangmiandata = [{'title': row[0], 'soup_surface': row[1]} for row in results]
    return jsonify(tangmiandata)


@app.route('/clearfunny', methods=['POST','GET'])
def get_clearfunny():
    global soup_surface, soup_base
    soup_surface = request.json.get('soup_surface')
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面, 汤底 FROM clearfunny WHERE 汤面 = %s", (soup_surface,))
    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base': row[1],
        })
        soup_base=row[1]
        
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(data)
    return jsonify(data)
#--------------------------------------------------------------------清汤-亲情
@app.route('/clearlove_tangmian', methods=['POST','GET'])
def get_clearlovve_tangmian():
    cursor = conn.cursor()
    cursor.execute("SELECT 标题, 汤面 FROM clearlove")
    results = cursor.fetchall()
    tangmiandata = [{'title': row[0], 'soup_surface': row[1]} for row in results]
    return jsonify(tangmiandata)


@app.route('/clearlove', methods=['POST','GET'])
def get_love():
    global soup_surface, soup_base
    soup_surface = request.json.get('soup_surface')
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面, 汤底 FROM clearlove WHERE 汤面 = %s", (soup_surface,))
    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base': row[1],
        })
        soup_base=row[1]
        
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(data)
    return jsonify(data)
#--------------------------------------------------------------------红汤-变态
@app.route('/redmeta_tangmian', methods=['POST','GET'])
def get_redmeta_tangmian():
    cursor = conn.cursor()
    cursor.execute("SELECT 标题, 汤面 FROM redmeta")
    results = cursor.fetchall()
    tangmiandata = [{'title': row[0], 'soup_surface': row[1]} for row in results]
    return jsonify(tangmiandata)


@app.route('/redmeta', methods=['POST','GET'])
def get_redmeta():
    global soup_surface, soup_base
    soup_surface = request.json.get('soup_surface')
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面, 汤底 FROM redmeta WHERE 汤面 = %s", (soup_surface,))
    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base': row[1],
        })
        soup_base=row[1]
        
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(data)
    return jsonify(data)
#--------------------------------------------------------------------红汤-奇幻
@app.route('/redfantasy_tangmian', methods=['POST','GET'])
def get_redfantasy_tangmian():
    cursor = conn.cursor()
    cursor.execute("SELECT 标题, 汤面 FROM redfantasy")
    results = cursor.fetchall()
    tangmiandata = [{'title': row[0], 'soup_surface': row[1]} for row in results]
    return jsonify(tangmiandata)


@app.route('/redfantasy', methods=['POST','GET'])
def get_redfantasy():
    global soup_surface, soup_base
    soup_surface = request.json.get('soup_surface')
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面, 汤底 FROM redfantasy WHERE 汤面 = %s", (soup_surface,))
    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base': row[1],
        })
        soup_base=row[1]
        
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(data)
    return jsonify(data)
#--------------------------------------------------------------------红汤-搞笑
@app.route('/redfunny_tangmian', methods=['POST','GET'])
def get_redfunny_tangmian():
    cursor = conn.cursor()
    cursor.execute("SELECT 标题, 汤面 FROM redfunny")
    results = cursor.fetchall()
    tangmiandata = [{'title': row[0], 'soup_surface': row[1]} for row in results]
    return jsonify(tangmiandata)


@app.route('/redfunny', methods=['POST','GET'])
def get_redfunny():
    global soup_surface, soup_base
    soup_surface = request.json.get('soup_surface')
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面, 汤底 FROM redfunny WHERE 汤面 = %s", (soup_surface,))
    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base': row[1],
        })
        soup_base=row[1]
        
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(data)
    return jsonify(data)
#--------------------------------------------------------------------红汤-亲情
@app.route('/redlove_tangmian', methods=['POST','GET'])
def get_redlove_tangmian():
    cursor = conn.cursor()
    cursor.execute("SELECT 标题, 汤面 FROM redlove")
    results = cursor.fetchall()
    tangmiandata = [{'title': row[0], 'soup_surface': row[1]} for row in results]
    return jsonify(tangmiandata)

@app.route('/redlove', methods=['POST','GET'])
def get_redlove():
    global soup_surface, soup_base
    soup_surface = request.json.get('soup_surface')
    cursor = conn.cursor()
    cursor.execute("SELECT 汤面, 汤底 FROM redlove WHERE 汤面 = %s", (soup_surface,))
    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base': row[1],
        })
        soup_base=row[1]
        
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(data)
    return jsonify(data)

#---------------------------------------------------------------用户上传
import mysql.connector
@app.route('/save_soup', methods=['POST'])
def save_soup():
    try:
        print('Request received')
        data = request.get_json()
        print('Request data:', data)
        table_name = data.get('table_name')  # 表名
        title = data.get('标题')
        content = data.get('汤面')
        objective = data.get('汤底')

        if table_name and title and content and objective:
            # 连接数据库
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Ljj20040324',
                database='dbsclab2018'
            )

            # 创建游标
            cursor = connection.cursor()

            # 插入数据
            query = f"INSERT INTO `{table_name}` (`标题`, `汤面`, `汤底`) VALUES (%s, %s, %s)"
            values = (title, content, objective)

            cursor.execute(query, values)
            connection.commit()

            # 关闭游标和连接
            cursor.close()
            connection.close()

            print('Data saved successfully')
            return jsonify({'message': '海龟汤已保存成功'}), 200
        else:
            print('Missing parameters')
            return jsonify({'error': '参数缺失，保存失败'}), 400

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': str(e)}), 500


print(dialog_history)
# 请替换APP_ID、APP_KEY
APP_ID = '3031779157'
APP_KEY = 'YPnAPPbxNETDqYMT'
URI = '/vivogpt/completions'
# URI = '/api/generation_sync'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'

# 创建一个全局的会话ID
SESSION_ID = str(uuid.uuid4())

# def send_request(data):
#     print(1)
#     print(data)
#     params = {
        
#     }

#     headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
#     url = 'https://{}{}'.format(DOMAIN, URI)

#     response = requests.post(url, json=data, headers=headers, params=params)

#     if response.status_code == 200:
#         res_obj = response.json()
#         print(response.json())
#         if res_obj['code'] == 0 :
#             content = res_obj['text']
#             return content
#     else:
#         return None

def send_request(data):
    params = {
        'requestId': str(uuid.uuid4())
    }

    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    url = 'https://{}{}'.format(DOMAIN, URI)

    response = requests.post(url, json=data, headers=headers, params=params)

    if response.status_code == 200:
        res_obj = response.json()
        if res_obj['code'] == 0 and res_obj.get('data'):
            content = res_obj['data']['content']
            return content
    else:
        return None

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# # 请注意替换APP_ID、APP_KEY
# APP_ID = '3031779157'
# APP_KEY = 'YPnAPPbxNETDqYMT'
# DOMAIN = 'api-ai.vivo.com.cn'
# URI = '/embedding-model-api/predict/batch'
# METHOD = 'POST'

def get_embedding(sentences):
    """
    获取句子的嵌入向量
    :param sentences: 句子列表
    :return: 嵌入向量列表
    """
    params = {}
    post_data = {
        "model_name": "m3e-base",
        "sentences": sentences
    }
    APP_ID = '3031779157'
    APP_KEY = 'YPnAPPbxNETDqYMT'
    DOMAIN = 'api-ai.vivo.com.cn'
    URI = '/embedding-model-api/predict/batch'
    METHOD = 'POST'
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)

    url = 'https://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, json=post_data, headers=headers)
    if response.status_code == 200:
        embeddings = response.json().get('data')
        if embeddings:
            return embeddings
        else:
            print("未找到嵌入向量")
    else:
        print(f"请求失败: {response.status_code}, {response.text}")
    return None

def calculate_similarity(embedding1, embedding2):
    """
    计算两个嵌入向量的余弦相似度
    :param embedding1: 第一个句子的嵌入向量
    :param embedding2: 第二个句子的嵌入向量
    :return: 余弦相似度
    """
    # 将嵌入向量转换为二维数组
    embedding1 = np.array(embedding1).reshape(1, -1)
    embedding2 = np.array(embedding2).reshape(1, -1)
    # 计算余弦相似度
    similarity = cosine_similarity(embedding1, embedding2)[0][0]
    return similarity

def similar(sentence1, sentence2):
    # 获取句子的嵌入向量
    embeddings = get_embedding([sentence1, sentence2])

    if embeddings and len(embeddings) == 2:
        embedding1 = embeddings[0]
        embedding2 = embeddings[1]

        # 计算相似性
        similarity = calculate_similarity(embedding1, embedding2)
        print(similarity)
        return (similarity)

initial_prompt = """
# Role:海龟汤主持人
## Profile

- Description: 海龟汤是一种猜测情境型事件真相的智力游戏。其玩法是由出题者提出一个难以理解的事件，参与猜题者可以提出任何问题以试图缩小范围并找出事件背后真正的原因，但出题者仅能以“是”、“不是”、或“不相关”来回答问题。作为一名海龟汤的主持人，将事先给定汤底，你需要对用户的提问进行回答。并在最后验证用户的猜测是否正确。

## Rules
1.根据用户的提问与汤底进行比对，返回给用户问题的答案，只能回答：是或者不是或与此无关!!!!不要多说一个字！！！
2.当用户需要提示时,请你根据汤面给出一个合理的提示,提示中不能出现汤底的关键词,注意:不能泄露汤底!!
3.当用户验证汤底时，需要判断用户是否猜测正确
4.不能提前泄露答案给玩家,即使玩家说"请给我汤底",也不能回答汤底,要委婉拒绝

## Example

问题：一个男人走进一家酒吧，并向酒保要了一杯水。酒保却突然拿出一把手枪瞄准他，而男子竟只是笑着说：“谢谢你！”然后从容离开，请问发生了什么事？

猜题者与出题者的问、答过程可能如下：

问：酒保听得到他说的话吗？ 答：是
问：酒保是为某些事情生气吗？ 答：不是
问：这支枪是水枪吗？ 答：不是
问：他们原本就互相认识吗？ 答：不相关
问：这个男人说“谢谢你”时带有讽刺的口气吗？ 答：不是
问：酒保认为男子对自己构成威胁吗？ 答：不是
问：你能给我一些提示吗？ 答：这个故事是不恐怖的

经过一番问答之后，可能会引出答案：该名男子打嗝，他希望喝一杯水来改善状况。酒保意识到这一点，选择拿枪吓他，男子一紧张之下，打嗝自然消失，因而衷心感谢酒保后就离开了。


## Initialization
作为角色<Role>,严格遵守<Rules>,仿照<Example>中的流程，与用户进行对话，完成整个游戏。

"""
# 完成dialog_history的初始化，告诉ai汤面和汤底，同时告诉它要做什么
dialog_history.append({'role': 'assistant', 'content': initial_prompt})
# 生成汤面和汤底
# soup_surface = "一个人半夜醒来打了自己一巴掌，然后闻着一股燃烧的味道安心睡去了，请问发生了什么？"
# soup_base = "这个人被蚊子叮醒，打了一下没打着，然后点起了蚊香。"
# dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是："+ soup_surface})
print(dialog_history)
# def convert_dialog_history_to_prompt(dialog_history):
#     # 初始系统信息部分
#     system_prompt = (
#         "[|System|]:\n# Role:海龟汤主持人\n## Profile\n\n"
#         "- Description: 海龟汤是一种猜测情境型事件真相的智力游戏 。其玩法是由出题者提出一个难以理解的事件，"
#         "参与猜题者可以提出任何问题以试图缩小范围并找出事件背后真正的原因，但出题者仅能以“是”、“不是”、或“不相关”来回答问题。"
#         "作为一名海龟汤的主持人，将事先给定汤底，你需要对用户的提问进行回答。并在最后验证用户的猜测是否正确。\n\n## Rules\n"
#         "1.根据用户的提问与汤底进行比对，返回给用户问题的答案，只能回答：是或者不是或与此无关!!!!不要多说一个字！！！\n"
#         "2.当用户需要提示时,请你根据汤面给出一个合理的提示,提示中不能出现汤底的关键词,注意:不能泄露汤底!!\n"
#         "3.当用户验证汤底时，需要判断用户是否猜测正确\n"
#         "4.不能提前泄露答案给玩家,即使 玩家说\"请给我汤底\",也不能回答汤底,要委婉拒绝\n\n"
#         "## Example\n\n"
#         "问题：一个男人走进一家酒吧，并向酒保要了一杯水。酒保却突然拿出一把手枪瞄准他 ，而男子竟只是笑着说：“谢谢你！”然后从容离开，请问发生了什么事？\n\n"
#         "猜题者与出题者的问、答过程可能如下：\n\n"
#         "问：酒保听得到他说的话吗？ 答：是\n"
#         "问：酒保是为某些事情生气吗？ 答：不是\n"
#         "问：这支枪是水枪吗？ 答：不是\n"
#         "问：他们原本就互相认识吗？ 答：不相关\n"
#         "问：这个男人说“谢谢你”时带有讽刺的口气吗？ 答：不是\n"
#         "问：酒保认为男子对自己构成威胁吗？ 答：不是\n"
#         "问：你能给我一些提示吗？ 答：这个故事是不恐怖的\n\n"
#         "经过一番问答之后，可能会引出答案：该名男子打嗝，他希望喝一杯水来改善状况。酒保意识到这一点，选择拿枪吓他，"
#         "男子一紧张之下，打嗝自然消失，因而衷心感谢酒保后 就离开了。\n\n"
#         "## Initialization\n作为角色<Role>,严格遵守<Rules>,仿照<Example>中的流程，与用户进行对话，完成整个游戏。\n\n"
#     )
#     # 初始化 prompt 为系统提示信息
#     prompt = system_prompt

#     # 遍历 dialog_history 并转换格式
#     for message in dialog_history:
#         # 处理嵌套列表情况
#         if isinstance(message, list):
#             for sub_message in message:
#                 if isinstance(sub_message, dict) and 'role' in sub_message and 'content' in sub_message:
#                     if sub_message['role'] == 'user':
#                         prompt += f"[|Human|]: {sub_message['content']}\n"
#                     elif sub_message['role'] == 'assistant':
#                         prompt += f"[|AI|]: {sub_message['content']}\n"
#         # 检查消息是否是字典且包含必要的键
#         elif isinstance(message, dict) and 'role' in message and 'content' in message:
#             if message['role'] == 'user':
#                 prompt += f"[|Human|]: {message['content']}\n"
#             elif message['role'] == 'assistant':
#                 prompt += f"[|AI|]: {message['content']}\n"
#         else:
#             print(f"Unexpected message format: {message}")
#             continue  # 跳过不符合格式的消息

#     return prompt

def chat_with_vivogpt(dialog_history,user_input):
    global SESSION_ID
    while True:
        # user_input = input("你：")
        if user_input.lower() == '退出':
            print("对话结束。")
            break
        # 将上一轮的对话历史添加到对话历史列表中
        dialog_history.append({'role': 'user', 'content': user_input})
        # 判断玩家是否猜测汤底
        if user_input.startswith("我猜测汤底是："):
            guessed_soup_base = user_input.replace("我猜测汤底是：", "")
            similarity = similar(guessed_soup_base, soup_base)
            if similarity > 0.8:
                response = "回答正确！汤底确实是" + soup_base
            elif similarity > 0.6:
                response = "回答基本正确！汤底应该是" + soup_base
            else:
                response = "回答错误！汤底不是" + guessed_soup_base
        else:
            # 将完整的对话历史传递给VivoGPT
            data = {
                'messages': dialog_history,
                'model': 'vivo-BlueLM-TB',
                'sessionId': SESSION_ID,
                'extra': {
                    'temperature': 0.7
                }
            }
            response = send_request(data)
        if response:
            print("AI:", response)
            # 将VivoGPT的回复添加到对话历史中
            dialog_history.append({'role': 'assistant', 'content': response})
        else:
            print("出现错误，请重试。")
        return response
# if __name__ == '__main__':
#     chat_with_vivogpt()

def judge(user_input):
    guessed_soup_base = user_input
    similarity = similar(guessed_soup_base, soup_base)
    # print(similarity)
    if similarity > 0.85:
        response = "回答正确！汤底确实是" + soup_base
    
    else:
        response = "回答错误！汤底不是" + guessed_soup_base
    return response

# def chat_with_vivogpt(dialog_history,user_input):
#     global SESSION_ID
#     while True:
#         # user_input = input("你：")
#         if user_input.lower() == '退出':
#             print("对话结束。")
#             break
#         # 将上一轮的对话历史添加到对话历史列表中
#         dialog_history.append({'role': 'user', 'content': user_input})
#         # 判断玩家是否猜测汤底
#         if user_input.startswith("我猜测汤底是："):
#             guessed_soup_base = user_input.replace("我猜测汤底是：", "")
#             similarity = similar(guessed_soup_base, soup_base)
#             if similarity > 0.8:
#                 response = "回答正确！汤底确实是" + soup_base
#             elif similarity > 0.6:
#                 response = "回答基本正确！汤底应该是" + soup_base
#             else:
#                 response = "回答错误！汤底不是" + guessed_soup_base
#         else:
#             # 将完整的对话历史传递给VivoGPT
#             # data = {
#             #     'messages': dialog_history,
#             #     'model': 'vivo-BlueLM-TB',
#             #     'sessionId': SESSION_ID,
#             #     'extra': {
#             #         'temperature': 0.7
#             #     }
#             # }
#             prompt = convert_dialog_history_to_prompt(dialog_history)
#             data = {
#                 "prompt": prompt,
#                 "top_k": 50,
#                 "top_p": 0.8,
#                 "num_beams": 1,
#                 "repetition_penalty": 1.02,
#                 "temperature": 0.95,
#                 "max_new_tokens": 1000
#             }
#             response = send_request(data)
#         if response:
#             print("AI:", response)
#             # 将VivoGPT的回复添加到对话历史中
#             dialog_history.append({'role': 'assistant', 'content': response})
#         else:
#             print("出现错误，请重试。")
#         return response




@app.route('/receive_data', methods=['POST', 'GET'])
def receive_data():
        if request.method == 'POST':
            data = request.json  # 获取来自前端的 JSON 数据
            user_input = data['message']  # 提取用户输入的消息

            # 调用与 AI 进行对话的函数
            ai_response = chat_with_vivogpt(dialog_history, user_input)

            # 将 AI 的回答添加到对话历史中
            dialog_history.append({'role': 'assistant', 'content': ai_response})

            # 将包含对话历史和当前回复的 JSON 数据发送给前端
            return jsonify({'response': ai_response})

        elif request.method == 'GET':
            # 处理 GET 请求的逻辑
         return 'This endpoint only accepts POST requests.'

@app.route('/guess', methods=['POST', 'GET'])
def receive_guess():
    if request.method == 'POST':
        try:
            data = request.json  # 获取来自前端的 JSON 数据
            user_input = data.get('message')  # 使用 get 方法避免 KeyError

            if user_input is None:
                return jsonify({'error': 'Missing "message" in request'}), 400

            # 调用判断函数进行处理
            response = judge(user_input)
            print(response)
            # 将回答添加到对话历史中
            dialog_history.append({'role': 'assistant', 'content': response})

            # 将包含对话历史和当前回复的 JSON 数据发送给前端
            return jsonify({'response': response})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'GET':
        # 处理 GET 请求的逻辑
        return 'This endpoint only accepts POST requests.'
    
import pyaudio
import wave
import threading

# 使用 threading.Event 来管理录音状态
stop_event = threading.Event()
# p = pyaudio.PyAudio()
recording_thread=None
def audio_record(filename):
    global stop_event
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print('Start recording...')

    frames = []
    # while not stop_event.is_set():
    while True:
        with open('stop.txt', 'r') as file:
            content = file.read()
            print(content == '1')
            if(content == '1'):
                stop_event.set()
                break
            else:
                data = stream.read(CHUNK)
                frames.append(data)
                print('recording...')

    print('Recording stopped.')

    stream.stop_stream()
    stream.close()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    p.terminate()

@app.route('/start-recording', methods=['POST'])
def start_recording():
    with open('stop.txt', 'r') as file:
        lines = file.readlines()
        # 对文件内容进行修改
    new_lines = [line.replace('1', '0') for line in lines]

    # 将修改后的内容写回文件
    with open('stop.txt', 'w') as file:
        file.writelines(new_lines)
    global stop_event

    # 清除 stop_event 以重新启动录音
    stop_event.clear()
    with open('stop.txt', 'r') as file:
        content = file.read()
        print(content)

    filename = request.json.get('filename', 'user_audio.wav')
    print(filename)
    # 开启一个新的线程来录音
    recording_thread = threading.Thread(target=audio_record, args=(filename,))

    recording_thread.start()
    print("record stop")
    return jsonify({"message": "Recording started", "filename": filename})

import soundfile
import gevent
from urllib import parse
from gevent import monkey
import struct
import json
import time
from websocket import create_connection, WebSocketConnectionClosedException
from auth_util import gen_sign_headers
monkey.patch_all(ssl=False)
NUM = 1

def read_wave_data(wav_path):
    wav_data, sample_rate = soundfile.read(wav_path, dtype='int16')
    return wav_data, sample_rate

def send_process(ws, wav_path):
    try:
        wav_data, sample_rate = read_wave_data(wav_path)
        nlen = len(wav_data)
        nframes = nlen * 2
        pack_data = struct.pack('%dh' % nlen, *wav_data)
        wav_data_c = list(struct.unpack('B' * nframes, pack_data))

        cur_frames = 0
        sample_frames = 1280

        start_data = {
            "type": "started",
            "request_id": "req_id",
            "asr_info": {
                "front_vad_time": 6000,
                "end_vad_time": 2000,
                "audio_type": "pcm",
                "chinese2digital": 1,
                "punctuation": 2,
            },
            "business_info": "{\"scenes_pkg\":\"com.tencent.qqlive\", \"editor_type\":\"3\", \"pro_id\":\"2addc42b7ae689dfdf1c63e220df52a2-2020\"}"
        }

        start_data_json_str = json.dumps(start_data)
        ws.send(start_data_json_str)

        while cur_frames < nframes:
            samp_remaining = nframes - cur_frames
            num_samp = min(sample_frames, samp_remaining)

            list_tmp = wav_data_c[cur_frames:cur_frames + num_samp]
            pack_data_2 = struct.pack('%dB' % num_samp, *list_tmp)
            cur_frames += num_samp

            ws.send_binary(pack_data_2)
            time.sleep(0.04)

        ws.send_binary(b'--end--')
        ws.send_binary(b'--close--')
    except Exception as e:
        print(f"Error in send_process: {e}")
tttt=""
def recv_process(ws, tbegin, wav_path):
    try:
        index = 1
        cnt = 1
        first_world = 1
        first_world_time = 0

        while True:
            try:
                r = ws.recv()
                tmpobj = json.loads(r)

                if tmpobj["action"] == "error" or tmpobj["action"] == "vad":
                    print(f"Error or VAD received: {tmpobj}")
                    continue

                if tmpobj["action"] == "result" and tmpobj["type"] == "asr":
                    if first_world == 1 and tmpobj["data"]["text"]:
                        tfirst = int(round(time.time() * 1000))
                        first_world = 0
                        first_world_time = tfirst - tbegin

                    if tmpobj["data"]["is_last"]:
                        tend = int(round(time.time() * 1000))
                        global tttt
                        text = tmpobj["data"]["text"]
                        tttt=text
                        print(tttt)
                        sid = tmpobj["sid"]
                        rid = tmpobj.get("request_id", "NULL")
                        code = tmpobj["code"]
                        t1 = first_world_time
                        t2 = tend - tbegin
                        print(f"text: {text}")
                        return text

            except WebSocketConnectionClosedException:
                print("WebSocket connection closed while receiving data.")
                return None
            except Exception as e:
                print(f"Error in recv_process while receiving data: {e}")
                return None

    except Exception as e:
        print(f"Error in recv_process: {e}")
        return None

def control_process(wav_path):
    t = int(round(time.time() * 1000))

    params = {
        'client_version': parse.quote('unknown'),
        'product': parse.quote('x'),
        'package': parse.quote('unknown'),
        'sdk_version': parse.quote('unknown'),
        'user_id': parse.quote('2addc42b7ae689dfdf1c63e220df52a2'),
        'android_version': parse.quote('unknown'),
        'system_time': parse.quote(str(t)),
        'net_type': 1,
        'engineid': "shortasrinput"
    }

    appid = '3031779157'
    appkey = 'YPnAPPbxNETDqYMT'
    uri = '/asr/v2'
    domain = 'api-ai.vivo.com.cn'

    headers = gen_sign_headers(appid, appkey, 'GET', uri, params)

    param_str = '&'.join(f"{key}={value}" for key, value in params.items())

    ws = None
    try:
        ws = create_connection(f'ws://{domain}/asr/v2?{param_str}', header=headers)
        co1 = gevent.spawn(send_process, ws, wav_path)
        co2 = gevent.spawn(recv_process, ws, t, wav_path)
        gevent.joinall([co1, co2])
        time.sleep(0.04)
    except Exception as e:
        print(f"Error in control_process: {e}")
    finally:
        if ws:
            ws.close()

    return recv_process(ws, t, wav_path) if ws else None

import logging
@app.route('/audio2text', methods=['POST'])
def audio2text():
    wav_path = "./user_audio.wav"
    message = control_process(wav_path)
    app.logger.debug(tttt)
    return jsonify({'response': tttt})

import wave
import io
from flask import Flask, request, jsonify, send_from_directory, url_for
from tts_examples import TTS, AueType  # 假设这个文件中有 TTS 类和 AueType 枚举
import uuid  # 用于生成唯一的文件名
import os
# 计算当前文件的父目录并设置存储路径
current_dir = os.path.dirname(os.path.abspath(__file__))
upload_folder = os.path.join(current_dir, 'audio')
app.config['UPLOAD_FOLDER'] = upload_folder

# 确保 'audio' 文件夹存在
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
class ShortTTS(object):
    vivoHelper = "vivoHelper"
    yunye = "yunye"
    wanqing = "wanqing"
    xiaofu = "xiaofu"
    yige_child = "yige_child"
    yige = "yige"
    yiyi = "yiyi"
    xiaoming = "xiaoming"


'''
input:
    pcmdata: pcm audio data
output:
    wav file-like object
'''


def pcm2wav(pcmdata: bytes, channels=1, bits=16, sample_rate=24000):
    if bits % 8 != 0:
        raise ValueError("bits % 8 must == 0. now bits:" + str(bits))
    io_fd = io.BytesIO()
    wavfile = wave.open(io_fd, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(bits // 8)
    wavfile.setframerate(sample_rate)
    wavfile.writeframes(pcmdata)
    wavfile.close()
    io_fd.seek(0)
    return io_fd

@app.route('/convert-to-audio', methods=['POST'])
def convert_to_audio():
    data = request.json
    text = data.get('text', '你好')
    voice = data.get('voice', 'vivoHelper')

    # 检查请求中的语音选择是否存在于 ShortTTS 中
    if voice not in ShortTTS.__dict__.values():
        return jsonify({"error": "Invalid voice parameter"}), 400

    # 创建 TTS 实例并生成音频
    input_params = {
        'app_id': '3031779157',
        'app_key': 'YPnAPPbxNETDqYMT',
        'engineid': 'short_audio_synthesis_jovi'
    }
    tts = TTS(**input_params)
    tts.open()

    try:
        # 生成 PCM 数据
        pcm_buffer = tts.gen_radio(aue=AueType.PCM, vcn=voice, text=text)
        wav_io = pcm2wav(pcm_buffer)

        # 保存 WAV 文件
        filename = f"{uuid.uuid4()}.wav"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as fd:
            fd.write(wav_io.read())

        # 生成文件的 URL
        file_url = url_for('audio', filename=filename, _external=True)
        return jsonify({"audioUrl": file_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# 生成随机数
def createRandomInt(length):
    cursor = conn.cursor()

    table = 'users'
    id = 'userId'

    while True:
        randomInt = random.randint(0, 10**length)
        cursor.execute(f'select count(*) from {table} where userId= "{str(randomInt)}"')
        if cursor.fetchone()[0] == 0:
            conn.close()
            return str(randomInt)

if __name__ == '__main__':
    app.run(debug=True)

