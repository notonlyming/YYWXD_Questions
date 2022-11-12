import os
import random

class Question:
    def __init__(self) -> None:
        self.id = str()
        self.question = str()
        self.options:list[str] = list()
        self.image_path:str = str()
        self.answer:str = str()
    
    def __str__(self) -> str:
        # 转字符串时输出问题
        return '{} {}{}\n{}'.format(
            self.id,
            self.question,
            '\n' + f'<img src="{self.image_path}">' if self.image_path else '',
            '\n'.join(self.options)
            )

    def __repr__(self) -> str:
        return self.id
    
    def to_final_show(self) -> str:
        self.shuffle() # 输出最终答案时，打乱！
        # 输出问题但换行要使用HTML的<br>标签了。并且附上答案。之间用制表符分隔。
        return str(self).replace('\n', '<br>').replace('\t', ' ') + '\t' + self.answer.replace('\t', ' ')

    def shuffle(self) -> None:
        random.shuffle(self.options)

if __name__ == '__main__':
    txt_path1 = './A类题库(v20211022).txt'
    txt_path2 = './总题库(v20211022).txt'
    txt_path3 = './B类题库(v20211022).txt'
    txt_path4 = './C类题库(v20211022).txt'
    this_txt_path = txt_path4
    with open(this_txt_path, 'r', encoding='gbk') as f:
        txt_tmp = f.read()

    pic_filenames:list = os.listdir('./总题库附图(v20211022)')

    questions:list[Question] = list()
    # 每行遍历
    for line in txt_tmp.split('\n'):
        if len(line) == 0:
            # 空行跳过
            continue
        elif len(line) >= 3:
            # 也许是正常行
            line_letter = line[1]
            # 读取行的标志
            if line_letter == 'I':
                questions.append(Question())
                questions[-1].id = line[3:]
                if questions[-1].id + '.jpg' in pic_filenames:
                    questions[-1].image_path = f'{questions[-1].id + ".jpg"}'
                continue
            elif line_letter == 'Q':
                questions[-1].question = line[3:]
                continue
            elif line_letter in 'abcdefgh'.upper():
                questions[-1].options.append(line[3:])
                # 默认答案为A，因此记录。
                if line_letter == 'A':
                    questions[-1].answer = line[3:]
                continue
            elif line_letter == 'P':
                continue
            else:
                raise IOError(f'Question sign not correct. {line}')
        else:
            raise IOError(f'line length not correct. {line}')

    print(questions[7].to_final_show())
    with open(f'{this_txt_path}-result.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join([question.to_final_show() for question in questions]))
