import base64

import pyduinocli
import os
import shortuuid
import shutil
arduino = pyduinocli.Arduino("./arduino-cli")

arduino.config.set("board_manager.additional_urls", ["https://arduino.esp8266.com/stable/package_esp8266com_index.json"])
# print(arduino.config.dump())
# print(arduino.board.listall())

arduino.core.install(["esp8266:esp8266"])

TEMP_DIR= os.path.join(os.path.dirname(__file__),"temp")
brds = arduino.board.search("NodeMCU 1.0 (ESP-12E Module)")

# print(str(brds))

def check_tmp_dir():
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)

def decoad_base64(base64_string):
    return base64.b64decode(base64_string).decode('utf-8')

def create_temp_project(data):
    check_tmp_dir()
    data=decoad_base64(str(data))
    tmp_uuid=str(shortuuid.ShortUUID().random(length=6))
    # print(tmp_uuid)
    temp_project =os.path.join(TEMP_DIR, tmp_uuid)
    os.mkdir(temp_project)
    temp_ino = os.path.join(temp_project, str(tmp_uuid+".ino"))
    with open(temp_ino,'w', encoding='utf-8') as f:
        f.write(data)
    # print(temp_ino)
    return temp_ino

def delete_temp_project(temp_ino):
    shutil.rmtree(temp_ino)

def ino_builder(temp_ino):
    inoproject, ino = os.path.split(temp_ino)
    fqbn = "arduino:avr:uno"
    res = arduino.compile(fqbn=fqbn, sketch=temp_ino)
    build_res = res['result']['builder_result']['build_path']
    print(build_res)

    hex_path = os.path.join(build_res, ino+".hex")
    print(hex_path)
    with open(hex_path, "rb") as f:
        hex = f.read()
        b64enHex = base64.b64encode(hex).decode('ascii')

    delete_temp_project(inoproject)

    return b64enHex

def nodemcu_builder(temp_ino):
    print("진입")
    inoproject, ino = os.path.split(temp_ino)
    fqbn = "esp8266:esp8266:nodemcuv2"
    try:
        res = arduino.compile(fqbn=fqbn, sketch=temp_ino, export_binaries=True, build_path=os.path.join(inoproject, "build"))
    except:
        return "compile failed"
    
    build_res = res['result']['builder_result']['build_path']

    bin_path = os.path.join(build_res,"esp8266.esp8266.nodemcuv2" , ino+".bin")

    with open(bin_path, "rb") as f:
        hex = f.read()
        b64enHex = base64.b64encode(hex).decode('ascii')
    delete_temp_project(inoproject)

    return b64enHex

def nodemcu_fbuilder(temp_ino):
    inoproject, ino = os.path.split(temp_ino)
    fqbn = "esp8266:esp8266:nodemcuv2"
    res = arduino.compile(fqbn=fqbn, sketch=temp_ino, export_binaries=True, build_path=os.path.join(inoproject, "build"))


    build_res = res['result']['builder_result']['build_path']


    bin_path = os.path.join(build_res,"esp8266.esp8266.nodemcuv2" , ino+".bin")



    return bin_path