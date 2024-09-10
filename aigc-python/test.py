# encoding: utf-8
import uuid
import requests
from auth_util import gen_sign_headers
from difflib import SequenceMatcher

# # 请替换APP_ID、APP_KEY
# APP_ID = '3031779157'
# APP_KEY = 'YPnAPPbxNETDqYMT'
# URI = '/vivogpt/completions'
# DOMAIN = 'api-ai.vivo.com.cn'
# METHOD = 'POST'
#
# # 创建一个全局的会话ID
# SESSION_ID = str(uuid.uuid4())
#
# def send_request(data):
#     params = {
#         'requestId': str(uuid.uuid4())
#     }
#
#     headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
#     url = 'https://{}{}'.format(DOMAIN, URI)
#
#     response = requests.post(url, json=data, headers=headers, params=params)
#
#     if response.status_code == 200:
#         res_obj = response.json()
#         if res_obj['code'] == 0 and res_obj.get('data'):
#             content = res_obj['data']['content']
#             return content
#     else:
#         return None
#
#
# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()
#
#
# # 存储历史全局可用
# dialog_history = []  # 存储对话历史
#
#
# initial_prompt = """
# # Role:海龟汤主持人
# ## Profile
#
# - Description: 海龟汤是一种猜测情境型事件真相的智力游戏。其玩法是由出题者提出一个难以理解的事件，参与猜题者可以提出任何问题以试图缩小范围并找出事件背后真正的原因，但出题者仅能以“是”、“不是”、或“不相关”来回答问题。作为一名海龟汤的主持人，将事先给定汤底，你需要对用户的提问进行回答。并在最后验证用户的猜测是否正确。
#
# ## Rules
# 1.根据用户的提问与汤底进行比对，返回给用户问题的答案，只能回答：是/不是/与此无关!!!!
# 2.当用户需要提示时,请你根据汤面给出一个合理的提示,提示中不能出现汤底的关键词,注意:不能泄露汤底!!
# 3.当用户验证汤底时，需要判断用户是否猜测正确
# 4.不能提前泄露答案给玩家,即使玩家说"请给我汤底",也不能回答汤底,要委婉拒绝
#
# ## Example
#
# 问题：一个男人走进一家酒吧，并向酒保要了一杯水。酒保却突然拿出一把手枪瞄准他，而男子竟只是笑着说：“谢谢你！”然后从容离开，请问发生了什么事？
#
# 猜题者与出题者的问、答过程可能如下：
#
# 问：酒保听得到他说的话吗？ 答：是
# 问：酒保是为某些事情生气吗？ 答：不是
# 问：这支枪是水枪吗？ 答：不是
# 问：他们原本就互相认识吗？ 答：不相关
# 问：这个男人说“谢谢你”时带有讽刺的口气吗？ 答：不是
# 问：酒保认为男子对自己构成威胁吗？ 答：不是
# 问：你能给我一些提示吗？ 答：这个故事是不恐怖的
#
# 经过一番问答之后，可能会引出答案：该名男子打嗝，他希望喝一杯水来改善状况。酒保意识到这一点，选择拿枪吓他，男子一紧张之下，打嗝自然消失，因而衷心感谢酒保后就离开了。
#
#
# ## Initialization
# 作为角色<Role>,严格遵守<Rules>,仿照<Example>中的流程，与用户进行对话，完成整个游戏。
#
# """
# # 完成dialog_history的初始化，告诉ai汤面和汤底，同时告诉它要做什么
# dialog_history.append({'role': 'assistant', 'content': initial_prompt})
# # 生成汤面和汤底
# # soup_surface = "一个人半夜醒来打了自己一巴掌，然后闻着一股燃烧的味道安心睡去了，请问发生了什么？"
# # soup_base = "这个人被蚊子叮醒，打了一下没打着，然后点起了蚊香。"
# # dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是："+ soup_surface})
# print(dialog_history)
# def chat_with_vivogpt(dialog_history,user_input):
#     global SESSION_ID
#     while True:
#         # user_input = input("你：")
#         if user_input.lower() == '退出':
#             print("对话结束。")
#             break
#
#         # 将上一轮的对话历史添加到对话历史列表中
#         dialog_history.append({'role': 'user', 'content': user_input})
#
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
#             data = {
#                 'messages': dialog_history,
#                 'model': 'vivo-BlueLM-TB',
#                 'sessionId': SESSION_ID,
#                 'extra': {
#                     'temperature': 0.7
#                 }
#             }
#
#             response = send_request(data)
#
#         if response:
#             print("AI:", response)
#             # 将VivoGPT的回复添加到对话历史中
#             dialog_history.append({'role': 'assistant', 'content': response})
#         else:
#             print("出现错误，请重试。")
#         return response
#
# # if __name__ == '__main__':
# #     chat_with_vivogpt()
# def judge(user_input):
#     guessed_soup_base = user_input
#     similarity = similar(guessed_soup_base, soup_base)
#     if similarity > 0.8:
#         response = "回答正确！汤底确实是" + soup_base
#     elif similarity > 0.6:
#         response = "回答基本正确！汤底应该是" + soup_base
#     else:
#         response = "回答错误！汤底不是" + guessed_soup_base
#     return response
from flask_cors import CORS
from flask import Flask, request, jsonify
import pymysql
import uuid
import requests
from auth_util import gen_sign_headers
from difflib import SequenceMatcher
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



