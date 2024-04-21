import os, time, pyautogui
pg = pyautogui
class air:
    def on():
        time.sleep(2)
        pg.write("ir universal ac Cool_hi")
        pg.press('enter')
    
    def off():
        time.sleep(2)
        pg.write("ir universal ac Off")
        pg.press('enter')

class Tv:
    def power():
        time.sleep(2)
        pg.write("ir universal tv Power")
        pg.press('enter')
    
    def mute():
        time.sleep(2)
        pg.write("ir universal tv Mute")
        pg.press('enter')
    

Tv.mute()
