from bson import json_util
import json

def Resposta(item) -> dict:
    doc = json_util.dumps(item)
    return json.loads(doc)
