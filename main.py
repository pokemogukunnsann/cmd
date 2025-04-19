from flask import Flask, request, send_from_directory
import subprocess
import os

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
GITHUB_USERNAME = "pokemogukunnsann"
GITHUB_TOKEN = "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"
REPO_URL = "https://github.com/pokemogukunnsann/cmdsennyoufile.git"
REPO_DIR = "/tmp/cmdrepo"

@app.route("/push", methods=["POST"])
def push_file():
    filename = request.args.get("filename", "test.txt")
    content = request.data.decode("utf-8")

    # 認証用 .netrc ファイルを生成
    netrc_path = os.path.expanduser("~/.netrc")
    with open(netrc_path, "w") as f:
        f.write(f"machine github.com\nlogin {GITHUB_USERNAME}\npassword {GITHUB_TOKEN}\n")
    os.chmod(netrc_path, 0o600)

    # Git clone
    if os.path.exists(REPO_DIR):
        subprocess.run(["rm", "-rf", REPO_DIR])
    subprocess.run(["git", "clone", REPO_URL, REPO_DIR])

    # ファイル保存
    file_path = os.path.join(REPO_DIR, "file", filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Git commit & push
    subprocess.run(["git", "-C", REPO_DIR, "add", "."], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", f"Add {filename}"], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "push"], check=True)

    return f"ファイル {filename} を push しました！", 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

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
