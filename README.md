# Installation

First clone the repo :
```
git clone https://github.com/YungBricoCoop/SPDV
```
And then install the dependencies
```bash
 cd ./SPDV
 pip install -r requirements.txt
```

# Run
Before running the script you just need to put your personal spotify history files inside the **streamingHistory** folder of the project, the name of thoses files starts with **StreamingHistory** and ends with a number like this : **StreamingHistory4**

To to get the desired result you just have to use this two commands in this order :
```bash
python main.py -db
python main.py -render
```
The result file (named **output.html**) will be generate in the output folder(named **output**) of the project if everything went well

## Parameters

|                |Parameters                                                  
|----------------|-------------------------------|
|Get some help with the commands |`-help`            |           
|Load spotify history data inside database         |`-db`            |          
|Generate a pretty html file for visualizing your data|`-render`|

# Result

The exported file should look like this (**output.html**) : 
![text](https://i.ibb.co/GkqrvQy/Capture.png "")

