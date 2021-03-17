# ictkisopydrone
ICT基礎Lab. for Junior　～Pythonプログラミング～ Python言語を用いたドローン制御プログラム作成 用のラッパーモジュール

# 使い方

```Python3

from ictdrone import Tello

drone = Tello()
drone.takeoff()
drone.forward(50)
drone.right(100)
drone.rotate(180)
drone.land()
```
