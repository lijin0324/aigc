from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    print('Received stop recording request')
    with open('stop.txt', 'r') as file:
        lines = file.readlines()

    # 对文件内容进行修改
    new_lines = [line.replace('0', '1') for line in lines]

    # 将修改后的内容写回文件
    with open('stop.txt', 'w') as file:
        file.writelines(new_lines)
    return jsonify({"message": "Recording stopped"})


if __name__ == '__main__':
    app.run(port=8000)

