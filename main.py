# unrestricted_api.py
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def run():
    long = request.args.get("lang")
    if not long:
        return "<h1>404 Not Found</h1> <br><h2>このサイトはpokemogukunnsのコマンドラインを再現するためのサイトです．<br>まだ完成はしておらず、コマンドは実行できません．</h2><h1>せめて完成を待ってください．</h1>", 200

    

@app.route("/run")
def run_command():
    cmd = request.args.get("cmd")
    if not cmd:
        return "Error: No command provided.", 400

    print(f"[実行] {cmd}")
    try:
        output = subprocess.getoutput(cmd)
        return f"<pre>{output}</pre>"
    except Exception as e:
        return f"<pre>実行エラー: {str(e)}</pre>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
