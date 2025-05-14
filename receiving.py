import sending
import networktables as nt

class ReceivablePose2D:
    def __init__(self, entry_name: str):
        table = sending.NetworkTableWrapper().table
        self.x_entry: nt.NetworkTableEntry = table.getEntry(entry_name + "_x")
        self.y_entry: nt.NetworkTableEntry = table.getEntry(entry_name + "_y")
        self.theta_entry: nt.NetworkTableEntry = table.getEntry(entry_name + "_theta")


    def get_pose(self):
        x = self.x_entry.getDouble(0)
        y = self.y_entry.getDouble(0)
        theta = self.theta_entry.getDouble(0)

        return sending.Pose2D(x, y, theta)


