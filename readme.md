Detection of sensitive words
---

#### workflows

merge2one -> traditional2simple -> split_vocab -> main

- data/
    - model 训练好的词向量模型
    - one
        - one_en.txt 合并后的英文敏感词词表
        - one_zh.txt 合并后的中文敏感词词表
    - raw
        - chinese 原始中文敏感词词库
        - english 原始英文敏感词词库
    - vocab
        - vocab_has_vec_zh.txt 有词向量的中文敏感词
        - vocab_has_vec_en.txt 有词向量的英文敏感词
        - vocab_no_vec.txt 没有词向量的敏感词
    - stop_word.txt 停用词词表

- src/
  - util
    - logger.py 日志管理器
  - crawl_english_badwords.py 英文词库抓取
  - merge2one.py 合并词库
  - traditional2simple.py 繁简体转换
  - main.py 程序入口
  - split_vocab.py 拆分敏感词有词向量和没有词向量的部分