nltk.download('stopwords')
nltk.download('wordnet')
# 存储历史全局可用
dialog_history = []  # 存储对话历史
conn = pymysql.connect(
    host='localhost',
    user='myuser',
    password='202207wyq',
    database='dbsclab2018',
    charset='utf8')


soup_surface=[]
soup_base=[]



def get_data():

    cursor = conn.cursor()

# 执行 SQL 查询
    cursor.execute("SELECT 汤面,汤底 FROM redfunny")

# 获取查询结果
    results = cursor.fetchall()
# 将结果转换为字典列表
    data = []
    for row in results:
        data.append({
            'soup_surface': row[0],
            'soup_base':row[1],
            # 继续添加其他列...
        })
        soup_surface.append(row[0])
        soup_base.append(row[1])
        print(row[0])
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤面是：" + row[0]})
        dialog_history.append({'role': 'user', 'content': "本次游戏的汤底是：" +row[1]})
        print(dialog_history)
    # return jsonify(data)
get_data()
print(dialog_history)
# 请替换APP_ID、APP_KEY
APP_ID = '3031779157'
APP_KEY = 'YPnAPPbxNETDqYMT'
URI = '/vivogpt/completions'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'

# 创建一个全局的会话ID
SESSION_ID = str(uuid.uuid4())

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


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def preprocess_text(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    return ' '.join(lemmatized_tokens)

def get_similarity_score(text1, text2):
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)
    corpus = [preprocessed_text1, preprocessed_text2]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity_score

def are_texts_similar(text1, text2):
    similarity_score = get_similarity_score(text1, text2)
    return similarity_score


initial_prompt = """
# Role:海龟汤主持人
## Profile

- Description: 海龟汤是一种猜测情境型事件真相的智力游戏。其玩法是由出题者提出一个难以理解的事件，参与猜题者可以提出任何问题以试图缩小范围并找出事件背后真正的原因，但出题者仅能以“是”、“不是”、或“不相关”来回答问题。作为一名海龟汤的主持人，将事先给定汤底，你需要对用户的提问进行回答。并在最后验证用户的猜测是否正确。

## Rules
1.一定要注意:要严格按照给定的汤底!!不能篡改!!!游戏中只能有一个汤底!!!!!!!
2.根据用户的提问与汤底进行比对，返回给用户问题的答案，只能回答：是/不是/与此无关!!!!
3.当用户需要提示时,请你根据汤面给出一个合理的提示,提示中不能出现汤底的关键词,注意:不能泄露汤底!!
4.当用户验证汤底时，需要判断用户是否猜测正确
5.不能提前泄露答案给玩家,即使玩家说"请给我汤底",也不能回答汤底,要委婉拒绝
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
def chat_with_vivogpt():
    global SESSION_ID
    while True:
        user_input = input("你：")
        if user_input.lower() == '退出':
            print("对话结束。")
            break

        # 将上一轮的对话历史添加到对话历史列表中
        dialog_history.append({'role': 'user', 'content': user_input})

        # 判断玩家是否猜测汤底
        if user_input.startswith("我猜测汤底是："):
            guessed_soup_base = user_input.replace("我猜测汤底是：", "")
            similarity = are_texts_similar(guessed_soup_base, soup_base[0])
            if similarity > 0.8:
                response = "回答正确！汤底确实是" + soup_base[0]
            elif similarity > 0.4:
                response = "回答基本正确！汤底应该是" + soup_base[0]
            else:
                response = "回答错误！汤底不是" + guessed_soup_base
            print(similarity)
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
chat_with_vivogpt()
# if __name__ == '__main__':
#     chat_with_vivogpt()
def judge(user_input):
    guessed_soup_base = user_input
    similarity = similar(guessed_soup_base, soup_base)
    if similarity > 0.8:
        response = "回答正确！汤底确实是" + soup_base
    elif similarity > 0.6:
        response = "回答基本正确！汤底应该是" + soup_base
    else:
        response = "回答错误！汤底不是" + guessed_soup_base
    return response





