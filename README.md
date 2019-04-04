# Book118 下载器
可用于下载[book118](https://max.book118.com/)的PDF文档
## 安装及使用
### 1. 安装Python3  
### 2. 安装`requests`、`Pillow`、`threadpool`  
  `pip install equests Pillow threadpool`  
### 3. 使用  
  `python Book118.py pid [filename]`  
  pid是要下载页面的链接中最后的数字  
  filename保存文件名称，可省略  
## 参考
[documentDownloader](https://github.com/OhYee/documentDownloader)
- 使用threadpool并发下载，提高下载速度
- 使用requests的session，提高请求速度
- 使用pillow根据文档页面大小保存pdf,不固定为A4大小 
