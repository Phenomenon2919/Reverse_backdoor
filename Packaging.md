# Packaging

Package you malwares as a single file executable with no console launching feature to hide the existence of malware in the target computer after deployment. This executable can be formed in *Windows* or *Linux* through the following ways. 

## Packaging python malwares into executables using Pyinstaller for Windows

### Using Windows OS to package the executable

* Install Pyinstaller in Windows;

> python.exe -m pip install pyinstaller 

* Use the Pyinstaller to create executable (.exe) of the malware

> pyinstaller.exe *<python malware code\>* --onefile --noconsole

### Using a Linux machine to create a Windows execuatble

* Download pythonX.XX.msi intepreter for windows from official site. *(X is a digit for the version to use)*
* Use **wine** to install the interpreter

> wine msiexec /i python-X.XX.XX.msi

* Go to directory of installed python executable; then

> wine python.exe -m pip install pyinstaller

* Install all the libraries that are required by your script if any

> wine python.exe -m pip install *<package name\>*

or

> wine python.exe -m pip install -r Requirements.txt

* Go to directory of installed pyinstaller;

* For a general executable;

> wine pyinstaller.exe --onefile --noconsole *<path_of_main_program\>*

* To add a **legitimate front file** to the executable

> wine pyinstaller.exe --onefile --noconsole --add-data *"<path_of_legitimate_file\>:."* *<path_of_main_program\>*

## Executable Compression using UPX

To compress your malware executable which may help avoid detection my antivirus softwares, we can use UPX

* Download latest version of UPX from https://github.com/upx/upx/releases and extract it
* Use binary for compression;

> ./upx *<path_of_backdoor_execuatable\>* -o *<new_compressed_executable_name\>*

## Adding an ICON to the malware executable

* Pick an ICON from https://www.iconfinder.com/ and download it
* Convert the .png file into .ico file. (You can use https://www.easyicon.net/language.en/covert/ )
* Use wine command to create executable with icon;

> wine pyinstaller.exe --onefile --noconsole --add-data *"<path_of_legitimate_file\>:."* --icon *<path_of_the_ICO_file\>* *<path_of_main_program\>*

## Spoofing the extension of the malware extension

* Use the **Right-to-left Override (U+202E)** character in the executable name. It can be found in *Characters* application in Linux.
* If it is not available, use https://r12a.github.io/app-conversion/ or similar converters to convert the hex code (U+202E) to the character and copy it from the same.
* Example: If the cover file is a .png image(let say of a bike; so your malware is named bike.exe); Rename it to something like bikegnp.exe and Add the Right-to-left Override before *gnp.exe* part. The file will seem renamed from *bikegnp.exe* to *bikeexe.png*.
* Read more about Right-to-left Override character and its usage from https://krebsonsecurity.com/tag/right-to-left-override/

## Packaging python malwares into executables using Pyinstaller for OS X

It is better to create an executable for OS X in an OS X operating system. 

* Python comes preinstalled in OS X, but the pip is slighly broken. To fix the packages, download *get-pip.py* from official site https://bootstrap.pypa.io. Run it as;

> sudo python get-pip.py

* Install pyinstaller;

> sudo pip install pyinstaller

The rest process is very similar to creating a Windows Executable with certain differences.
* Download the .ICNS format of ICON instead of .ICO, since it better readable in OS X
* Create OS X executable using;

> pyinstaller --onefile --noconsole --icon *<path_of_icns_file\>* --add-data *"<path_of_legitimate_file\>:."* *<path_of_main_program\>*

Note: In OS X file extension is not really important, so that addition is optional

## Packaging python malwares into executables for Linux
This process of packaging is very similar to that of Windows and OS X. However, it is important to know that in linux, if the malware executable is double clicked, there is a chance, Linux machine will prompt with a message **Could not display <malware_execuatble_name\>**. And when the victim explores options to open the file, he/she may get suspicious. Hence, try to embed the malicious code with another executable front file, that victim voluntarily chooses to execute on their system, causing the malware to executed simultaneously.