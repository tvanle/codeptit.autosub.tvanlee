# # AUTO SUB CODE PTIT
This project automates the submission of homework on **PTIT Online Judge** (https://code.ptit.edu.vn/) using Selenium. The script automatically logs in, submits the solution for a given assignment, and can handle multiple submissions.


## Usage 
1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run:
```
python main.py
```

4. Enter your credentials on the terminal when prompted.
```
Nhập tên tài khoản: 
Nhập mật khẩu:  

```
## Features

- **Automated Login and Assignment Submission**  
  Automatically logs into the PTIT website and submits assignments for you.

- **Handle File Uploads for Assignments**  
  The script supports uploading files for assignments automatically once logged in. Files can be placed in a designated **resource** folder and modified before submission.