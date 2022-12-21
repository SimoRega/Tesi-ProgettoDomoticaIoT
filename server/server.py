from flask import Flask
from flask import request
import json
from enum import Enum
app = Flask(__name__)

class SystemState(Enum):
    WORKING = 0 #System is normally working, manage comms & data elaborations
    IDLE = 1 #System in energy saving mode,  just manage comms
    ERROR = 2 #Somethings broke normal workflow or some components went in error

currentState=SystemState.WORKING

def mergeDictionaries(x, y):
    z = x.copy()  
    z.update(y)
    return z

class myHouse():
  def __init__(self) -> None:
     self.myData = dict(generalState=0, sensors=dict(lux=0,hum=0,tmp=0), modules=[])
    
  def changeState(self, newState):
    self.myData["GeneralState"]=newState

  def getData(self):
    return self.myData #json.dumps(self.myData, indent=4)

  def updateDataSensors(self,newLux,newHum,newTmp):
    if newLux!=None : self.myData["sensors"]["lux"] = newLux
    if newHum!=None : self.myData["sensors"]["hum"] = newHum
    if newTmp!=None : self.myData["sensors"]["tmp"] = newTmp

  def addNewModule(self,newModule) :
    if newModule!= None : 
      for v in self.myData["modules"]:
        if v["modName"] == newModule["modName"]: return
      self.myData["modules"].append(newModule)
    
      

@app.route("/")
def test():
  return myIstance.getData()

@app.route("/sensorsData")
def updateData():
  newLux= request.args.get("lux")
  newHum= request.args.get("hum")
  newTmp= request.args.get("tmp")
  myIstance.updateDataSensors(newLux,newHum,newTmp)
  return myIstance.getData()

@app.route("/addModule")
def addModule():
  newModule = dict(modName=request.args.get("modName"),
                    modState=request.args.get("modState"))
  myIstance.addNewModule(newModule)
  return myIstance.getData()


if __name__ == "__main__":
  myIstance= myHouse()
  app.run(host="0.0.0.0", port=80, debug=True, use_reloader=False)