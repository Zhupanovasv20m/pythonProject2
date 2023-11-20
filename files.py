import subprocess
import paramiko

from checkers import ssh_get



def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f'File {local_path} in {remote_path}')
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def getout(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout


# def save_log(starttime, name):
#     with open(name, 'w') as f:
#         f.write(ssh_get('0.0.0.0', 'user2', '1111',
#                         'echo "1111" | sudo -S journalctl --since "{}">> stat.txt'.format(starttime)))
#
#
# save_log(start_time, 'lll.txt')
