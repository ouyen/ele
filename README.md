# 耍克鸡（大概

使用了[PKUAutoElective](https://github.com/zhongxinghong/PKUAutoElective)的验证码识别功能，用selenium随手写的（

除了原所需的包外还需安装selenium和[geckodriver](https://github.com/mozilla/geckodriver/releases)

需要将`config copy.json`重命名为`config.json`并编辑信息：

```
{
    "stuid":"1900019810",//学号
    "passwd":"114514",//密码
    "ele_set":["集合论与图论,1","集合论与图论,2"],//需要关注的课程，需要写入课程名和班号码（用,连接）
    "ele_type":0,//0:无双学位; 1:主修; 2:辅双
    "headless":0,//是否以无头模式运行
    "max_turn":300,//运行max_turn后重新登陆
    "state":0//选课阶段：0为补退选;1为补选
}
```
TAKE YOUR OWN RISK  

## todo

支持正则表达式（？