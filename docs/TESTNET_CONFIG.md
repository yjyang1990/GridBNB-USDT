# 币安测试网配置指南

## 概述

本项目已支持币安测试网，您可以在测试环境中安全地调试和测试交易策略，而无需使用真实资金。

## 配置步骤

### 1. 获取测试网API密钥

1. 访问币安现货测试网：https://testnet.binance.vision/
2. 使用GitHub账户登录
3. 生成HMAC_SHA256密钥
4. **重要**：密钥仅显示一次，请妥善保管

### 2. 配置环境变量

在项目根目录创建 `.env` 文件，添加以下配置：

```bash
# 测试网配置
USE_TESTNET=True

# 测试网API密钥
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_here

# 其他配置...
SYMBOLS=BNB/USDT
MIN_TRADE_AMOUNT=20.0
INITIAL_PRINCIPAL=1000.0
```

### 3. 验证配置

运行测试脚本验证配置：

```bash
python test_testnet_config.py
```

如果配置正确，您将看到：
- ✅ 连接成功
- 🔧 使用币安测试网进行调试

## 切换环境

### 切换到测试网
```bash
# 在.env文件中设置
USE_TESTNET=True
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret
```

### 切换到主网
```bash
# 在.env文件中设置
USE_TESTNET=False
BINANCE_API_KEY=your_mainnet_api_key
BINANCE_API_SECRET=your_mainnet_secret
```

## 技术实现

### 配置位置

测试网配置在以下文件中实现：

1. **`src/config/settings.py`**：
   ```python
   USE_TESTNET: bool = False  # 是否使用币安测试网
   ```

2. **`src/core/exchange_client.py`**：
   ```python
   # 初始化交易所实例
   self.exchange = ccxt.binance({...})
   
   # 根据配置启用沙盒模式（测试网）
   if settings.USE_TESTNET:
       self.exchange.set_sandbox_mode(True)
   ```

**重要说明**：根据 [CCXT 官方文档](https://docs.ccxt.com/#/README?id=authentication)，币安测试网的正确配置方式是使用 `set_sandbox_mode(True)` 方法，而不是在 `options` 中设置 `testnet`。

### 日志输出

系统会在启动时显示当前使用的环境：
- 🔧 使用币安测试网进行调试
- 🌐 使用币安主网

## 注意事项

1. **API密钥独立**：测试网和主网的API密钥是独立的，需要分别创建
2. **数据隔离**：测试网的数据与主网完全隔离
3. **功能限制**：某些高级功能可能在测试网中不可用
4. **资金安全**：测试网使用虚拟资金，不会影响真实资产

## 故障排除

### 常见问题

1. **连接失败**
   - 检查API密钥是否正确
   - 确认网络连接正常
   - 验证是否使用了正确的测试网API密钥

2. **权限错误**
   - 确认API密钥具有相应权限
   - 检查IP白名单设置

3. **配置不生效**
   - 确认.env文件在项目根目录
   - 重启应用程序
   - 检查环境变量名称是否正确

### 调试步骤

1. 运行测试脚本：`python test_testnet_config.py`
2. 查看日志输出
3. 检查网络连接
4. 验证API密钥格式

## 相关链接

- [币安现货测试网](https://testnet.binance.vision/)
- [币安API文档](https://developers.binance.com/)
- [CCXT文档](https://docs.ccxt.com/)
