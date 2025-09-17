import json
from jsonschema import validate, ValidationError

EXTRACT_SCHEMA = {
  "type":"object",
  "properties":{
    "customer_name":{"type":"string"},
    "issue":{"type":"string"},
    "priority":{"type":"string","enum":["low","medium","high",""]}
  },
  "required":["customer_name","issue","priority"]
}

def try_parse_and_validate(s: str):
    s = s.strip()
    # try to isolate a JSON block if model added prose
    start, end = s.find("{"), s.rfind("}")
    if start != -1 and end != -1 and end > start:
        s = s[start:end+1]
    obj = json.loads(s)
    validate(obj, EXTRACT_SCHEMA)
    return obj
