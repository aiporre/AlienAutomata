import time
class blockingMachine:
    def __init__(self,OnTime):
        # states
        self.blocked = False
        self.opened = True

        self.bad = False

        self.color = False
        self.OnTime = OnTime
        self.referenceTime = time.time()
        self.timer = 0


    def updateStates(self,bad):
        # inputs
        self.bad = bad
        # update timer
        self.updateTimer()

        blockTimeout = self.timer > self.OnTime
        opened = (blockTimeout and self.blocked) or \
                  (not(bad and not(self.blocked)) and self.opened)
        blocked = (bad and self.opened) or \
                   ( not(blockTimeout and not(self.opened)) and self.blocked)

        self.opened = opened
        self.blocked = blocked

        if (opened):
            print "State(" + str(self.timer) + "): OPEN"
        else:
            print "State(" + str(self.timer) + "): BLOCKED"

    def updateTimer(self):
        running = self.blocked and not(self.opened or self.bad)
        if running:
            self.timer = time.time() - self.referenceTime
        else:
            self.referenceTime = time.time()
            self.timer = 0

##
class light:
    def __init__(self,OnTime,lightColor):
        # states
        self.timer = 0
        self.stateOn = False
        self.stateOff = True
        self.blockOut = False
        self.letThrough = False
        self.color = False
        self.OnTime = OnTime
        self.referenceTime = time.time()
        self.lightColor = lightColor

    def updateStates(self,blockOut,letThrough,color):

        self.blockOut = blockOut
        self.letThrough = letThrough
        self.color = color

        self.updateTimer()

        lightTimeout = self.timer > self.OnTime
        isColor = (color == self.lightColor)

        stateOn = (letThrough and isColor and self.stateOff) or \
                  ((not(blockOut or lightTimeout) or self.stateOff) and self.stateOn)
        stateOff = ((blockOut or lightTimeout) and self.stateOn) or \
                   ( not(letThrough and isColor and (not self.stateOn)) and self.stateOff)

        self.stateOn = stateOn
        self.stateOff =  stateOff
        if (stateOn):
            print self.lightColor + "(" + str(self.timer) + "): ON"
        else:
            print self.lightColor + "(" + str(self.timer) + "): OFF"
    def updateTimer(self):
        running = self.stateOn and not(self.stateOff or (self.color == self.lightColor))
        if running:
            self.timer = time.time() - self.referenceTime
        else:
            self.referenceTime = time.time()
            self.timer = 0


print "test light red..."
light1 = light(10,"red")
light1.updateStates(False,True,"red")
cnt = 0

while(cnt<15):
    cnt += 1
    print "==========(" + str(cnt) + ")==========="
    light1.updateStates(False, True, "none")
    time.sleep(1)


print "test light blocking..."
blocker = blockingMachine(10)
blocker.updateStates(True)
cnt = 0

while(cnt<15):
    cnt += 1
    print "==========(" + str(cnt) + ")==========="
    blocker.updateStates(False)
    time.sleep(1)

print "test comsumer..."
blocker = blockingMachine(5)
lightRed = light(3,"red")
lightBlue = light(3,"blue")
lightGreen = light(3,"green")
stack = ["green", "blue", "blue"]

cnt = 0
delay = 0.5


def putMoreElements(cnt,stack):
    if(cnt == 10):
        stack.append("green")
        stack.append("blue")
    if (cnt == 20):
        stack.append("green")
        stack.append("red")
        stack.append("green")
        stack.append("blue")
    if (cnt == 30):
        stack.append("red")
        stack.append("blue")
    if (cnt == 32):
        stack.append("blue")
    if (cnt == 40):
        stack.append("red")
    if (cnt == 42):
        stack.append("red")
    if (cnt == 50):
        stack.append("green")
        stack.append("blue")
        stack.append("blue")

    return stack


while(cnt<60):
    cnt += 1
    print "==========(" + str(cnt * delay) + ")==========="
    # Read queue

    slack = putMoreElements(cnt,stack)
    if(len(stack)>0):
        colorObject = stack.pop()
        print "Queue value : " + colorObject
    else:
        colorObject = "none"
        print "Queue value : " + colorObject
    ##



    # Update inputs
    forbiddenColor = colorObject == "red"


    # Updated blocking state
    blocker.updateStates(forbiddenColor)
    letThrough = blocker.opened
    blockOut = blocker.blocked
    # Update lights
    lightGreen.updateStates(blockOut,letThrough,colorObject)
    lightBlue.updateStates(blockOut,letThrough,colorObject)
    lightRed.updateStates(False,blockOut,colorObject)

    time.sleep(delay)