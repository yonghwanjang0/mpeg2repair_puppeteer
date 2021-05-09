# mpeg2repair_puppeteer

mpeg2repair automation

This code automates ts file error checking by mpeg2repair.

This source code makes for windows 10.

## Use
 1. Select directory. (input UI path fields directly or by Text file.(path.txt))
 2. Input priority is UI input first. (If you do both option, Text file input is ignored.)
 3. If you have completed entering, Press Start Button (or F2 Button) (You don't have to enter all of them. Please enter only as many as you want.)

## Use Settings
### /exe_path.txt
 * please input mpeg2repair execute file path. (ex. C:/mpeg2repair/mpeg2repair.exe)

### /path.txt
* write transport stream files folder path on each line of file.
* separate by each line. 
  (ex.
  C:/target/\n
  D:/target/\n
  E:/target/)
* maximum 3 lines possible, more input value be ignored.

## requirements
* PyQt5
* pywinauto
* pymediainfo
