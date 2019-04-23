# python的format使用

- 作者：codehackfox@gmail.com
- 时间：2018-10-26 17:15:23

### 0x00、介绍

- format优点
    * 1.不需要理会数据类型的问题，在%方法中%s只能替代字符串类型
    * 2.单个参数可以多次输出，参数顺序可以不相同
    * 3.填充方式十分灵活，对齐方式十分强大
    * 4.官方推荐用的方式，%方式将会在后面的版本被淘汰

```python

print('hello {0}'.format('world'))

// hello world

```

- format格式
```python

#format的格式
replacement_field ::= "{" [field_name] ["!" conversion] [":" format_spec] "}"
field_name ::= arg_name ("." attribute_name | "[" element_index "]")*
arg_name ::= [identifier | integer]
attribute_name ::= identifier
element_index ::= integer | index_string
index_string ::= <any source character except "]"> +
conversion ::= "r" | "s" | "a"
format_spec ::= <described in the next section>

```

- format_spec 的格式
```python

format_spec 　　::= 　　[[fill]align][sign][#][0][width][,][.precision][type]
fill 　　　　　::= 　　<any character>
align 　　　　::= 　　"<" | ">" | "=" | "^"
sign 　　　　 ::= 　　"+" | "-" | " "
width 　　　　 ::= 　　 integer
precision 　　　　::= 　　 integer
type 　　　　::= 　　"b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"

```

### 0x01、应用

#### 一、填充

- 1.通过位置来填充字符串

```python

print('hello {0} i am {1}'.format('Kevin','Tom'))                  # hello Kevin i am Tom
print('hello {} i am {}'.format('Kevin','Tom'))                # hello Kevin i am Tom
print('hello {0} i am {1} . my name is {0}'.format('Kevin','Tom')) # hello Kevin i am Tom . my name is Kevin

```

- 2.通过key来填充

```python

print('hello {name1} i am {name2}'.format(name1='Kevin',name2='Tom') )    # hello Kevin i am Tom

```

- 3.通过下标填充

```python

names=['Kevin','Tom']
print('hello {names[0]} i am {names[1]}'.format(names=names))                  # hello Kevin i am Tom
print('hello {0[0]} i am {0[1]}'.format(names))                                # hello Kevin i am Tom

```

- 4..通过字典的key    注意访问字典的key，不用引号的

```python

names={'name':'Kevin','name2':'Tom'}
print('hello {names[name]} i am {names[name2]}'.format(names=names))    # hello Kevin i am Tom

```

- 5.通过对象的属性

```python

class Names():
    name1='Kevin'
    name2='Tom'
print('hello {names.name1} i am {names.name2}'.format(names=Names))                  # hello Kevin i am Tom

```

- 6.使用魔法参数

```python

args=['lu']
kwargs = {'name1': 'Kevin', 'name2': 'Tom'}
print('hello {name1} {} i am {name2}'.format(*args, **kwargs))  # hello Kevin i am Tom

```

#### 二、格式转换

-  b、d、o、x分别是二进制、十进制、八进制、十六进制。


| 数字 | 格式 | 输出 | 描述 |
| --- | --- | --- | --- |
| 3.1415926 |{:.2f}  |3.14  |保留小数点后两位  |
| 3.1415926 | {:+.2f} |3.14  | 带符号保留小数点后两位 |
| -1 | {:+.2f} | -1 |带符号保留小数点后两位  |
|2.71828|	{:.0f}	|3	|不带小数|
|1000000|	{:,}	|1,000,000|	以逗号分隔的数字格式|
|0.25	|{:.2%}	|25.00%|	百分比格式|
|1000000000|	{:.2e}|	1.00E+09|	指数记法|
|25|	{0:b}|	11001|	转换成二进制|
|25	|{0:d}|	25|	转换成十进制|
|25	|{0:o}|	31|	转换成八进制|
|25	|{0:x}|	19|	转换成十六进制|

#### 三、对齐与填充

|数字|	格式|	输出|	描述|
| --- | --- | --- | --- | --- |
|5	|{:0>2}	|05	|数字补零 (填充左边, 宽度为2)|
|5	|{:x<4}|5xxx|	数字补x (填充右边, 宽度为4)|
|10|{:x^4}|x10x|	数字补x (填充右边, 宽度为4)|
|13	|{:10}|13|	右对齐 (默认, 宽度为10)|
|13	|{:<10}|13|	左对齐 (宽度为10)|
|13	|{:^10}|13|	中间对齐 (宽度为10)|

#### 四、其他
- 1.转义{和}符号
```python
prin('{{ hello {0} }}'.format('Kevin'))
# 跟%中%%转义%一样，formate中用两个大括号来转义
```

- 2.format作为函数
```python
f = 'hello {0} i am {1}'.format    
print(f('Kevin','Tom'))
```

- 3.格式化datetime
```python
now=datetime.now()
print('{:%Y-%m-%d %X}'.format(now))
```

- 4.{}内嵌{}
```python
print('hello {0:>{1}} '.format('Kevin',50))
```

- 5.叹号的用法
    * ！后面可以加s r a 分别对应str() repr() ascii()
    * 作用是在填充前先用对应的函数来处理参数
    * 差别就是repr带有引号，str()是面向用户的，目的是可读性，repr()是面向python解析器的，返回值表示在python内部的含义
```python
print("{!s}".format('2'))  # 2
print("{!r}".format('2'))   # '2'
```

