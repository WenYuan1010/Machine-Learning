# -*- coding: utf-8 -*-
"""
利用百度的UIE工具 实现人才项目的信息提取

Created on 2022年7月18日 18点00分
@author  liutaixing
@version 1.0
"""

import pandas as pd
from pprint import *
from paddlenlp import Taskflow


df=pd.read_excel('person2.xlsx')
schema=['学历','职称','本科学校']#'学校及学位','公司及职位','现任公司及职位'
uie=Taskflow('information_extraction', schema=schema)
'''
微调可以提高准确度，微调的整体过程见网站：
https://github.com/PaddlePaddle/PaddleNLP/tree/develop/model_zoo/uie#%E8%BD%BB%E5%AE%9A%E5%88%B6%E5%8A%9F%E8%83%BD
因为涉及标注工具doccano ，这里只写了不需要微调时的通用代码，而这在一些场景就已经够用了。
微调过程的代码：

-----------------数据转换-----------------------
需要注意的是 数据转换时我们选择7.1的转换方式 其他的可能出错
7.1 抽取式任务数据转换
当标注完成后，在 doccano 平台上导出 JSONL(relation) 形式的文件，并将其重命名为 doccano_ext.json 后，放入 ./data 目录下。
通过 doccano.py 脚本进行数据形式转换，然后便可以开始进行相应模型训练。
！python doccano.py \
    --doccano_file ./data/doccano_ext.json \
    --task_type "ext" \
    --save_dir ./data \
    --negative_ratio 5

可配置参数说明：
doccano_file: 从doccano导出的数据标注文件。
save_dir: 训练数据的保存目录，默认存储在data目录下。
negative_ratio: 最大负例比例，该参数只对抽取类型任务有效，适当构造负例可提升模型效果。负例数量和实际的标签数量有关，最大负例数量 = negative_ratio * 正例数量。该参数只对训练集有效，默认为5。为了保证评估指标的准确性，验证集和测试集默认构造全负例。
splits: 划分数据集时训练集、验证集所占的比例。默认为[0.8, 0.1, 0.1]表示按照8:1:1的比例将数据划分为训练集、验证集和测试集。
task_type: 选择任务类型，可选有抽取和分类两种类型的任务。
options: 指定分类任务的类别标签，该参数只对分类类型任务有效。默认为["正向", "负向"]。
prompt_prefix: 声明分类任务的prompt前缀信息，该参数只对分类类型任务有效。默认为"情感倾向"。
is_shuffle: 是否对数据集进行随机打散，默认为True。
seed: 随机种子，默认为1000.
separator: 实体类别/评价维度与分类标签的分隔符，该参数只对实体/评价维度级分类任务有效。默认为"##"。   
-----------------模型微调-----------------
!python finetune.py \
    --train_path "./data/train.txt" \
    --dev_path "./data/dev.txt" \
    --save_dir "./checkpoint" \
    --learning_rate 1e-5 \
    --batch_size 30 \
    --max_seq_len 512 \
    --num_epochs 100 \
    --model "uie-base" \
    --seed 1000 \
    --logging_steps 10 \
    --valid_steps 100 \
    --device "gpu"
可配置参数说明：

train_path: 训练集文件路径。
dev_path: 验证集文件路径。
save_dir: 模型存储路径，默认为./checkpoint。
learning_rate: 学习率，默认为1e-5。
batch_size: 批处理大小，请结合机器情况进行调整，默认为16。
max_seq_len: 文本最大切分长度，输入超过最大长度时会对输入文本进行自动切分，默认为512。
num_epochs: 训练轮数，默认为100。
model: 选择模型，程序会基于选择的模型进行模型微调，可选有uie-base, uie-medium, uie-mini, uie-micro和uie-nano，默认为uie-base。
seed: 随机种子，默认为1000.
logging_steps: 日志打印的间隔steps数，默认10。
valid_steps: evaluate的间隔steps数，默认100。
device: 选用什么设备进行训练，可选cpu或gpu。

----------------模型评估-----------------（这部分当时运行时报错 一直没解决，但是不影响当时的效果。因此可以选择不运行）
!python evaluate.py \
    --model_path "./checkpoint/model_best" \
    --test_path "./data/dev.txt" \
    --batch_size 16 \
    --max_seq_len 512

----------------------定制模型一键预测------------------------
paddlenlp.Taskflow装载定制模型，通过task_path指定模型权重文件的路径，路径下需要包含训练好的模型权重文件model_state.pdparams。

from pprint import pprint
from paddlenlp import Taskflow

schema = ['出发地', '目的地', '费用', '时间']
# 设定抽取目标和定制化模型权重路径
my_ie = Taskflow("information_extraction", schema=schema, task_path='./checkpoint/model_best')
pprint(my_ie("城市内交通费7月5日金额114广州至佛山"))
结果：[{'出发地': [{'end': 17,
           'probability': 0.9975287467835301,
           'start': 15,
           'text': '广州'}],
  '时间': [{'end': 10,
          'probability': 0.9999476678061399,
          'start': 6,
          'text': '7月5日'}],
  '目的地': [{'end': 20,
           'probability': 0.9998511131226735,
           'start': 18,
           'text': '佛山'}],
  '费用': [{'end': 15,
          'probability': 0.9994474579292856,
          'start': 12,
          'text': '114'}]}]
          
'''

for i in df['简介'][:2]:
    if pd.isna(i):
        continue
    else:
        print(i)
        pprint(uie(i))