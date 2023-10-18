from ssh_checkout import ssh_checkout, ssh_getout
from checkout import getout
import yaml
import pytest

with open("config.yaml", encoding='UTF-8') as f:
    data = yaml.safe_load(f)


class TestChPositive:

    def s_log(self, file_name, write_stat):
        with open(file_name, 'w') as f:
            f.write(getout(f"journalctl --since '{write_stat}'"))

    def test_step_one(self, make_folder, make_file, write_stat):
        # test1
        self.s_log(write_stat, "log_test1.txt")
        assert ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                        f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}arch -t{data.get('type_arch')}",
                        "Everything is Ok", data.get('port')), "test1 FAIL"

    def test_step_two(self, make_folder, make_file, write_stat):
        # test2
        self.s_log(write_stat, "log_test2.txt")
        assert ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                            f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}arch -t{data.get('type_arch')}",
                            "", data.get('port'))
        assert ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                            f"cd {data.get('folder_out')}; 7z d ./arch.7z file1", "Everything is Ok",
                            data.get('port')), "test2 FAIL"

    def test_step_three(self, make_folder, make_file, write_stat):
        # test3
        self.s_log(write_stat, "log_test3.txt")
        assert ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                            f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}arch", "", data.get('port'))
        assert ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                            f"cd {data['folder_out']}; 7z l ./arch.7z", "Name", data.get('port')), "test3 FAIL"

    def test_step_four(self, make_folder, make_file, write_stat):
        # test3
        self.s_log(write_stat, "log_test4.txt")
        assert ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                            f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}arch", "", data.get('port'))
        assert ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                            f"cd {data['folder_out']}; 7z x ./arch.7z", "Everything is Ok",
                            data.get('port')), "test4 FAIL"

    def test_step_five(self, make_folder, make_file, write_stat):
        res1 = ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                            f"cd {data['folder_in']}; 7z h file2 -t{data.get('type_arch')}", "Everything is Ok",
                            data.get('port'))
        hs = ssh_getout(data.get('host'), data.get('user'), data.get('passwd'),
                        f"cd {data['folder_in']}; crc32 file2".upper(), data.get('port'))
        res2 = ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                            f"cd {data['folder_in']}; 7z h file2", hs, data.get('port'))
        self.s_log(write_stat, "log_test5.txt")
        assert res1 and res2, "test5 FAIL"


if __name__ == '__main__':
    pytest.main(["-vv"])