import os
import tkinter as tk
from tkinter import filedialog
import pathspec

def get_gitignore_spec(folder_path):
    gitignore_path = os.path.join(folder_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f.readlines())
            return spec
    return None

def convert_line_endings(folder_path):
    # 获取 .gitignore 规则
    gitignore_spec = get_gitignore_spec(folder_path)
    
    # 统计数据
    stats = {
        'total': 0,        # 未被跳过的文件总数
        'converted': 0,    # 成功转换的文件数
        'failed': 0,       # 转换失败的文件数
        'no_need': 0      # 无需转换的文件数
    }
    
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        # 跳过 .git 目录
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            file_path = os.path.join(root, file)
            
            # 计算相对路径用于 gitignore 匹配
            rel_path = os.path.relpath(file_path, folder_path)
            
            # 如果文件被 .gitignore 排除，则跳过
            if gitignore_spec and gitignore_spec.match_file(rel_path):
                continue
                
            stats['total'] += 1
            try:
                # 以二进制模式读取文件
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # 检查是否需要转换
                new_content = content.replace(b'\n', b'\r\n').replace(b'\r\r\n', b'\r\n')
                if new_content == content:
                    stats['no_need'] += 1
                    print(f'无需转换: {file_path}')
                    continue
                
                # 写回文件
                with open(file_path, 'wb') as f:
                    f.write(new_content)
                stats['converted'] += 1
                print(f'已转换: {file_path}')
            except Exception as e:
                stats['failed'] += 1
                print(f'转换失败: {file_path}, 错误: {str(e)}')
    
    return stats

def select_folder():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    folder_path = filedialog.askdirectory(title='选择要转换的文件夹')
    if folder_path:
        print(f'开始转换文件夹: {folder_path}')
        stats = convert_line_endings(folder_path)
        print('\n转换统计:')
        print(f'处理文件总数: {stats["total"]}')
        print(f'成功转换数量: {stats["converted"]}')
        print(f'无需转换数量: {stats["no_need"]}')
        print(f'转换失败数量: {stats["failed"]}')
        print('\n转换完成！')
        input('\n按回车键退出...')
    else:
        print('未选择文件夹')
        input('\n按回车键退出...')

if __name__ == '__main__':
    select_folder()
