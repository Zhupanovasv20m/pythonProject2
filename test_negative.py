import yaml
from checkers import ssh_checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_bad_arx):
        # test1
        assert ssh_checkout_negative('0.0.0.0', 'user2', '1111',
                                     'cd {}; 7z e bad_arx.{} -o{} -y'.format(data['folder_out'], data['type'],
                                                                             data['folder1']),
                                     'ERRORS'), "test1 FAIL"

    def test_step2(self):
        # test2
        assert ssh_checkout_negative('0.0.0.0', 'user2', '1111',
                                     'cd {}; 7z t bad_arx.{}'.format(data['folder_out'], data['type']),
                                     'ERRORS'), "test2 FAIL"
