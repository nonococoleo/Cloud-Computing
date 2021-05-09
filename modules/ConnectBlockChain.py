import subprocess

getData = "getData.js"
publishData = "publishData.js"
network = "abs_ccprojchain_hc2885_hc2885"


def publish(content):
    publishDataBash = "cd blockchain && truffle exec {file} --network {net} {date} {arg1} {arg2} {arg3} {arg4} {arg5} {arg6} "
    bash = publishDataBash.format(file=publishData, net=network, date=content["date"], arg1=content["visiter"]
                                  , arg2=content["male"], arg3=content["female"], arg4=content["emo_neg"],
                                  arg5=content["emo_pos"], arg6=content["emo_mild"])
    stream = subprocess.Popen(bash, shell=True, stdout=subprocess.PIPE, text=True)
    stdout = stream.stdout.read()
    return stdout


def get(content):
    getDataBash = "cd blockchain && truffle exec {file} --network {net} {date} {arg1}"
    field = {"visiter": "1", "male": "2", "female": "3", "emo_neg": "4", "emo_pos": "5", "emo_mild": "6"}

    bash = getDataBash.format(file=getData, net=network, date=content["date"], arg1=field[content["field"]])
    stream = subprocess.Popen(bash, shell=True, stdout=subprocess.PIPE, text=True)
    stdout = stream.stdout.read()
    return stdout


def main(data):
    if data["type"] == "publishData":
        res = publish(data["data"])
    elif data["type"] == "getData":
        output = get(data["data"])
        val = output.split()[-3]
        if val.isdigit():
            return int(val)
        else:
            return "Not exist!"
    else:
        raise NotImplementedError

    return res


if __name__ == '__main__':
    # test publish
    res = main({"type": "publishData",
                "data": {"date": "June1", "visiter": "50", "male": "20", "female": "100", "emo_neg": "10",
                         "emo_pos": "20", "emo_mild": "30"}})
    print(res)

    # test get
    res = main({"type": "getData", "data": {"date": "June1", "field": "female"}})
    print(res)
