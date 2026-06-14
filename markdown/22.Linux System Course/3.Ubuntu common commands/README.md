# 3.Ubuntu common commands
### 3.1、Add
New create file


New create folder


![](3.Ubuntu-common-commands.pdf-0-1.jpeg)


Copy


### 3.2、Delete
|-i|To execute interactively|
|---|---|
|-f|Forced deletion, ignoring non-existent files without prompting|
|-r|Recursively delete the contents of a directory|


### 3.3、Modify
move、re-name


chmod changes file permissions


Permission settings

|Symbol|Meaning|
|---|---|
|+|Add permissions|
|-|Revoke permission|
|=|Set permissions|


rwx


|Letter<br>permissions|Meaning|
|---|---|
|r|read means read permission. For a directory, if there is no r permission, it<br>means that the contents of this directory cannot be viewed through ls.|
|w|write means write permission. For a directory, if there is no w permission, it<br>means that new files cannot be created in the directory.|
|x|execute means executable permission. For a directory, if there is no x<br>permission, it means that the directory cannot be entered through cd.|


Add a shortcut to all permissions


Set root password


Set user password


### 3.4、View
View system version


![](3.Ubuntu-common-commands.pdf-1-4.jpeg)


View hardware information


View file information


![](3.Ubuntu-common-commands.pdf-1-5.jpeg)
![](3.Ubuntu-common-commands.pdf-2-0.jpeg)


tree installation command


Find files


![](3.Ubuntu-common-commands.pdf-2-2.jpeg)


### 3.5、Other
tar command


tar usage format: tar [parameter] package file name file


![](3.Ubuntu-common-commands.pdf-2-3.jpeg)


Pack


![](3.Ubuntu-common-commands.pdf-2-4.jpeg)


Unpack


![](3.Ubuntu-common-commands.pdf-2-5.jpeg)


zip、unzip command


Compressed file: zip [-r] target file (no extension) source file


Unzip the file: unzip -d directory file after decompression compressed file


ln command


Soft link: Soft link does not occupy disk space. If the source file is deleted, the soft link will become

invalid. Commonly used, you can create files or folders


Hard links: Hard links can only link ordinary files, not directories. Even if the source file is deleted,

the linked file still exists


scp remote copy


![](3.Ubuntu-common-commands.pdf-3-3.jpeg)


wget file download


Search for an image address on Baidu as an example.


![](3.Ubuntu-common-commands.pdf-3-4.jpeg)


Other


![](3.Ubuntu-common-commands.pdf-3-5.jpeg)
