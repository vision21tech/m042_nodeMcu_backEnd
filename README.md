m042 nodeMcu backEnd
=

m042 어플리케이션의 아두이노 컴파일러를 담당하는 서버입니다.
칩셋 정보와 코드를 받아 컴파일 후 다시 어플리케이션으로 전송합니다.

설치
-
```
python -m venv venv
pip install -r requirement.txt
```
실행
-
```app.py```를 실행하기 전, ```arduino.py```를 먼저 실행하고 ```app.py```를 실행시켜 주세요. 이 과정은 프로젝트를 처음 실행할 때 한번만 하면 됩니다.
