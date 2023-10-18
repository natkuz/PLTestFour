import pytest
import yaml
from ssh_checkout import ssh_checkout, ssh_getout
from datetime import datetime

with open("config.yaml", encoding='UTF-8') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folder():
    yield ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                        f"mkdir -p {data.get('folder_in')} {data.get('folder_out')} {data.get('folder_fld')}", "",
                        data.get('port'))
    return ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                        f"rm -r {data.get('folder_in')} {data.get('folder_out')} {data.get('folder_fld')}", "",
                        data.get('port'))


@pytest.fixture()
def make_file():
    return ssh_checkout(data.get('host'), data.get('user'), data.get('passwd'),
                        f"cd {data.get('folder_in')}; touch file1 file2 file3", "", data.get('port'))


@pytest.fixture()
def write_stat():
    yield
    stat = ssh_getout(data.get('host'), data.get('user'), data.get('passwd'), "cat /proc/loadavg", data.get('port'))
    w_stat = f"time: {datetime.now().strftime('%H:%M:%S.%f')} count:{data.get('count')} size: {data.get('bs')} load: {stat}"
