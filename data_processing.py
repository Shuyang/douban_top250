from urllib import request
from lxml import etree


def get_pages():
	for i in range(0, 250, 25):
		url = 'https://movie.douban.com/top250?start={start}&filter='.format(start=i)
		print(url)
		request.urlretrieve(url, 'data/raw/movie_{i}'.format(**locals()))

	for i in range(0, 250, 25):
		url = 'https://book.douban.com/top250?start={start}'.format(start=i)
		print(url)
		request.urlretrieve(url, 'data/raw/book_{i}'.format(**locals()))

def process_data():
	with open('data/movies.csv', 'w') as movie_csv:
		print('rank,title,ratings,rating_num,meta', file=movie_csv)
		for start in range(0, 250, 25):
			doc = open('data/raw/movie_{start}'.format(**locals())).read()
			tree = etree.HTML(doc)
			titles = tree.xpath("/html/body//ol//a/span[1][@class='title']")
			ratings = tree.xpath("//span[@class='rating_num']")
			rating_nums = tree.xpath("//div[@class='star']/span[last()]")
			metas = tree.xpath("//div[@class='bd']/p[@class='']")
			for i in range(25):
				print(
					start + i + 1, titles[i].text, ratings[i].text, rating_nums[i].text[:-3], 
					'/'.join(x.strip() for x in metas[i].itertext()),
					sep=',', file=movie_csv)

	with open('data/books.csv', 'w') as book_csv:
		print('rank,title,ratings,rating_num,meta', file=book_csv)
		for start in range(0, 250, 25):
			doc = open('data/raw/book_{start}'.format(**locals())).read()
			tree = etree.HTML(doc)
			titles = tree.xpath('//a[@title]')
			ratings = tree.xpath("//span[@class='rating_nums']")
			rating_nums = tree.xpath("//span[@class='pl']")
			metas = tree.xpath("//p[@class='pl']")
			for i in range(25):
				print(
					start + i + 1, titles[i].get('title'), ratings[i].text,
					rating_nums[i].text.split('\n')[1].strip()[:-3],
					metas[i].text, sep=',', file=book_csv
				)

process_data()