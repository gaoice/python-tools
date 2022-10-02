# 使用说明

**配置文件**

`[DEFAULT]`

`cam_num = 0` 				启用的摄像头编号，例如笔记本自带的摄像头为 0

`tolerance = 0.4` 			值越小，人脸识别越严格

`recognition_times = 10` 	识别总次数

`min_right_times = 8` 		最少识别正确的次数，否则触发邮件

`send_mail = true` 			邮件被触发后是否发送

`[DEBUG]`

`debug = true` 				是否打开调试，第一次使用打开调试查看效果

`debug_send_mail = false` 	是否调试发送邮件

`[EMAIL]`

`from_addr = test@163.com`		发件箱账户。

`password = test`				发件箱授权码。

`smtp_server = smtp.163.com`	发件箱smtp服务地址。

`to_addr = test@qq.com`			收件箱地址。



**使用**

需要两个邮箱，一个作为发件箱，一个作为收件箱。发件箱使用前需要前往自己的邮箱设置。

需要将自己的图片命名为 `me.jpg` 。

