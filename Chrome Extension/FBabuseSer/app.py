from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pickle
import re
from pythainlp.tokenize import word_tokenize
import numpy as np
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

word_vectors = KeyedVectors.load("fb_vectors.kv", mmap='r')
clf = pickle.load(open('clf_model.sav', 'rb'))

paraDict = {'กู': 'เ̲ร̲า', 'กุ': 'เ̲ร̲า', 'กรู': 'เ̲ร̲า', 'มึง': 'คุ̲̲ณ', 'เมิง': 'คุ̲̲ณ', 'เมริง': 'คุ̲̲ณ', 'มรึง': 'คุ̲̲ณ', 'มุง': 'คุ̲̲ณ', 'มรุง': 'คุ̲̲ณ', 'เหี้ย': 'แ̲ย่̲', 'ควย': '!̲!̲!', 'สัส': 'ไ̲ม่̲̲ด̲ี', 'ชิบหาย': 'แ̲ย่̲', 'ฉิบหาย': 'แ̲ย่̲', 'ตอแหล': 'โ̲ก̲ห̲ก', 'หน้าด้าน': 'อ̲ด̲ท̲น', 'ดอก': 'แ̲ย่̲', 'กะหรี่': '!̲!̲!', 'ร่าน': 'อ̲ั̲ธ̲ย̲า̲ศ̲ั̲ย̲ด̲ี', 'แรด': 'อ̲ั̲ธ̲ย̲า̲ศ̲ั̲ย̲ด̲ี', 'สันดาน': 'น̲ิ̲ส̲ั̲ย', 'แม่ง': ' ̲!̲!̲!', 'ระยำ': 'แ̲ย่̲', 'แดก': 'ก̲ิ̲น', 'หี': '!̲!̲!', 'หัวดอ': '!̲!̲!', 'กระโปก': '!̲!̲!', 'ซ่อง': 'ส̲ถ̲า̲น̲บ̲ร̲ิ̲ก̲า̲ร', 'ผัว': 'ส̲า̲ม̲ี', 'เมีย': 'ภ̲ร̲ร̲ย̲า', 'ตรู': 'เ̲ร̲า', 'สัด': 'ไ̲ม่̲̲ด̲ี', 'ส้นตีน': 'เ̲ท้̲̲า', 'ห่า': 'ไ̲ม่̲̲ด̲ี', 'เชี้ย': 'แ̲ย่̲', 'โง่': 'ค̲ิ̲ด̲น้̲̲อ̲ย', 'ไอ': 'คุ̲̲ณ', 'อี': 'คุ̲̲ณ', 'อิ': 'คุ̲̲ณ', 'แหก': 'บ̲อ̲ก', 'แตด': '!̲!̲!', 'ตีน': 'เ̲ท้̲̲า', 'แคม': '!̲!̲!', 'อัย': 'คุ̲̲ณ', 'อั่ย': 'คุ̲̲ณ', 'วะ': 'อ̲ะ'}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def index():
    if (request.method == 'POST'):
    	jsdata = request.form['javascript_data']

    	res = classify_msg(jsdata, clf)[0]    
    	if res == 0:
    		return 'True'
    	else:
    		return 'False'
    else:
    	return jsonify({'sending':"not post"})
    
@app.route("/para", methods=['GET', 'POST'])
def para():
    if (request.method == 'POST'):
    	jsdata = request.form['javascript_data']

    	return str(para(jsdata, paraDict))
    else:
    	return jsonify({'sending':"not post"})

if __name__ == "__main__":
    app.run(debug=True)
    
def para(msg, paraDict):
    for i, v in paraDict.items():
        if i in msg:
            msg = msg.replace(i, v)
    return msg

def replace_url(text):
    URL_PATTERN = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    return re.sub(URL_PATTERN, 'xxurl', text)

def replace_rep(text):
    def _replace_rep(m):
        c,cc = m.groups()
        return f"{c}xxrep"
    re_rep = re.compile(r"(\S)(\1{2,})")
    return re_rep.sub(_replace_rep, text)


def rule_based_preprocess(text):
    res = text.lower().strip()
    res = res.replace('\r', ' ')
    res = replace_url(res)
    res = replace_rep(res)
    return res

def wordvec(msg):
    sentence = word_tokenize(msg, engine='ulmfit')
    avg_sent = np.zeros(300)
    avg_c = 0
    for j in sentence:
        if j in word_vectors.vocab:
            avg_sent += word_vectors.get_vector(j)
            avg_c+=1
    score = avg_sent/avg_c
    
    return score

def classify_msg(msg, model):
    msg = rule_based_preprocess(msg)
    vector = wordvec(msg)
    return model.predict([vector])