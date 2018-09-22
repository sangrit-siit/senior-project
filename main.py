from flask import Flask, render_template, request, jsonify, Response
import requests, json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['GET','POST'])
def homepage():
    f = 'researchers'
    s = None
    result = None

    try:
        s = request.args['s']
        f = request.args['f']
        result = search_enname(s)
    except:
        pass

    return render_template('home/index.html', f=f, s=s, result=result)


@app.route('/profile/<researcher_id>', methods=['GET', 'POST'])
def profile(researcher_id):
    result = get_profile(researcher_id)
    r = Response(json.dumps(result, ensure_ascii=False), mimetype="application/json")
    # print(json.dumps(result,ensure_ascii=False))
    return render_template('profile/index.html', r=result)

@app.route("/search")
def search():

    print(request.args)

    return jsonify(request.args)

def search_enname(querystring):
    query = "http://35.240.224.81:9200/researcher/_search?q=search_result.en_name:{}".format(querystring)
    try:
        result = requests.get(url=query).json().get('hits').get('hits')
        result = [{"name_th": item['_source']['search_result']['th_name'],
                  "name_en": item['_source']['search_result']['en_name'],
                  "keywords": item['_source']['search_result']['keywords'],
                  "id": item['_source']['search_result']['id']} for item in result]
    except:
        return []
    else:
        return result

def get_profile(researcherid):
    query = "http://35.240.224.81:9200/researcher/_search?q=search_result.id:{}".format(researcherid)
    try:
        result = requests.get(url=query).json().get('hits').get('hits')
    except:
        return []
    else:
        return result[0]['_source']

