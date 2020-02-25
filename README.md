#  Python 图片无损压缩工具

#### 环境要求
    python >= 3.6 

#### 扩展依赖
    pip3 install -r requirements.txt

#### 打包成MacOS应用
    pyinstaller --onedir -n Compress  -i compress.icns -y -w -D compress.py

#### 打包成Windows应用
    pyinstaller --onedir -n Compress  -i compress.ico -y -w -D compress.py

#### 压缩前图片(14.6MB)
![image1](https://github.com/shangjinglong/compress/blob/master/_bKzOhUxczE_1.jpg）
    
#### 压缩后图片(133KB)
![image2](https://github.com/shangjinglong/compress/blob/master/_bKzOhUxczE_2.jpg）
        
#### 效果演示
![image3](https://github.com/shangjinglong/compress/blob/master/compress.gif）