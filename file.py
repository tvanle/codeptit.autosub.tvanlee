import os
from pathlib import Path

from AutoSubmit.ultis.handle_string import get_file_name


def load_abs_file(url: str):
    name = get_file_name(url)
    
    if not name:
        return None
    
    resources_dir = os.path.join(os.getcwd(), "resource")
    
    if not os.path.isdir(resources_dir):
        raise FileNotFoundError(f"Thư mục 'resources' không tồn tại: {resources_dir}")
    
    for file in os.listdir(resources_dir):
        if file.startswith(name):
            return os.path.abspath(os.path.join(resources_dir, file))
    
    # Nếu không tìm thấy file nào phù hợp
    raise FileNotFoundError(f"Không tìm thấy file bắt đầu với '{name}' trong thư mục resources.")

if __name__ == "__main__":
    print(load_abs_file("https://code.ptit.edu.vn/student/question/CHELLO"))