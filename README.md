# mpeg2repair_puppeteer
mpeg2repair automation

This code automates transport stream file error checking by mpeg2repair.
This source code makes for windows 10.

## Use
 1. Select directory. (optional : date option) (input UI path fields directly or by Text file.(path.txt))
 2. Input priority is UI input first. (If you do both option, Text file input is ignored.)
 3. If you have completed entering, Press Start Button. (or Keyboard F2 Button.) (You don't have to enter all of them. Please enter only as many as you want.)
 4. Whenever each file is completed scan. filename, duration and capacity are wrote in the result box.
 5. After total files have been scanned, mpeg2repair program is turned off. (It turns off independently for each task.)

### date option (optional)
caution : only use filename start with prefix "MMDD_". (input date string type)
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
 * please input mpeg2repair execute file path. (e.g. C:/mpeg2repair/mpeg2repair.exe)

### /path.txt
* write transport stream files folder path on each line of 'path.txt' file.
* separate by each line. (seperate by enter button. ("\n"))
  (e.g. : 
  C:/target/\n
  D:/target/\n
  E:/target/)
* maximum 3 lines possible, more input value be ignored.

## requirements
* PyQt5
* pywinauto
* pymediainfo
