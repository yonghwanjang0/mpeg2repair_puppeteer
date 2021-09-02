# mpeg2repair_puppeteer
mpeg2repair automation

This code automates transport stream file error checking by mpeg2repair.
This source code makes for windows 10.

## use
 1. Select the directory contain stream files. (optional : date option) (input the UI path fields directly or by Text file.(use path.txt))
 2. Input priority is UI input first. (If you do both option, Text file input is ignored.)
 3. If you have completed entering, Press the Start Button. (or Keyboard F2 Button.) (You don't have to enter all of them. Please enter only as many as you want.)
 4. Whenever each file is completed scan. filename, duration and capacity are wrote in the result box.
 5. After total files have been scanned, mpeg2repair program is turned off. (It turns off independently for each task.)
 6. While working, the start button does not work. (for blocking the duplicate work.)
 7. When all tasks are finished, the next task can be executed. (The address value of the previous work will be deleted, must re-enter the stream files folder paths.) 

### date option (optional)
caution : only use filename start with prefix "MMDD_". (month-day string type)
(e.g. : '0528_filename.ts')

1. use /path.txt
   * input "folder|option" (e.g. : C:/folder/|1204)
     * From ~ : "start date-" (e.g. : C:/folder/|0525-)
     * ~ To : "-end date" (e.g. : C:/folder/|-0528)
     * From ~ To : "start date-end date" (e.g. : C:/folder/|0525-0528)
     * Only One Day : "date" (e.g. : C:/folder/|0528)

2. use UI Input
   * Same as the above usage. but you only have to enter 'date option' in the option field box.

## Use Settings
### /exe_path.txt
 * Input the mpeg2repair execute file path. (e.g. C:/mpeg2repair/mpeg2repair.exe)

### /path.txt
* write the transport stream files folder path on each line of 'path.txt' file.
* Input paths are separated by each line. (seperate by enter button. ("\n"))
  (e.g. : 
  C:/target/\n
  D:/target/\n
  E:/target/)
* maximum 3 lines wrote possible(3 paths), and more input value be ignored.

## requirements
* PyQt5
* pywinauto
* pymediainfo
