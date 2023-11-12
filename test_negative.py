import subprocess

tst = '/home/user/tst'
out = '/home/user/out'
folder1 = '/home/user/folder1'
folder2 = '/home/user/folder2'


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def test_step1():
    # test1
    assert checkout('cd /home/user/out; 7z e arx2.7z -o/home/user/folder1 -y'.format(out, folder1), 'ERRORS'), "test1 FAIL"


def test_step2():
    # test2
    assert checkout('cd {}; 7z t arx2.7z'.format(out), 'ERRORS'), "test2 FAIL"
