import os

subtitle_dir = 'CourseraScript'

course_name = ''
chapter = 1
week = 1

check_cw = input(f'{course_name}-{chapter}-{week} if Right, type "y"\n')
if check_cw != 'y':
    exit(0)

file_list = sorted(os.listdir(os.path.join(subtitle_dir, 'script')), key=lambda x: (len(x), x))

check_cw = input(f'check order:\n {file_list}\n')
if check_cw != 'y':
    exit(0)

print(file_list)
# file name
w_file = open(os.path.join(subtitle_dir, 'merged_script', f'{course_name}-{chapter}-{week}.txt'), 'w')
w_file.write(f'[{chapter}-{week}]\n\n')

change = [('\n', ' '), ('. ', '.\n'), ('? ', '?\n'), ('! ', '!\n'), ('니다 ', '니다.\n'), 
          ('어요 ', '어요.\n'), ('세요 ', '세요.\n'), ('십시오 ', '십시오.\n'), ('시다 ', '시다.\n'), ('데요 ', '데요.\n'),
          ('이죠 ', '이죠.\n'), ('시죠 ', '시죠.\n'), ('이에요 ', '이에요.\n'), ('예요 ', '예요.\n'), ('해요 ', '해요.\n')]

for i, file_name in enumerate(file_list, 1):
    r_file = open(os.path.join(subtitle_dir, 'script', file_name), "r", encoding='utf-8')
    lines = r_file.read()
    for old, new in change:
        lines = lines.replace(old, new)
    r_file.close()

    w_file.write(f'[{chapter}-{week}-{i}]\n\n')
    w_file.write(lines)
    w_file.write('\n\n')
w_file.close()
