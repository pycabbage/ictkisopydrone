import threading
import socket
import sys
import time
try:
    import cv2
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Module cv2 not found!\n[*]Please run `pip install opencv-python` or ask Fuminto.")


class PYtello:
    def setup_tello(self, host="", port=9000, COMMAND_DELAY=True):
        """
        Telloのセットアップを行う。
        """
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.locaddr = (host, port)
        self.tello_address = ('192.168.10.1', 8889)
        self.sock.bind(self.locaddr)
        self.command_delay = COMMAND_DELAY

        # recvThread create
        recvThread = threading.Thread(target=self.recv_tello)
        recvThread.start()

    def recv_tello(self):
        """
        Telloから応答を受け取る
        """
        while True:
            try:
                data, server = self.sock.recvfrom(2048)
                if b"ok" in data:
                    print("OK << Tello")
                if b"error" in data:
                    print("Error << Tello")

            except socket.error:
                print("socket error")
                return

    def go_tello(self, S, interval=0.3, delay=0.0):
        """
        S : コマンド(大文字小文字どちらでもいい)
        interval : 入力コマンド間の遅延
        delay : すべてのコマンド実行後の遅延

        command
        takeoff
        land
        up[down, left, right, forward, back] "Value" : "Value" = 20-500
        cw[ccw] "Value" : "Value" = 1-360
        flip "Direction" : "Direction" = l(left), r(right), f(forward), b(back)
        """
        _ALL_COMMANDS_ = ["command", "takeoff", "land", "up", "down",
                          "left", "right", "forward", "back", "flip",
                          "cw", "streamon", "streamoff", "emergency"]

        if isinstance(S, str):
            if self.command_delay:
                time.sleep(interval)
            S = S.lower()
            sent = self.sock.sendto(S.encode("utf-8"), self.tello_address)
            print(S, ">> Tello")
            self.recv_tello()
            if self.command_delay:
                time.sleep(interval)
        elif isinstance(S, list):
            if self.command_delay:
                time.sleep(interval)
            for s in S:
                s = s.lower()
                sent = self.sock.sendto(s.encode("utf-8"), self.tello_address)
                print(s, ">> Tello")
                self.recv_tello()
                time.sleep(interval)
        else:
            raise TypeError
        time.sleep(delay)

    def close_tello(self):
        print("Exit...")
        self.go_tello("LAND", delay=2.0)
        self.go_tello("END")
        self.sock.close()

    def query(self, Query=["battery", "speed", "time", "height", "wifi", "sdk", "sn"]):
        """
        Telloに現在の設定項目を問い合わせる。
        Queryになんかぶち込んでみて
        """
        if not isinstance(Query, list):
            raise TypeError
        Query_words = {
            "battery": "バッテリー残量",
            "speed": "設定速度",
            "time": "現在の飛行時間",
            "height": "現在の高さ",
            "temp": "ドローンの温度",
            "attitude": "ドローンの姿勢",
            "tof": "get distance value from TOF",
            "wifi": "接続Wi-FiのS/N比",
            "sdk": "SDKのバージョン",
            "sn": "シリアルナンバー"
        }
        for query_word, S in Query_words.items():
            if query_word not in Query:
                continue
            ans = self.go_tello(query_word + "?", interval=0.3)
            print(S, ":", ans)

    def set_speed(self, N):
        """
        Telloの速度を変更する。
        入力値Nに対しN[cm/s]に設定する。
        設定可能範囲：10 <= N <= 100
        """

        try:
            N = int(N)
        except ValueError:
            raise ValueError
        self.go_tello(N, interval=0.3)

    def video_on(self):
        """
        Telloのビデオストリームをオンにする
        """
        self.go_tello("streamon")

    def video_off(self):
        """
        Telloのビデオストリームをオフにする
        """
        self.go_tello("streamoff")

    def reject(delf):
        """
        Telloのすべてのプロセスを中断する
        要するに墜落する
        """
        self.go_tello("emergency")

    def go_tello_mid(self, x=0, y=0, z=0, speed=20, mid=""):
        """
        ミッションパッド(mid)のx, y, zに移動する
        """
        try:
            x, y, z, speed = map(str, [x, y, z, speed])
        except ValueError:
            raise ValueError
        self.go_tello(" ".join(["go", x, y, z, speed, mid]))

    def take_picture(self, parameter_list):
        """
        未実装
        """
        while True:
            frame = tello.read()
            if frame is None or frame.size == 0:
                continue
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            small_image = cv2.resize(image, dsize=(480, 360))
            cv2.imshow('OpenCV Window', small_image)

    def take_video(self, parameter_list):
        """
        未実装
        """
        while True:
            # (A)画像取得
            frame = drone.read()    # 映像を1フレーム取得
            if frame is None or frame.size == 0:    # 中身がおかしかったら無視
                continue
            # (B)ここから画像処理
            # OpenCV用のカラー並びに変換する
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            small_image = cv2.resize(image, dsize=(480, 360))   # 画像サイズを半分に変更

            # (X)ウィンドウに表示
            # ウィンドウに表示するイメージを変えれば色々表示できる
            cv2.imshow('OpenCV Window', small_image)
