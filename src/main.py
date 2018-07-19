#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:main
   Author:jasonhaven
   date:18-7-12
-------------------------------------------------
   Change Activity:18-7-12:
-------------------------------------------------
"""
from hanziconv import HanziConv
import jieba
import nltk
import os
import sys
import codecs
import re
import datetime
import codecs


def check(word_lst):
	rst = []
	for w in word_lst:
		for s in rules:
			p = re.compile(s)
			match = re.match(p, w)
			if match:
				rst.append(w)

	for w in word_lst:
		if w in vocab:
			rst.append(w)
	return list(set(rst))


def load_stop_word_list(file_path):
	stop_word_lst = [line.strip() for line in codecs.open(file_path, 'r', encoding='utf-8').readlines()]
	return list(set(stop_word_lst))


def load_vocab(dir_path):
	vocab_has_vec_zh = []
	vocab_has_vec_en = []
	vocab_no_vec = []

	with codecs.open(dir_path + os.sep + 'vocab_has_vec_zh.txt', 'r', encoding='utf-8') as f:
		vocab_has_vec_zh.extend([word.strip() for word in f.readlines()])

	with codecs.open(dir_path + os.sep + 'vocab_has_vec_en.txt', 'r', encoding='utf-8') as f:
		vocab_has_vec_en.extend([word.strip() for word in f.readlines()])

	with codecs.open(dir_path + os.sep + 'vocab_no_vec.txt', 'r', encoding='utf-8') as f:
		vocab_no_vec.extend([word.strip() for word in f.readlines()])
	return vocab_has_vec_zh + vocab_has_vec_en + vocab_no_vec


def load_every_thing():
	# load stop words
	print('INFO : Loading stopwords......')
	stop_word_lst = load_stop_word_list('../data/stop_word.txt')

	# load sensitive vocab
	print('INFO : Loading sensitive vocabulary......')
	vocab = load_vocab('../data/vocab')

	return stop_word_lst, vocab


def main(sent):
	global num_sent
	global count_words
	result = []
	sent = HanziConv.toSimplified(sent)

	'''
	英文处理：分词、词形还原
	'''
	word_lst = nltk.word_tokenize(sent)
	wn = nltk.WordNetLemmatizer()
	word_lst = [wn.lemmatize(w) for w in word_lst]

	'''
	中文处理：分词
	'''
	word_lst = jieba.cut(' '.join(word_lst), cut_all=True)

	# remove stop word
	word_lst = [word.strip() for word in word_lst if word.strip() not in stop_word_lst + ['']]

	'''
	处理
	'''
	temp = check(word_lst)
	result.extend(temp)

	'''
	输出结果
	'''
	if result and len(result) >= 2:
		count_words+=len(result)
		num_sent+=1
		fp.write('{}:{}{}\n'.format(num_sent,sent,result))
		print('No.',num_sent,sent.strip())
		print('Total',count_words,','.join(result))

	print('')




if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print('illegal arguments')
		sys.exit(0)
	
	num_sent=0
	count_words=0

	fp=codecs.open('output.txt','w',encoding='utf-8')
	
	with codecs.open('../data/rules.txt',encoding='utf-8') as f:
		rules=['"{}"'.format(w.strip()) for w in f.readlines()]

	stop_word_lst, vocab = load_every_thing()
	jieba.load_userdict('../data/vocab/vocab_has_vec_zh.txt')

	starttime = datetime.datetime.now()
	
	with codecs.open(sys.argv[1], 'r', encoding='utf-8') as f:
		for sent in f.readlines():
			if sent.strip() != '':
				main(sent.strip())
				
	
	fp.close()

	endtime = datetime.datetime.now()
	print("finished in {} seconds".format(endtime - starttime))
