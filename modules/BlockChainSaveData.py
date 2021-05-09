import subprocess
import os

getData = "getData.js"
publishData = "publishData.js"
network = "abs_ccprojchain_rz1600_rz1600"

def main(data):
    if data["type"] == "publishData":
        content = data["data"]
        publishDataBash = "truffle exec {file} --network {net} {date} {arg1} {arg2} {arg3} {arg4} {arg5} {arg6} "
        bash = publishDataBash.format(file = publishData,net =  network, date = content["date"], arg1 = content["visiter"]
        ,arg2 = content["male"], arg3 = content["female"], arg4 = content["emo_neg"], arg5 = content["emo_pos"], arg6 = content["emo_mild"])
        os.system(bash)
    elif data["type"] == "getData":
        content = data["data"]
        getDataBash = "cd ../blockchain && truffle exec {file} --network {net} {date} {arg1}"
        field = {"visiter":"1", "male":"2", "female":"3", "emo_neg":"4", "emo_pos":"5", "emo_mild":"6"}
        bash = getDataBash.format(file = getData, net = network, date = content["date"], arg1 = field[content["field"]])
        #os.system(bash)
        stream = os.popen(bash)
        print("12312313")
        
        stdout = stream.read()
        #print(stdout)
        #print(len(stdout.split(" ")))
        
        val = stdout.split()[-3]
        if val.isdigit():
            return int(val)
        else:
            return "Not exist!"
    else:
        return False
    
    return True


if __name__ == '__main__':
    '''res = main({"type": "publishData", "data": {"date":"Jan1", "visiter":"50", "male":"20", 
            "female":"30", "emo_neg":"10", "emo_pos":"20", "emo_mild":"30"}})''' 
    #print(res)
    res = main({"type":"getData", "data":{"date":"May3", "field":"female"}})
    print(res)