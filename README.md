# Traffic

This is a rewrite of a very old `Trafic.exe` app used by students to, well, calculate traffic.  
This one does basically the same thing, except it works correctly on modern software.

## Installation

Make sure that [Python](https://www.python.org/downloads/) is installed and is available in your PATH.  
To check this, try running `python3` in your command prompt

1. Download this project as zip and unpack it somewhere.
2. Run `install_windows.bat` if you are using Windows 7 or above. 
For macOS and GNU/Linux, run `install_linux_macos.sh` instead.
3. Check for errors. If there are none, installation succeeded.

If installation is successful, `launcher.bat` (on Windows) or `launcher.sh` (on macOS and GNU/Linux) should appear.
Use it to start the app.

## Notes for Windows 7

Installing PyQt5 on 7 is a bit harder.
You need to download this 
[wheel](https://files.pythonhosted.org/packages/f0/3a/8f2261c0477008057636b9f992952033748b9ee94541dd54373f7d6bf5f1/PyQt5-5.8-5.8.0-cp34.cp35.cp36.cp37-none-win32.whl) 
and put it in project folder. Now, open terminal, navigate to project folder and do this:
```shell
venv\Scripts\activate.bat
pip install PyQt5-5.8-5.8.0-cp34.cp35.cp36.cp37-none-win32.whl
pip install sip==4.19.7
```
Then run the installation script to create `launcher.bat`.

## For other OSes

If your OS can't install the requirements but can run 
<b> Python 2 or later</b>, you can use the console version.  
It doesn't need venv or anything, just double-click `main_cli.py` if you have Python 3 or `main_cli_py2.py` if Python 2.