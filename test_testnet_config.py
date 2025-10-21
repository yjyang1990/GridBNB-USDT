#!/usr/bin/env python3
"""
测试币安测试网配置的脚本
"""

import os
import sys
import asyncio
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.settings import settings
from src.core.exchange_client import ExchangeClient

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_testnet_config():
    """测试测试网配置"""
    logger.info("=" * 50)
    logger.info("测试币安测试网配置")
    logger.info("=" * 50)
    
    # 显示当前配置
    logger.info(f"USE_TESTNET: {settings.USE_TESTNET}")
    logger.info(f"API Key 前8位: {settings.BINANCE_API_KEY[:8]}..." if settings.BINANCE_API_KEY else "API Key: 未设置")
    logger.info(f"API Secret 前8位: {settings.BINANCE_API_SECRET[:8]}..." if settings.BINANCE_API_SECRET else "API Secret: 未设置")
    
    # 验证沙盒模式状态
    if settings.USE_TESTNET:
        logger.info("🔧 配置为使用币安测试网（沙盒模式）")
    else:
        logger.info("🌐 配置为使用币安主网")
    
    if not settings.BINANCE_API_KEY or not settings.BINANCE_API_SECRET:
        logger.error("❌ API密钥未设置，请在.env文件中配置BINANCE_API_KEY和BINANCE_API_SECRET")
        return False
    
    try:
        # 创建交易所客户端
        client = ExchangeClient()
        
        # 测试连接（添加超时控制）
        logger.info("正在测试连接...")
        try:
            # 使用asyncio.wait_for设置超时
            await asyncio.wait_for(client.load_markets(), timeout=30.0)
            logger.info("✅ 市场数据加载成功")
        except asyncio.TimeoutError:
            logger.error("❌ 连接超时（30秒），可能是网络问题")
            logger.error("建议检查：")
            logger.error("1. 网络连接是否正常")
            logger.error("2. 是否使用了代理")
            logger.error("3. 防火墙设置")
            await client.close()
            return False
        
        # 获取服务器时间
        server_time = await client.exchange.fetch_time()
        logger.info(f"✅ 连接成功！服务器时间: {server_time}")
        
        # 测试获取余额（如果有权限）
        try:
            balance = await client.fetch_balance()
            logger.info("✅ 余额获取成功")
        except Exception as e:
            logger.warning(f"⚠️ 余额获取失败（可能是权限问题）: {e}")
        
        # 关闭连接
        await client.close()
        
        logger.info("=" * 50)
        if settings.USE_TESTNET:
            logger.info("🎉 测试网配置验证成功！")
            logger.info("💡 提示：您正在使用币安测试网，所有交易都是模拟的")
        else:
            logger.info("🎉 主网配置验证成功！")
            logger.info("⚠️ 警告：您正在使用币安主网，请谨慎操作")
        logger.info("=" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 连接失败: {e}")
        logger.error("请检查：")
        logger.error("1. API密钥是否正确")
        logger.error("2. 网络连接是否正常")
        logger.error("3. 如果使用测试网，请确保API密钥是测试网的")
        return False

def show_usage():
    """显示使用说明"""
    print("""
币安测试网配置使用说明：

1. 创建测试网API密钥：
   - 访问：https://testnet.binance.vision/
   - 使用GitHub账户登录
   - 生成HMAC_SHA256密钥

2. 配置环境变量：
   在.env文件中设置：
   USE_TESTNET=True
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_secret

3. 运行测试：
   python test_testnet_config.py

4. 切换回主网：
   在.env文件中设置：
   USE_TESTNET=False
   BINANCE_API_KEY=your_mainnet_api_key
   BINANCE_API_SECRET=your_mainnet_secret
""")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        show_usage()
    else:
        asyncio.run(test_testnet_config())
