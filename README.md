# 自定义定时任务

通过图像识别，可自定义定时任务，只需要在 `img` 中添加自己的任务文件夹，并放置需要的图片，随后在 `config.yaml`，中配置识别流程，即可轻松自定义定时任务！

目前支持的操作如下：

```yaml
  - {
    name: 示例,
    name_en: example,
    enable: off,
    parent_phase: daily_activity,
    schedule: 12:12:12,
    phases: [
      {id: -1, name: 等待 n 秒, action: wait, duration: n},
      {id: 1, name: 移动鼠标, action: move},
      {id: 1, name: 点击 n 次, action: click, times: n},
      {id: 1, name: 双击, action: doubleClick},
      {id: -1, name: 键盘按键 n 次, action: press, key: down（任意按键）, times: n},
      {id: 1, name: 检查，等待几秒查看是否识别，检查失败不退出, action: check},
      {id: 1, name: 严格检查，检查失败会退出, action: check, action: strict},
      {id: 1, name: 等待至成功识别, action: finish},
    ]
  }
```
其中 `id` 为图像名称，例如 `1.png`，更多细节请查看 `config.yaml`。

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
pyinstaller -D main.py
# Enigma Virtual Box  再次压缩
```
