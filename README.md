# Python 小工具集合



### FaceCheck

基于 [face_recognition](https://github.com/ageitgey/face_recognition) 的人脸检测，检测到陌生人发邮件通知，可以通过脚本设置为开机启动或者定时启动，增强电脑安全性。

更多见 [使用说明](https://github.com/gaoice/python-tools/blob/master/FaceCheck/README.md) 。



### ClipboardSync 

局域网Windows系统剪切板同步工具。

通过在配置文件中指定数据库地址和要使用的表名，软件会自动创建一张表，用来同步剪切板。

需要注意的是，在一个同步周期内，软件将会优先将本机的剪切板更改上传到数据库，在本机剪切板没有被更改的情况下才会同步远程（数据库）的剪切板内容到本机。



### ClipboardFormat

Windows系统剪切板格式化工具。

通过系统钩子监听 `Ctrl + C` ，对剪切板内容进行正则提取，将匹配到的group进行合并，并且可以在剪切板前后追加指定内容。

示例1：

`pattern = ^([\s\S]*)---------------------[\s\S]*转载请附上博文链接！$` 

对csdn的复制内容进行提取，裁剪掉了强制的小尾巴。

示例2：

`pattern = ^([\s\S]*)`

`append_bottom = \n我的小尾巴`

可以在匹配到的内容后面添加自己的小尾巴。
