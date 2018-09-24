import websocket
# import time

def on_message(ws, message):
    print('On message: ', message)

def on_error(ws, error):
    print('On error: ', error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("on_open")
    # def run(*args):
    #     for i in range(3):
    #         time.sleep(1)
    #         ws.send("Hello %d" % i)
    #     time.sleep(1)
    #     ws.close()
    #     print("thread terminating...")
    # thread.start_new_thread(run, ())
    print('Sending ciao')
    ws.send(b"Ciao")
    print('Sending bytes')
    ws.send(b'\xac\xed\x00\x05sr\x00)io.mirko.boundary.UserNotificationMessage\xd5\x1a\xa2\xdc\x9d\xafl$\x02\x00\x01L\x00\x04usert\x00\x16Lio/mirko/entity/User;xpsr\x00\x14io.mirko.entity.UserA^b<+\x199t\x02\x00\x02L\x00\tfirstNamet\x00\x12Ljava/lang/String;L\x00\x08lastNameq\x00~\x00\x04xpt\x00\x05Mirkot\x00\tBonasorte')


if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:8080/dashner/user_notifications",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
