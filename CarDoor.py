from ElevatorComponent import ElevatorComponent
from Messages import *
from time import sleep

class STATE(Enum):
    """
    States used exclusively by Car Door
    """
    OPENED = "opened"
    OPENING = "opening"
    CLOSED = "closed"
    CLOSING = "closing"


class CarDoor(ElevatorComponent):
    
    def __init__(self, CarCtrl, ElevatorCar):
        super().__init__()
        # input
        self.IN = None    # Received from Car Controller

        # output
        self.OUT = None # Recipient is Car Controller and Elevator Car

        # Coupled Input/Output: Sends and receives from Car Controller and sends to Elevator Car, so an instance of the both is needed
        self.ctrl = CarCtrl
        self.car = ElevatorCar

        # component vars
        self.state = STATE.CLOSED # initialize in CLOSED state

        self.processing_time = 5.0
        self.motion_time = 3.0
    
    def setIN(self, IN):
        # in ? job && cmdDoor == OPEN
            # Above Met: MoveTo STATE.OPENING
        self.IN = IN
        if(self.IN):
            if(self.IN.contents["value"] == CommandDoor.DOOR_CAR_OPEN):
                self.state = STATE.OPENING
                        
                # Generate IN Log 
                self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","Car Door","R","in",self.IN)
                
                # in ? job && cmdDoor == CLOSE
                # Above Met: MoveTo STATE.CLOSING
            elif(self.IN.contents["value"] == CommandDoor.DOOR_CAR_CLOSE):
                self.state = STATE.CLOSING
                # Generate IN Log 
                self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","Car Door","R","in",self.IN)

    def state_processor(self):
        while True:
            if self.state == STATE.CLOSED:
                pass
                    # Generate IN Status Log 
                    # TODO: if(self.IN):
                        # TODO: self.write_log(self.get_sim_time(), self.get_real_time(),"Car Ctrl","","C",self.IN.contents)
               
            elif self.state == STATE.OPENING:
                # Send message MsgDoor -> OUT
                self.OUT = MsgDoor("out", StatusDoor.DOOR_CAR_OPENED, 100, False)

                # MoveTo STATE.OPENED
                self.state = STATE.OPENED
                
            elif self.state == STATE.OPENED:
                # Do some timeout logic, MoveTo STATE.CLOSING
                
                # Generate OUT Log 
                self.write_log(self.get_sim_time(), self.get_real_time(),"Car Door","Car Ctrl","S","out",self.OUT)
                self.write_log(self.get_sim_time(), self.get_real_time(),"Car Door","Elevator Car","S","out",self.OUT)
                
                self.ctrl.setiDoor(self.OUT)
                self.car.setoStDoorMsg(self.OUT)

                sleep(self.processing_time)
                sleep(self.motion_time)
                self.state = STATE.CLOSING
                
            elif self.state == STATE.CLOSING:
                # Send message MsgDoor -> OUT
                self.OUT = MsgDoor("out", StatusDoor.DOOR_CAR_CLOSED, 100, False)
                # MoveTo STATE.CLOSED
                self.state = STATE.CLOSED

                # Generate OUT Log 
                self.write_log(self.get_sim_time(), self.get_real_time(),"Car Door","Car Ctrl","S","out",self.OUT)
                self.write_log(self.get_sim_time(), self.get_real_time(),"Car Door","Elevator Car","S","out",self.OUT)

                self.ctrl.setiDoor(self.OUT)
                self.car.setoStDoorMsg(self.OUT)

    def main(self):
        self.state_processor()
        
    
if __name__ == '__main__':
    ctrl = None
    car = None
    door = CarDoor(ctrl, car)
    door.main()