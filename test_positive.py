import subprocess
from checkers import checkout, getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        result1 = checkout('cd {}; 7z a {}/arx'.format(data['folder_in'], data['folder_out']), 'Everything is Ok')
        result2 = checkout('ls {}'.format(data['folder_out']), 'arx.7z')
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, make_files):
        # test2
        res = []
        res.append(checkout('cd {}; 7z a {}/arx2'.format(data['folder_in'], data['folder_out']), 'Everything is Ok'))
        res.append(checkout('cd {}; 7z e arx2.7z -o{} -y'.format(data['folder_out'], data['folder1']), 'Everything is Ok'))
        for item in make_files:
            res.append(checkout('ls {}'.format(data['folder1']), item))
        assert all(res), 'test2 FAIL'

    def test_step3(self):
        # test3
        assert checkout('cd {}; 7z t arx.{}'.format(data['folder_out'], data['type']), 'Everything is Ok'), "test3 FAIL"

    def test_step4(self):
        # test4
        assert checkout('cd {}; 7z u arx2.{}'.format(data['folder_out'], data['type']), 'Everything is Ok'), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(checkout('cd {}; 7z a {}/arx'.format(data['folder_in'], data['folder_out']), 'Everything is Ok'))
        for i in make_files:
            res.append(checkout('cd {}; 7z l arx.{}'.format(data['folder_out'], data['type'], data['folder1']), i))
        assert all(res), 'test5 FAIL'

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout('cd {}; 7z a {}/arx'.format(data['folder_in'], data['folder_out']), 'Everything is Ok'))
        res.append(checkout('cd {}; 7z x arx.{} -o{} -y'.format(data['folder_out'], data['type'], data['folder2']), 'Everything is Ok'))
        for i in make_files:
            res.append(checkout('ls {}'.format(data['folder2']), i))

        res.append(checkout('ls {}'.format(data['folder2']), make_subfolder[0]))
        res.append(checkout('ls {}/{}'.format(data['folder2'], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        assert checkout('cd {}; 7z d arx.{}'.format(data['folder_out'], data['type']),'Everything is Ok'), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            res.append(checkout('cd {}; 7z h {}'.format(data['folder_in'], i), 'Everything is Ok'))
            hash = getout('cd {}; crc32 {}'.format(data['folder_in'], i)).upper()
            res.append(checkout('cd {}; 7z h {}'.format(data['folder_in'], i), hash))
        assert all(res), "test8 FAIL"


