import os

subtitle_dir = 'CourseraScript'
chapter = 3
week = 3

file_list = sorted(os.listdir(os.path.join(subtitle_dir, 'script')))

w_file = open(os.path.join(subtitle_dir, 'merged_script', f'{chapter}-{week}.txt'), 'w')
w_file.write(f'[{chapter}-{week}]\n\n')

change = [('\n', ' '), ('. ', '.\n'), ('? ', '?\n'), ('! ', '!\n')]
for i, file_name in enumerate(file_list, 1):
    r_file = open(os.path.join(subtitle_dir, 'script', file_name), "r")
    lines = r_file.read()
    for old, new in change:
        lines = lines.replace(old, new)
    r_file.close()

    w_file.write(f'[{chapter}-{week}-{i}]\n\n')
    w_file.write(lines)
    w_file.write('\n\n')
w_file.close()
