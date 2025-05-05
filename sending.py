from networktables import NetworkTables
import networktables as nt
import constants

class Pose2D:
    def __init__(self, x: float=0, y: float=0, theta: float=0):
        self.x = x
        self.y = y
        self.theta = theta


    def copy(self):
        return Pose2D(self.x, self.y, self.theta)
    
    def add(self, pose):
        if pose.__class__ is not self.__class__:
            raise ValueError("must give another pose to addition expression")

        return Pose2D(self.x + pose.x, self.y + pose.y, self.theta + pose.theta)
    
    def set_to_pose(self, pose):
        if pose.__class__ is not self.__class__:
            raise ValueError("must give another pose to set expression")
        
        self.x = pose.x
        self.y = pose.y
        self.theta = pose.theta

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}, theta: {self.theta}" 


class SendablePose2D:
    NetworkTables.initialize(server="localhost")
    table = nt.NetworkTables.getTable(constants.NETWORK_TABLE_NAME)

    def __init__(self, pose: Pose2D, entry_name: str):
        self.pose = pose  

        self.x_entry: nt.NetworkTableEntry = self.table.getEntry(entry_name + "_x")
        self.y_entry: nt.NetworkTableEntry = self.table.getEntry(entry_name + "_y")
        self.theta_entry: nt.NetworkTableEntry = self.table.getEntry(entry_name + "_theta")
        self.set_pose(pose)

    
    def set_pose(self, pose: Pose2D):
        self.pose = pose.copy()
        
        self.x_entry.setDouble(self.pose.x)
        self.y_entry.setDouble(self.pose.y)
        self.theta_entry.setDouble(self.pose.theta)

class SendableBoolean:
    table = nt.NetworkTables.getTable(constants.NETWORK_TABLE_NAME)

    def __init__(self, value: bool, entry_name: str):
        self.value = value
        self.entry: nt.NetworkTableEntry = self.table.getEntry(entry_name)
        self.set_value(value)
    
    def set_value(self, value: bool):
        self.value = value
        self.entry.setBoolean(value)

