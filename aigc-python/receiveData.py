# from flask import Flask, request, jsonify
# from test import chat_with_vivogpt,dialog_history,judge
# app = Flask(__name__)

# @app.route('/receive_data', methods=['POST','GET'])
#
# def receive_data():
#     if request.method == 'POST':
#         data = request.json  # 获取来自前端的 JSON 数据
#         user_input = data['message']  # 提取用户输入的消息
#
#         # 调用与 AI 进行对话的函数
#         ai_response = chat_with_vivogpt(dialog_history,user_input)
#
#         # 将 AI 的回答添加到对话历史中
#         dialog_history.append({'role': 'assistant', 'content': ai_response})
#
#         # 将包含对话历史和当前回复的 JSON 数据发送给前端
#         return jsonify({'response': ai_response})
#
#     elif request.method == 'GET':
#         # 处理 GET 请求的逻辑
#         return 'This endpoint only accepts POST requests.'
#
# @app.route('/guess', methods=['POST','GET'])
# def receive_guess():
#     if request.method == 'POST':
#         data = request.json  # 获取来自前端的 JSON 数据
#         user_input = data['message']  # 提取用户输入的消息
#
#         # 调用判断函数进行处理
#         response = judge(user_input)
#
#         # 将回答添加到对话历史中
#         dialog_history.append({'role': 'assistant', 'content': response})
#
#         # 将包含对话历史和当前回复的 JSON 数据发送给前端
#         return jsonify({'response': response})
#
#     elif request.method == 'GET':
#         # 处理 GET 请求的逻辑
#         return 'This endpoint only accepts POST requests.'

# if __name__ == '__main__':
#     app.run(debug=True)