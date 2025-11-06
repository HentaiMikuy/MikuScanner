# MikuScanner

<div align="center">

![MikuScanner Logo](./app/resource/images/logo.png)

**一个基于 PySide6 和 QFluentWidgets 开发的现代化网络扫描器**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Latest-green.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

</div>

## 📋 项目简介

MikuScanner 是一个功能强大的网络扫描工具，采用现代化的 Fluent Design 风格界面设计，支持多种网络扫描技术。项目采用模块化架构，提供友好的图形用户界面，主要用于网络发现、端口扫描和主机信息收集。

## ✨ 主要特性

### 🔍 多种扫描模式
- **TCP 连接扫描**：全连接扫描，兼容性好但速度较慢
- **TCP SYN 扫描**：半连接扫描，速度快且相对隐蔽
- **TCP ACK 扫描**：ACK 扫描，用于防火墙检测
- **Ping 扫描**：主机发现扫描，基础网络探测

### 🎯 核心功能
- 🖥️ **操作系统识别**：自动识别目标主机的操作系统类型
- 🔌 **端口扫描**：检测开放端口和对应服务
- 📊 **实时进度**：扫描过程中显示实时进度和状态
- 📄 **报告导出**：生成详细的 Word 格式扫描报告
- 🎨 **现代化界面**：基于 Fluent Design 的美观界面

### 🚀 技术亮点
- **多线程并发**：支持自定义线程数量，提高扫描效率
- **异步处理**：使用 Qt 信号槽机制，确保界面响应性
- **模块化设计**：清晰的代码结构，易于维护和扩展
- **跨平台支持**：基于 Qt 的跨平台 GUI 框架

## 📁 项目结构

```
MikuScanner/
├── MikuScanner.py                 # 主程序入口
├── LICENSE                        # 许可证文件
├── app/                           # 应用程序代码
│   ├── network/                   # 网络扫描模块
│   │   ├── HostInformation.py     # 主机信息获取
│   │   ├── PingScan.py           # Ping 扫描
│   │   ├── TcpAckScan.py         # TCP ACK 扫描
│   │   ├── TcpConnectScan.py     # TCP 连接扫描
│   │   └── TcpSynScan.py         # TCP SYN 扫描
│   ├── components/                # UI 组件模块
│   │   ├── link_card.py          # 链接卡片组件
│   │   ├── sample_card.py        # 样例卡片组件
│   │   ├── table_bar.py          # 标签页组件
│   │   ├── table_frame.py        # 表格组件
│   │   └── type_writer.py        # 打字机效果组件
│   ├── resource/                  # 资源文件
│   │   └── images/               # 图片资源
│   │       ├── app_logo.ico      # 应用图标
│   │       ├── header.png        # 主页头部图片
│   │       ├── header-host.png   # 主机信息页面头部
│   │       ├── header-scanner.png# 扫描页面头部
│   │       └── logo.png          # 主 Logo
│   └── view/                      # 界面视图模块
│       ├── home_interface.py     # 主页面界面
│       ├── hostInfo_interface.py # 主机信息界面
│       └── scanner_interface.py  # 扫描器界面
└── todo.md                        # 任务清单（开发用）
```

## 🛠️ 技术栈

| 技术/库 | 版本 | 用途 |
|---------|------|------|
| **Python** | 3.8+ | 主要编程语言 |
| **PySide6** | Latest | Qt for Python，GUI 框架 |
| **QFluentWidgets** | Latest | 现代化 UI 组件库 |
| **python-nmap** | Latest | nmap 扫描功能 |
| **Scapy** | Latest | 网络包处理和发送 |
| **python-docx** | Latest | Word 文档生成 |
| **concurrent.futures** | Built-in | 并发处理 |
| **ThreadPoolExecutor** | Built-in | 线程池管理 |

## 🚀 快速开始

### 环境要求
- Python 3.8 或更高版本
- nmap 工具
- 支持的网络环境

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd MikuScanner

