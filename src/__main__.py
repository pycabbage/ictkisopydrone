#!/usr/bin/env python3
# coding: utf-8

import threading
import socket
import sys
import time
import cv2


class Tello:
    def __init__(self, host="", port=9000, COMMAND_DELAY=True):
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
        recvThread = threading.Thread(target=self._recv_tello)
        recvThread.start()

        self._send_command("command")

    def _recv_tello(self):
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

    def _send_command(self, c, interval=0.3, delay=3.0):
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

        if isinstance(c, str):
            if self.command_delay:
                time.sleep(interval)
            c = c.lower()
            sent = self.sock.sendto(c.encode("utf-8"), self.tello_address)
            print(c, ">> Tello")
            # self._recv_tello()
            print("SEND COMMAND '{}'".format(c))
            if self.command_delay:
                time.sleep(interval)
        elif isinstance(c, list):
            if self.command_delay:
                time.sleep(interval)
            for s in c:
                s = s.lower()
                sent = self.sock.sendto(s.encode("utf-8"), self.tello_address)
                print(s, ">> Tello")
                # self._recv_tello()
                time.sleep(interval)
        else:
            raise TypeError
        time.sleep(delay)

    def takeoff(self):
        print("TAKEOFF")
        """離陸"""
        return self._send_command("takeoff")

    def land(self):
        """着陸"""
        print("LAND")
        return self._send_command("land")

    def up(self, x: int):
        """
        x[cm]上昇する
        x: int 20-500
        """
        return self._send_command("up {}".format(x))

    def down(self, x: int):
        """
        x[cm] 下降する
        x: int 20-500
        """
        return self._send_command("down {}".format(x))

    def left(self, x: int):
        """
        x[cm] 左に移動する
        x: int 20-500
        """
        return self._send_command("left {}".format(x))

    def right(self, x: int):
        """
        x[cm] 右に移動する
        x: int 20-500
        """
        return self._send_command("right {}".format(x))

    def forward(self, x: int):
        """
        x[cm] 前に移動する
        x: int 20-500
        """
        return self._send_command("forward {}".format(x))

    def back(self, x: int):
        """
        x[cm] 後ろに移動する
        x: int 20-500
        """
        return self._send_command("back {}".format(x))

    def cw(self, x: int):
        """
        x[cm] 後ろに移動する
        x: int 20-500
        """
        return self._send_command("cw {}".format(x))

    def flip(self, x="f"):
        """
        x[cm] 後ろに移動する
        x: int 20-500
        """
        return self._send_command("flip {}".format(x))


if __name__ == '__main__':
    t = Tello()
    t.takeoff()
    t.forward(30)
    t.cw(90)
    t.forward(30)
    t.land()
