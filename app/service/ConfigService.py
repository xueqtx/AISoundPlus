from app.gateway.db.SqliteDB import DBTool
from .FileService import list_mp3_files
import json


def query(job_id):
    db = DBTool()
    json_config = []
    try:
        result = db.executeQuery("select config from audio_config where id = ? ", job_id)
        json_config = json.loads(result[0][0])
    except:
        print("")
    finally:
        return json_config
        db.close()


def update(job_id, form):
    db = DBTool()
    db.c.execute("INSERT OR REPLACE INTO audio_config(id,type,config) VALUES( ?,?,? )", (job_id, '1', form))
    db.conn.commit()
    db.close()
    return True


def get_music_list():
    result = []
    file_list = list_mp3_files("music")
    for i in file_list:
        result.append({"value": i, "label": i})
    return result
