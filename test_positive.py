import subprocess

tst = '/home/user/tst'
out = '/home/user/out'
folder1 = '/home/user/folder1'
folder2 = '/home/user/folder2'


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    # test1
    result1 = checkout('cd {}; 7z a {}/arx2'.format(tst, out), 'Everything is Ok')
    result2 = checkout('ls {}'.format(out), 'arx2.7z')
    assert result1 and result2, "test1 FAIL"


def test_step2():
    # test2
    result1 = checkout('cd {}; 7z e arx2.7z -o{} -y'.format(out, folder1), 'Everything is Ok')
    result2 = checkout('ls {}'.format(folder1), 'qwe')
    result3 = checkout('ls {}'.format(folder1), 'asd')
    result4 = checkout('ls {}'.format(folder1), 'code')
    assert result1 and result2 and result3 and result4, "test2 FAIL"


def test_step3():
    # test3
    assert checkout('cd {}; 7z t arx2.7z'.format(out), 'Everything is Ok'), "test3 FAIL"


def test_step4():
    # test4
    assert checkout('cd {}; 7z u arx2.7z'.format(out), 'Everything is Ok'), "test4 FAIL"


def test_step5():
    # test5
    result1 = checkout('cd {}; 7z l arx2.7z'.format(out, folder1), 'qwe')
    result2 = checkout('cd {}; 7z l arx2.7z'.format(out, folder1), 'asd')
    result3 = checkout('cd {}; 7z l arx2.7z'.format(out, folder1), 'code')
    assert result1 and result2 and result3, 'test5 FAIL'


def test_step6():
    # test6
    result1 = checkout('cd {}; 7z x arx2.7z -o{} -y'.format(out, folder2), 'Everything is Ok')
    result2 = checkout('ls {}'.format(folder2), 'qwe')
    result3 = checkout('ls {}'.format(folder2), 'asd')
    result4 = checkout('ls {}'.format(folder2), 'code')
    assert result1 and result2 and result3 and result4, "test6 FAIL"


def output(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout


print(output('cd /home/user/tst; 7z h qwe'))


def test_step7():
    # test7
    result1 = checkout('cd {}; 7z h qwe'.format(tst), 'Everything is Ok')
    result2 = output('cd /home/user/tst; 7z h qwe')
    result3 = checkout('cd {}; 7z h qwe'.format(tst), result2)
    assert result1 and result3, "test7 FAIL"
