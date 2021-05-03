# mpeg2repair_puppeteer

mpeg2repair automation

This source code makes for windows 10.

/exe_path.txt
 * please input mpeg2repair execute file path. (ex. C:/mpeg2repair/mpeg2repair.exe)

/path.txt
* write transport stream files folder path on each line of file.
* separate by each line. 
  (ex.
  C:/target/\n
  D:/target/\n
  E:/target/)
* maximum 3 lines possible, more input value be ignored.

requirement

* PyQt5
* pywinauto
* pymediainfo
