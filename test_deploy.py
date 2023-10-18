from ssh_checkout import ssh_checkout, upload_files
from checkout import getout
import yaml

with open('config.yaml', encoding='UTF-8') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def s_log(self, file_name, write_stat):
        with open(file_name, 'w') as f:
            f.write(getout(f"journalctl --since '{write_stat}'"))

    def test_deploy(self, write_stat):
        res = []
        upload_files(data.get('host'), data.get('user'), data.get('passwd'), data.get('local_path'),
                     data.get('remote_path'), data.get('port'))
        res.append(ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                                f"echo {data.get('passwd')} | sudo -S dpkg -i {data.get('remote_path')}",
                                "Настраивается пакет", data.get('port')))
        res.append(ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                                f"echo {data.get('passwd')} | sudo -S dpkg -s {data.get('package_name')}",
                                "Status: install ok installed", data.get('port')))
        self.s_log(write_stat, "log_deploy.txt")
        assert all(res), "test_deploy FAIL"
