import os, time, argparse, math

try:
    from pythonosc import dispatcher, osc_server
    from pynput.keyboard import Key, Controller
except Exception as e:
    os.system("pip install pynput")
    os.system("pip install pythonosc")

keyboard = Controller()

def HandleIT(unused_addr, arg):
    global keyboard
    UsedKeys = [Key.space,Key.ctrl,Key.alt,Key.shift,"y","u",Key.f13,Key.f14]
    if arg == 0:
        for Button in UsedKeys:
            keyboard.release(Button)
    elif arg == 1:
        keyboard.press(Key.ctrl)
        keyboard.press(Key.alt)
        keyboard.press("u")
    elif arg == 2:
        keyboard.press(Key.ctrl)
        keyboard.press(Key.alt)
        keyboard.press("y")
    elif arg == 3:
        keyboard.press(Key.f13)
    elif arg == 4:
        keyboard.press(Key.f14)
    else:
        #Never gunna give you errors
        os.system("start /max https://youtu.be/dQw4w9WgXcQ ")
      

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=9001, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/avatar/parameters/OSCOut", HandleIT)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()