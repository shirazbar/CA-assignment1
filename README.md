# Cellular Automaton - Covid19
- Authors: Shiraz Bar Nave and Eden Meidan
- Description: This project creates a Covid19 Cell Automat. This Cell Automat creates a 200*200 model filled with creatures. The creature can infect each other with Covid19 in a set probability. The goal of this Cell Automat is to create at least three different waves of Covid19 virous. 
- Parameters: The user can input the fallowing parameters into the Cell Automat-
  * number of creatures [N]
  * percentage of sick creatures [D]
  * percentage of quick creatures [R]
  * number of generations a creature is contagious [X]
  * percentage of sick as a threshold [T]
  * high probability for creature to get infected from a sick neighbor [P high]
  * low probability for creature to get infected from a sick neighbor [P low]
recommended parameters that create at least three different waves were set as default.
- Collisions: movement in this Cell Automat is set in a way that all creatures move together and with a uniform probability. The model is built in a way that there will always be a single creature in a cell. Collisions are prevented from being made.

For execution, you may use the controller.exe file by clicking it. 
Download from: https://github.com/shirazbar/CA-assignment1

You can also run the program using the full code with the following commands:
>> pip install -r requirements.txt

>> python controller.py
