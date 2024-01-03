def checkid(videoid):
    import json
    try:
        with open("log.json", 'r') as json_file:
            existing_data = json.load(json_file)
    except:
        existing_data = [{}]
    
    for indexs, loadedjsonfile in enumerate(existing_data):
        getid = loadedjsonfile.get("SunnySkyzId", 0)
        if getid == videoid:
            if loadedjsonfile["Status"] == "Downloaded":
                return {"downloaded": True, "existing_data": existing_data}
            else:
                return {"downloaded": False, "jsondata": loadedjsonfile, "existing_data": existing_data, "index": indexs}
    
    if not existing_data[0]:
        existing_data.pop()
    return {"downloaded": False, "jsondata": False, "existing_data": existing_data}
    
def count_vidoes():
    import json
    with open("log.json", 'r') as file:
        log = json.load(file)
    return len(log)

def updatejson(new_data):
    import json
    with open("log.json", "w") as file:
        json_data_str = json.dumps(new_data, indent=4)
        file.write(json_data_str)

def errjs(errk):
    import json
    try:
        with open('err.json', 'r') as err:
            errlist = json.load(err)
    except:
        errlist = []
    if str(errk) in errlist:
        return {'skip': True}
    else:
        return {'skip': False, 'errlist': errlist}
