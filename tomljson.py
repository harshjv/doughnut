import pytoml as toml
import ujson

def diff(a,b):
     ret_dict = {}
     for key,val in a.items():
         if b.has_key(key):
             if b[key] != val:
                 ret_dict[key] = [val,b[key]]
         else:
             ret_dict[key] = [val]
     for key,val in b.items():
         ret_dict.setdefault(key,[val])
     return ret_dict

with open('_doughnut.json', 'r') as fin:
    with open('_doughnut.toml', 'w') as fout:
        fout.write(toml.dumps(ujson.loads(fin.read())))


with open('_doughnut.toml', 'r') as fin:
    with open('_doughnut_1.json', 'w') as fout:
        fout.write(ujson.dumps(toml.loads(fin.read())))


with open('_doughnut.json', 'r') as f1:
    with open('_doughnut_1.json', 'r') as f2:
        o = ujson.loads(f1.read())
        t = ujson.loads(f2.read())
        print(o == t)
