import subprocess

getData = "getData.js"
publishData = "publishData.js"
network = "abs_ccprojchain_hc2885_hc2885"


def publish(content):
    publishDataBash = "cd blockchain && truffle exec {file} --network {net} {date} {arg1} {arg2} {arg3} {arg4} {arg5} {arg6} "
    bash = publishDataBash.format(file=publishData, net=network, date=content["date"], arg1=content["visitor"]
                                  , arg2=content["male"], arg3=content["female"], arg4=content["emo_neg"],
                                  arg5=content["emo_pos"], arg6=content["emo_mild"])
    stream = subprocess.Popen(bash, shell=True, stdout=subprocess.PIPE, text=True)
    stdout = stream.stdout.read()
    return True


def get(content):
    getDataBash = "cd blockchain && truffle exec {file} --network {net} {date}"
    field = ["visiter", "male", "female", "emo_neg", "emo_pos", "emo_mild"]

    bash = getDataBash.format(file=getData, net=network, date=content["date"])
    # stream = os.popen(bash)
    stream = subprocess.Popen(bash, shell=True, stdout=subprocess.PIPE, text=True)
    stdout = stream.stdout.read()
    val = stdout.split()[-8:-2]
    # print(val)
    res = {}
    if val[0].isdigit():
        for i in range(6):
            res[field[i]] = val[i]
    else:
        res = "File Not Exist"
    return res


def main(data):
    if data["type"] == "publishData":
        res = publish(data["data"])
    elif data["type"] == "getData":
        res = get(data["data"])
    else:
        raise NotImplementedError

    return {"results": res}


if __name__ == '__main__':
    # test publish
    '''res = main({"type": "publishData",
                "data": {"date": "June1", "visitor": "50", "male": "20", "female": "100", "emo_neg": "10",
                         "emo_pos": "20", "emo_mild": "30"}})
    print(res)'''

    # test get
    res = main({"type": "getData", "data": {"date": "May3"}})
    print(res)
