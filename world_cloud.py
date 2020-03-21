from wordcloud import WordCloud
import jieba,imageio
class wordcloud:
    def __init__(self):
        self.color_mask = imageio.imread("res/logo.png")
        self.f = open('data/data.txt', encoding='utf-8')
        self.txt = self.f.read()
        self.txt_list = jieba.lcut(self.txt)
        self.string = ' '.join(self.txt_list)
        self.cloud = WordCloud(width=1920,
            height=1080,
            font_path='res/simhei.ttf',
            background_color='white',
            mask=self.color_mask,
            #max_words=880,
            scale=25,
            #stopwords=({'吸吸','哈哈哈','欧拉','这个','不是'})
        )
    def run(self):
        self.cloud.generate(self.string)
        self.cloud.to_file('wordcloud.png')

    def cipin(self):
        words = self.txt_list
        counts = {}
        for word in words:
            if len(word) == 1:
                continue
            else:
                counts[word] = counts.get(word, 0) + 1
        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)
        for i in range(20):
            word, count = items[i]
            print("{0:<10}{1:<5}".format(word, count))

W = wordcloud()
W.run()
#W.cipin()