from networktables import NetworkTables
import networktables as nt

class Pose2D:
    def __init__(self, x: float=0, y: float=0, theta: float=0):
        self.x = x
        self.y = y
        self.theta = theta


    def copy(self):
        return Pose2D(self.x, self.y, self.theta)


class CommunicablePose2D:
    NetworkTables.initialize(server="localhost")
    table = nt.NetworkTables.getTable("DrivingGUI")

    def __init__(self, pose: Pose2D, entry_name: str):
        self.pose = pose  

        self.x_entry: nt.NetworkTableEntry = self.table.getEntry(entry_name + "_x")
        self.y_entry: nt.NetworkTableEntry = self.table.getEntry(entry_name + "_y")
        self.theta_entry: nt.NetworkTableEntry = self.table.getEntry(entry_name + "_theta")

    
    def set_pose(self, pose: Pose2D):
        self.pose = pose.copy()
        
        self.x_entry.setDouble(self.pose.x)
        self.y_entry.setDouble(self.pose.y)
        self.theta_entry.setDouble(self.pose.theta)


class Robot:
    def __init__(self): 
        self.pose = Pose2D()

    def set_pose(self, pose: Pose2D):
        self.pose = pose
        return self
