## 国家统计局区划地址信息爬取

> 使用scrapy框架进行数据爬取

#### 1、配置要爬取的年份
在settings.py中
```python
# 配置要爬取的年份
region_year = 2021
```

#### 2、配置数据库
在settings.py中
```python
user = "xxx"  # mysql用户名
passwd = "xxx"  # mysql用户密码
host = "172.xx.xx.xx"  # mysql ip address
db = "xxxx"  # 用于设置数据库名，这个必须提前创建好
```
执行 ./sql/create_table.sql 创建表信息


#### 3、执行脚本进行爬取
```shell
python ./stats_data_spider/run.py
```

#### 4、由于网站有反爬限制，不能过快爬取，可以配置每个页面等待时间
```python
# 每爬一个页面等待1秒，自己测试下情况，进行相应配置
sleep_time = 1.0
```



### 附：
本项目在[原项目](git@github.com:Ingram7/stats_data_spider.git)上进行了部分改造，插入到mysql数据库中

感谢：Ingram7的项目分享
