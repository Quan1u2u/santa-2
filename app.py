from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# ===== LOAD DATABASE (CẤM ĐỔI) =====
df = pd.read_csv("res.csv")

# Tạo map: target -> giver
giver_map = {}
for _, row in df.iterrows():
    giver_map[row["TARGET (Ten)"]] = row["Ten Nguoi Tang"]

# Lưu lượt hỏi
user_state = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user = data["user"]
    target = data["target"]
    question = data["question"].lower()

    if target not in giver_map:
        return jsonify({"error": "Không tìm thấy người nhận"}), 400

    if user not in user_state:
        user_state[user] = {"count": 0, "guessed": False}

    if user_state[user]["count"] >= 3:
        return jsonify({"answer": "❌ Bạn đã dùng hết 3 câu hỏi."})

    giver = giver_map[target]
    name_words = giver.split()
    char_len = len(giver.replace(" ", ""))

    user_state[user]["count"] += 1

    # ===== AI Q&A LIÊN QUAN TÊN =====
    answer = "🤖 AI: "

    if "mấy từ" in question:
        answer += f"Tên người đó có {len(name_words)} từ."
    elif "dài" in question:
        answer += "Tên người đó khá dài." if char_len >= 15 else "Tên người đó không quá dài."
    elif "họ" in question:
        answer += f"Họ của người đó phổ biến trong lớp."
    else:
        answer += "Câu hỏi này có liên quan đến cấu trúc tên."

    return jsonify({
        "answer": answer,
        "remaining": 3 - user_state[user]["count"]
    })

@app.route("/guess", methods=["POST"])
def guess():
    data = request.json
    user = data["user"]

    if user_state.get(user, {}).get("guessed"):
        return jsonify({"result": "❌ Bạn chỉ được đoán 1 lần!"})

    user_state.setdefault(user, {})["guessed"] = True
    return jsonify({"result": "🎄 Đã ghi nhận lượt đoán của bạn!"})

if __name__ == "__main__":
    app.run()
