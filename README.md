# G3 DrivingGUI 🧠🕹️  
*A StarCraft-inspired GUI for intuitive FRC robot control — by Team 1648: G3 Robotics*

## 🚀 Overview

The **G3 Command Interface** is a real-time robot-driving GUI designed to make controlling your FRC robot feel like commanding units in *StarCraft II*. Built by **Team 1648 – G3 Robotics**, this tool enables operators to direct their robot with clicks, and high-level commands instead of joystick-only inputs.

Whether you're driving at competition or practicing autonomous coordination, this interface gives you a whole new strategic layer of control.

## 🎮 Features

- **Unit-Style Control**  
  Right click a point to move to it, just like an RTS game.

- **Live Field Visualization**  
  See a 2D top-down view of the field and robot in real-time, powered by telemetry and odometry.

- **Multiple Control Modes**  
  Toggle between manual (joystick) or semi-auto (click-to-move).

- **Hotkeys & UI Optimizations**  
  Designed for speed: quick-access keys and status indicators.

## 🛠️ Installation

### Requirements
- Python 3.13+
- `pillow`, `pygame`, `pynetworktables`
- A positive mindset 😊

### Setup

```bash
git clone https://github.com/darknessraider/DrivingGUI
cd DrivingGUI
pip install -r requirements.txt
python main.py
