from flask_apscheduler import APScheduler
from flask import Flask, render_template, request, jsonify
from datetime import timedelta
from main import audio_job
import service.ConfigService as configService


class Config(object):
    JOBS = [
        {
            'id': '1',
            'func': '__main__:audio_job',
            'args': '1',
            'trigger': 'cron',
            'hour': 13,
            'minute': 41
        },
        {
            'id': '2',
            'func': '__main__:audio_job',
            'args': '2',
            'trigger': 'cron',
            'hour': 16,
            'minute': 00
        }
    ]


app = Flask(__name__, template_folder="templates", static_folder="templates/static")
app.config.from_object(Config())  # 为实例化的flask引入配置


@app.route('/', methods=['GET', 'POST'])  # 首页路由
def index():
    return render_template('sound.html')


@app.route('/config.jhtml', methods=['GET', 'POST'])  # 配置页面
def config():
    request
    return render_template('config.html', job_id="1")


@app.route('/config/query.do', methods=['GET', 'POST'])  # 配置页面
def query():
    job_id = request.get_json()["job_id"]
    result = configService.query(job_id)
    response = result
    return jsonify(response)


@app.route('/config/update.do', methods=['POST'])  # 配置页面
def update():
    job_id = request.get_json()["job_id"]
    form = request.get_json()["form"]
    result = configService.update(job_id, form)
    response = result
    return jsonify(response)


@app.route('/config/getMusicList.do', methods=['GET', 'POST'])  # 配置页面
def list_mp3_file():
    result = configService.get_music_list()
    response = result
    return jsonify(response)


@app.route('/config/upload.do', methods=['GET', 'POST'])  # 配置页面
def upload():
    try:
        request.files['file'].save("music/" + request.files['file'].filename.replace(" ", "_"))
    except:
        return jsonify({"success": False})
    return jsonify({"success": True})


if __name__ == '__main__':
    # 自动重载模板文件
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # 设置静态文件缓存过期时间
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()
    Flask.run(app, '0.0.0.0')
