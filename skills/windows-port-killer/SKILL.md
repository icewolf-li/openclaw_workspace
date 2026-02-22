# Windows 端口占用解决技能

## 概述
本技能用于快速诊断和解决 Windows 系统中的端口占用问题，包括普通进程占用和 Hyper-V 动态端口保留两种情况。

## 使用场景
- 当你尝试启动服务时遇到 "端口已被占用" 错误
- 需要释放特定端口供应用程序使用
- Hyper-V 保留了你需要的端口

## 技能命令

### 1. 查找占用端口的进程
```bash
netstat -ano | findstr "<端口号>"
```

### 2. 终止占用端口的进程
```bash
taskkill /t /f /pid <进程ID>
```

### 3. 检查动态端口范围
```bash
netsh int ipv4 show dynamicport tcp
```

### 4. 检查被排除的端口范围
```bash
netsh interface ipv4 show excludedportrange protocol=tcp
```

### 5. 解决方案一：重置动态端口范围
以管理员身份运行 PowerShell：
```powershell
netsh int ipv4 set dynamicport tcp start=49152 num=16384
```
然后重启电脑。

### 6. 解决方案二：保留特定端口给应用程序
以管理员身份运行 PowerShell：
```powershell
# 保留单个端口
netsh int ipv4 add excludedportrange protocol=tcp startport=<端口号> numberofports=1

# 保留端口范围
netsh int ipv4 add excludedportrange protocol=tcp startport=<起始端口> numberofports=<端口数量>
```
然后重启电脑。

### 7. 取消端口保留
```powershell
netsh int ipv4 delete excludedportrange protocol=tcp startport=<端口号> numberofports=1
```

## 注意事项
- 所有 `netsh` 命令需要管理员权限
- 修改端口设置后必须重启电脑才能生效
- 终止进程前请确认该进程可以安全关闭
- Hyper-V 保留的端口通常在 1024-5000 范围内

## 故障排除
如果上述方法无效，请检查：
1. 是否有其他虚拟化软件（如 Docker、WSL2）占用了端口
2. 防火墙设置是否阻止了端口访问
3. 应用程序是否配置了正确的绑定地址

## 参考来源
- [解决端口占用，hyper-v占用动态端口](https://nodaoli.top/posts/%E8%A7%A3%E5%86%B3%E7%AB%AF%E5%8F%A3%E5%8D%A0%E7%94%A8.html)