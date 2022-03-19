import jieba
import jieba.posseg as pesg

string = '什么时候举办四六级'
# jieba.enable_paddle()
jieba.load_userdict('dictionary.txt')
words = pesg.cut(string, use_paddle=True)
for i in words:
    print(i.word, i.flag)
