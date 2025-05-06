import os
import shutil
import argparse
import logging
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """自定义日志格式（无时间戳）"""
    def format(self, record):
        return record.getMessage()

def setup_logging():
    """配置日志记录系统"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"/app/logs/copy_log_{timestamp}.log"
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 文件处理器（只记录纯消息）
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(CustomFormatter())
    
    # 控制台处理器（带颜色）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return log_filename

def copy_directory(src, dst):
    """复制文件夹内容并跳过同名文件"""
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    cnt_copied = 0
    cnt_skipped = 0

    if dst.startswith(src + os.sep) or src == dst:
        logging.error("目标目录不能位于源目录内或与源目录相同")
        return False

    try:
        for root, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root, src)
            dst_path = os.path.join(dst, rel_path)
            
            # 创建目标目录（如果不存在）
            os.makedirs(dst_path, exist_ok=True)
            
            # 复制文件
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_path, file)
                
                if not os.path.exists(dst_file):
                    shutil.copy2(src_file, dst_file)
                    logging.info(f"已复制: {src_file} -> {dst_file}")
                    cnt_copied += 1
                else:
                    logging.warning(f"跳过已存在文件: {dst_file}")
                    cnt_skipped += 1
        logging.info(f"复制完成: {cnt_copied} 个文件已复制, {cnt_skipped} 个文件已跳过")
        return True
    except Exception as e:
        logging.error(f"复制过程中发生错误: {str(e)}", exc_info=True)
        return False

class ArgumentParser(argparse.ArgumentParser):
    """自定义参数解析器（记录错误到日志）"""
    def error(self, message):
        logging.error(f"参数错误: {message}")
        self.exit(2, f"\n错误: {message}\n")

if __name__ == "__main__":
    log_file = setup_logging()
    logging.info(f"日志文件: {os.path.abspath(log_file)}")
    
    parser = ArgumentParser(
        description="文件夹复制工具 - 版本 2.0",
        epilog="示例: python3 copy_dir.py /source /destination")
    parser.add_argument("source", help="源目录路径")
    parser.add_argument("destination", help="目标目录路径")
    
    try:
        args = parser.parse_args()
        logging.info(f"从 ${args.source}到 ${args.destination}复制开始")
        if copy_directory(args.source, args.destination):
            logging.info("操作成功完成！")
        else:
            logging.error("操作未完成，请检查错误信息。")
    except Exception as e:
        logging.error(f"发生未捕获的异常: {str(e)}", exc_info=True)