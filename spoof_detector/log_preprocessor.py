raw_f = open('./clean_log.txt', 'r')

raw_log = raw_f.readline()

new_log = raw_log.replace('  0,', '\n  0,')

with open('./clean_log_new.txt', 'w') as f:
    f.write(new_log)