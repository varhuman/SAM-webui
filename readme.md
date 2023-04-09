# Segment-Anything WebUI Demo

欢迎来到我为 [segment-anything](https://github.com/facebookresearch/segment-anything) 所做的一个简易可本地搭建的webui demo。

## 🚀 安装与设置

1. **创建本地虚拟环境并安装所需库：**

    - Windows：直接运行 `setup.bat`
    - macOS / Unix：
        ```bash
        chmod +x setup.sh
        ./setup.sh
        ```

2. **下载必要的模型文件（至少选择一个）：**

    - [sam_vit_h_4b8939.pth](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth)（推荐）
    - [sam_vit_l_0b3195.pth](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth)
    - [sam_vit_b_01ec64.pth](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth)

    > ⚠️ 注意：目前只测试过 `sam_vit_h_4b8939`。根据现状，`sam_vit_b_01ec64` 不能直接运行。

    下载好模型文件后，将其放入项目的 `models` 目录下。

3. 使用 VSCode 打开项目。已经设置好运行入口，直接按 F5 运行即可。

## 🎨 使用方法

![App Screenshot](assets/webui.png?raw=true)

- 左侧是默认图片，一只可爱的小猫 by stable diffusion。
- 你可以通过选择文件按钮导入自己的图片。
- 通过点击左侧图片上的点来选择我们需要裁剪出来的 mask，可以多点，识别率更高。

    ![App Screenshot](assets/clickpoints.png?raw=true)

    > 🔴 红点表示你选择的点。点击 "Clear Points" 可以清除所有点。

- 选择好你想要的点后，点击 "Process Points"。稍等片刻，即可生成你的 mask。

    ![App Screenshot](assets/result.png?raw=true)

- 如果这就是你想要的 mask，那么点击 "Download" 即可下载你的 mask。

    ![App Screenshot](assets/mask.png?raw=true)

## 📝 注意事项

- `app.py` 是本项目的入口。
- Python 使用 Flask，Web 前端使用 TypeScript + HTML + CSS。你所开发的所有 TypeScript 代码会在调试运行时自动转换为 JavaScript。
- 在 `tools` 文件夹中还有一个小工具 `get_all_masks.py`。它可以将 `tools/input` 目录下所有的图片（JPG、PNG）的所有 mask 提取出来并放入 `output` 文件夹中。
- 目前的 webui 界面还很简陋。如果你愿意，欢迎帮助完善它！

## 🌟 致谢

感谢 [Facebook Research](https://github.com/facebookresearch) 团队提供的 [segment-anything](https://github.com/facebookresearch/segment-anything) 项目作为本项目的基础。

## 🤝 贡献

如果你有任何建议或想为这个项目做出贡献，欢迎通过 [Issues](https://github.com/varhuman/SAM-webui/issues) 或 [Pull Requests](https://github.com/varhuman/SAM-webui/pulls) 与我联系。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可。

祝你编程愉快！
keep coding！

ps. this readme is imporve by chatgpt4 :)