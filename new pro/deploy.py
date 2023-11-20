from sshcheckers import ssh_checkout

def deploy():
    res = []
    upload_files('0.0.0.0', 'user2', '1111', '/home/user/PycharmProjects/pythonProject2/p7zip-full.deb', '/home/user2'
                                                                                                         '/p7zip-full'
                                                                                                         '.deb')
    res.append(ssh_checkout('0.0.0.0', 'user2', '1111', 'echo "1111" | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                            'Настраивается пакет'))
    res.append(
        ssh_checkout('0.0.0.0', 'user2', '1111', 'echo "1111" | sudo -S dpkg -s p7zip-full.deb', 'Status: install ok '
                                                                                                 'installed'))
    return all(res)


if deploy():
    print('Ok')
else:
    print('Not ok')
