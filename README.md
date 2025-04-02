This repository contains a commented python code for the OSPREY smart worksheet. 
The code is designed to function with minimal user editing. 
A triple hash (###) indicates a region of code where the user can change certain features, such as a question to be asked or a given answer.
Searching for ### is therefore the quickest way to edit the smart worksheet.
A sample lab script is also provided to support the practical session. 
Note, all image files contained in this repo are needed to be stored in the same folder as the code in order to the worksheet to correctly run. 
The code can be compiled as an executable (.exe) file by running the following pyinstaller code:


pyinstaller --onefile --windowed --noconsole --icon=icon_whole.ico --add-data "Faraday.png;." --add-data "Qit.png;." --add-data "Randles.png;." --add-data "soton_logo.png;." --add-data "logo_small.png;." --add-data "icon.ico;." --add-data "icon_whole.ico;." OSPREY.py
