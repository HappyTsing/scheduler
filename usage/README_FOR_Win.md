# 关机（未测试）

实现电脑关机，自动定时开启执行脚本。

## step 0: 关闭windows通知

软件需要管理员权限，每次都要点确定给予权限太烦了，建议关掉！

参考：http://news.558idc.com/408276.html

## step 1: 配置Windows自动登录

win + r，输入 regedit，回车。

依次点击：HKEY_LOCAL_MACHINE -> SOFTWARE -> Microsoft -> Windows NT -> CurrentVersion

右键修改或新建（字符串类型），并输入对应值：

- DefaultUsername：查询 `C:\Users` 下文件夹的名字即为用户名
- DefaultPassword：密码，若为微软账号登录，其密码就是账号密码。不要输入PID
- AutoAdminLogon：设置值为 1

重启，即可实现自动登录

## step 2: 配置Windows自动开机

需要进入bios修改，但屏幕坏了暂时无法测试。

## step 3: 配置Windows执行定时脚本

打开文件夹，找到 `此电脑`，右键点击 `管理`。

点击 `任务计划程序`，右侧 `创建基本任务`，输入名称、设置定时触发器，操作为启动程序，输入 `main_boxed.py` 的全路径即可。

设置条件：选中唤醒计算机运行此任务。

此时，只需要 `Alt + F4` ，对计算机睡眠即可，时间到时，会自动唤醒，并执行该脚本，进行一件日常。

> 注意：不要使用鼠标点击 win 图标的方式进行睡眠，可能会有问题？懒得测试了。

# 睡眠（已测试）

实现电脑睡眠，自动定时唤醒执行脚本

仅配置关机中的 step 3 即可。