# 安装 Python 依赖
pip install PySide6 QFluentWidgets python-nmap scapy python-docx

# 安装 nmap（Ubuntu/Debian）
sudo apt-get install nmap

# 安装 nmap（CentOS/RHEL）
sudo yum install nmap

# 安装 nmap（macOS）
brew install nmap

# 安装 nmap（Windows）
# 下载并安装 nmap for Windows
```

### 运行程序

```bash
python MikuScanner.py
```

## 📖 使用指南

### 第一步：启动扫描
1. 选择 **"Scanner"** 导航标签
2. 输入要扫描的 IP 地址或 IP 段（例如：`192.168.1.0/24`）
3. 选择扫描模式：
   - **TCP Connect**：全连接扫描，兼容性好
   - **TCP SYN**：半连接扫描，速度快
   - **TCP ACK**：ACK 扫描，防火墙检测
   - **Ping**：主机发现扫描
4. 对于 TCP Connect 扫描，可以设置端口号和线程数
5. 点击 **"Start Scanning"** 开始扫描

### 第二步：查看结果
1. 扫描完成后，选择 **"Host Information"** 导航标签
2. 从下拉列表中选择要分析的主机 IP
3. 点击 **"Get it!"** 获取详细的主机信息

### 第三步：导出报告
1. 在主机信息页面点击 **"Report export"** 按钮
2. 系统会自动生成 Word 格式的扫描报告
3. 报告文件保存在程序运行目录中

## 🔧 配置选项

### 扫描参数
- **IP 地址格式**：
  - 单个 IP：`192.168.1.1`
  - CIDR 格式：`192.168.1.0/24`
  - IP 范围：`192.168.1.1-192.168.1.254`
  - 多 IP：`192.168.1.1,192.168.1.2`

- **端口设置**：
  - 单个端口：`80`
  - 端口范围：`1-1000`
  - 多个端口：`21,22,80,443`

- **线程数**：1-10000（推荐 10-50）

## 🏗️ 架构设计

### 模块架构
- **主窗口模块**：应用入口和导航管理
- **网络扫描模块**：各种扫描算法的实现
- **UI 组件模块**：可复用的界面组件
- **界面视图模块**：三个主要的功能界面
- **资源模块**：图片和样式资源

### 设计模式
- **工厂模式**：不同扫描类型对象的创建
- **观察者模式**：Qt 信号槽机制
- **单例模式**：资源管理
- **策略模式**：不同扫描算法的切换

## ⚠️ 注意事项

### 安全提醒
- 本工具仅用于授权的网络安全测试
- 使用前请确保有相应的网络操作权限
- 遵守当地法律法规和道德准则

### 性能考虑
- TCP Connect 扫描速度较慢，不建议在大网段使用
- 建议合理设置线程数，避免对网络造成过大压力
- 在生产环境中使用前请先在测试环境验证

### 兼容性
- 支持 Windows、macOS、Linux 系统
- 需要管理员权限进行某些高级扫描
- 部分扫描功能可能受防火墙影响

## 🐛 故障排除

### 常见问题

**Q: 扫描没有结果？**
A: 检查 IP 地址格式是否正确，确认网络连接正常

**Q: 某些端口扫描失败？**  
A: 可能被防火墙拦截或目标主机禁用了相关服务

**Q: 程序运行缓慢？**
A: 减少线程数量或缩小扫描范围

**Q: 导出报告失败？**
A: 检查是否有文件写入权限，确保目标目录可写

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](./LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目！

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 创建 GitHub Issue
- 发送邮件至项目维护者

## 🗺️ 路线图

- [ ] 增强扫描算法
- [ ] 添加更多报告格式
- [ ] 支持 Web 界面
- [ ] 添加批量扫描功能
- [ ] 集成威胁情报数据库
- [ ] 开发移动端应用

---

**MikuScanner** - 让网络扫描变得更加简单和优雅！ ✨
