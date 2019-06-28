from socket import socket
from threading import Thread
from zlib import compress

from mss import mss


WIDTH = 1900
HEIGHT = 1000


def retreive_screenshot(conn):
    with mss() as sct:
        # The region to capture
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while 'recording':
            # Capture the screen
            img = sct.grab(rect)
            # Tweak the compression level here (0-9)
            pixels = compress(img.rgb, 6)

            # Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            # Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            # Send pixels
            conn.sendall(pixels)


def main(host):
    print (host)
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ''
    port = 5555
    s.bind((host, port))
    s.listen(5)
    try:
        print('Server started.')

        while 'connected':
            conn, addr = s.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=retreive_screenshot, args=(conn,))
            thread.start()
    finally:
        s.close()


if __name__ == '__main__':
    import platform
    host = platform.node()

    main(host)
