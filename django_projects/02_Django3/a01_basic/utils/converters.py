class MyYearConverter(object):
    # year的正则
    regex = '[0-9]{4}'

    # python使用， 在python 中以什么类型输出
    def to_python(self, value):
        return int(value)

    #  你在path中如何输入？
    def to_url(self, value):
        return "%04d"%value


