import havoc, havocui
import time
import requests
import json
import os

start_time = time.time()
current_dir = os.getcwd()
install_path = "/data/extensions/havoc-bot/"
conf_path = current_dir + install_path + "settings.json"
pane = havocui.Widget("settings", True)
settings = {
    "dingtalk": "Please input here",
    "wechat": "Please input here",
}

def send_messages(message):
    global settings
    session = requests.Session()

    if settings["dingtalk"].startswith("https://oapi.dingtalk.com/robot/send?access_token="):
        send = {
            "msgtype": "markdown",
            "markdown": {
                "title":"有新的推送消息",
                "text": message
            }
        }
    elif settings["wechat"].startswith("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="):
        send = {
            "msgtype": "text",
            "text": {
                "content": message
        }
    }
    else:
        havocui.messagebox("ERROR", "Invalid webhook!")

    send = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }

    req = session.post(settings["wechat"], json=send, timeout=7)
    if req.json()["errcode"] != 0:
        print(f"Error occurred in sending messages to wechat bot: {req.text}")
        print(f"message: {message}")


def monitor_process(demon_id):
    global start_time
    current_time = time.time()
    if current_time - start_time <= 5:
        return
    demon = havoc.Demon(demon_id)

    msg = """
新主机上线!
主机ID: {demond_id}  
用户: {user}
计算机名称: {pc}
操作系统: {os}
外网IP: {eip}
内网IP: {iip}
上线时间: {time}
Implant总数: {sum}
""".format(
    demond_id=demon.DemonID.strip(),
    user=demon.User.strip(),
    pc=demon.Computer.strip(),
    os=demon.OS.strip(),
    eip=demon.ExternalIP.strip(),
    iip=demon.InternalIP.strip(),
    time=time.asctime(),
    sum=len(havoc.GetDemons()),
)
    send_messages(msg)  


def get_wechat_api_key(text):
    global settings
    settings["wechat"] = text

def get_dingtalk_api_key(text):
    global settings
    settings["wechat"] = text


def save_settings():
    global settings
    global conf_path
    print(conf_path)
    print(settings)
    with open(conf_path, "w") as fp:
        json.dump(settings, fp)


def open_settings():
    global settings
    pane.clear
    pane.addLabel("<h3 style='color:#bd93f9'>Settings:</h3>")
    pane.addLabel("<span style='color:#71e0cb'>DingTalk API Key:</span>")
    pane.addLineedit(settings["dingtalk"], get_dingtalk_api_key)
    pane.addLabel("<span style='color:#71e0cb'>Wechat API Key:</span>")
    pane.addLineedit(settings["wechat"], get_wechat_api_key)
    pane.addButton("save", save_settings)
    pane.setSmallTab()
    print("open settings")



def load_settings():
    global settings
    global conf_path

    if not os.path.exists(conf_path):
        open(conf_path, 'w').close() 
    else:
        with open(conf_path, "r") as f:
            settings = json.load(f)
 
        

load_settings()        
event = havoc.Event("events")
event.OnNewSession(monitor_process)
havocui.createtab("Bot", "settings", open_settings)
