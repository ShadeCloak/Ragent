import logging
import time

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def tool_api(func):
    """
    一个装饰器，用来标记某个方法为工具的API接口，可能包含日志记录、参数验证等功能。
    :param func: 被装饰的方法
    :return: 包装后的方法
    """
    def wrapper(*args, **kwargs):
        # 记录调用信息
        logging.info(f"调用方法: {func.__name__}，参数: {args}, {kwargs}")
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            # 执行原始方法
            result = func(*args, **kwargs)
        except Exception as e:
            # 记录异常信息
            logging.error(f"方法 {func.__name__} 执行失败: {str(e)}")
            result = None
        
        # 记录方法执行时间
        elapsed_time = time.time() - start_time
        logging.info(f"方法 {func.__name__} 执行时间: {elapsed_time:.4f}秒")
        
        return result

    # 为方法添加标记
    wrapper.is_tool_api = True  # 标记这个方法为 tool API
    wrapper.__doc__ = func.__doc__
    return wrapper
