from flask import Flask, render_template, request, session, redirect
from function import error, login_required
from flask_session import Session
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "1234"
app.config["MYSQL_DB"] = ""

@app.route('/read-post', methods=['POST', 'GET'])
def read_post():
    current_diary_id = request.form.get("button") if request.method == "POST" else request.args.get("diary_id")

    # 데이터베이스에서 글 읽어오는 코드
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT diary_id, diary_title, diary_cont, diray_date FROM diary WHERE user_id = ? ORDER BY diary_id;",
        session["user_email"],
    )
    diary_list = cur.fetchall()
    cur.close()

    # 현재 글의 이전 글과 다음 글 찾기
    diary = {}
    prev_diary_id, next_diary_id = 0, 0
    for diary_id, diary_title, diary_cont, diary_date in diary_list:
        if diary_id < current_diary_id:
            prev_diary_id = diary_id
        elif current_diary_id < diary_id:
            next_diary_id = diary_id
            break
        else:
            diary["title"] = diary_title
            diary["cont"] = diary_cont
            diary["date"] = diary_date

    return render_template(
        "read-post.html",
        prev_diary_id=prev_diary_id,
        next_diary_id=next_diary_id,
        diary=diary,
    )

if __name__ == '__main__':
    app.run(debug=True)
