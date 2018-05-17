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


if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:8080/dashner/user_notifications",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
