# 自定义定时任务

通过图像识别，可自定义定时任务，只需要在 `img` 中添加自己的任务文件夹，并放置需要的图片，随后在 `config.json`，中配置识别流程，即可轻松自定义定时任务！

目前支持的操作如下：

```json
{
  "task_name": {
    "schedule": false,
    "phases": [
      {"comment": "等待 2 秒","action": "wait","duration": 2},
      {"comment": "热键", "action": "hotkey","keys": ["winleft", "d"]},
      {"comment": "单击", "img_id": 1, "action": "click","times":2},
      {"comment": "双击", "img_id": 1,"action": "doubleClick","times":2},
      {"comment": "等待完成", "img_id": 2,"action": "finish"},
      {"comment": "插槽", "action": "slot","handler": "seer_login"},
      {"comment": "循环", "img_id": 4,"action": "loop","index": "index_1","times":2}
      {"comment": "打开 exe", "action": "open","path": "/path/to/file_name_reg.*.exe"}
    ],
    "loops": {
      "index_1": [
          //循环体的 phases
      ]
    }
  }
}

```
## Quick start

若想运行源代码版本，可进行如下操作：

```sh
# python 3.8.10

# pytorch https://pytorch.org/get-started/locally/

python -m virtualenv venv

pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

python3 main.py
```

> 建议直接使用打包好的 release 版本，双击 `exe` 文件即可运行。

## Package

若想自行打包，可进行如下操作：

```sh
# 打包单个 exe 文件
pyinstaller -F main.py
```

上述方式打包后运行较慢，建议采用 `-D` 打包多文件，再使用 [Enigma Virtual Box](https://enigmaprotector.com/en/downloads.html) 将其压缩为可执行文件。

```sh
# 1. pyinstaller
pyinstaller -D main.py

# 2. Enigma Virtual Box  再次压缩
# Enter Input File Name
dist\main\main.exe

# Drag files and folders to the Virtual Box Files tree
add folder recursive -> dist\main

# Process
```

# update

1. 后续计划新增 `或` 语法：

```json
{
  "task_name": {
    "schedule": false,
    "phases": [
      {"comment":"或", "img_ids": [1,2],"action": "click/doubleClick/move/finish","index": "index_1","times":2}
    ],
  }
}
```
2. 错误处理

新开一个进程，配置文件如下：

```json
{
  "task_name": {
    "schedule": false,
    "phases": [],
    "errors":[],  // 语法和 phases 相同，例如识图时发现 flash 崩溃如何处理之类的
    "loops":{}
  }
}

```

3. 允许配置多任务

配置文件已经支持，需要修改main.py，暂定使用多线程。

- 同时执行多个任务
- 还是修改为依次执行？
- 或者修改为启动时让用户选择本次执行哪一个任务？