import os
import io
import time
import datetime
from zipfile import ZipFile
from socket import gaierror
from log_collector import constants
from scp import SCPClient, SCPException
from paramiko import SSHClient, AutoAddPolicy, SSHException


class ConnectionException(Exception):
    pass


def generate_new_folder(dir_path):
    """
    Generate new directory of format /dir_path/timestamp

    :param dir_path: path to directory
    :returns: path to new directory where to put logs
    """
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
    return os.path.join(dir_path, 'logs_%s' % ts)


def get_file_via_ssh(src, dst, host_name, host_user, host_password):
    """
    Get file via ssh from remote host

    :param src: source of the file on remote machine
    :param dst: destination of file on local machine
    :param host_name: fqdn or ip of host
    :param host_user: user to connect to host
    :param host_password: password to connect to host
    :raises: ConnectionException
    """
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect(host_name, username=host_user, password=host_password)
    except (SSHException, gaierror):
        raise ConnectionException(
            "Can't connect to host %s with user: %s and password: %s" %
            (host_name, host_user, host_password)
        )
    scp = SCPClient(ssh.get_transport())
    try:
        scp.get(src, dst)
    except SCPException:
        pass
    ssh.close()


def zip_dir(path):
    """
    Zip whole directory
    :param path: path to directory
    :return:
    """
    io_bytes = io.BytesIO()
    with ZipFile(io_bytes, "a") as zip_obj:
        for root, dirs, files in os.walk(path):
            zip_obj.write(root, os.path.relpath(root, constants.LOCAL_LOG_DIR))
            for f in files:
                filename = os.path.join(root, f)
                if os.path.isfile(filename):
                    file_path = os.path.join(
                        os.path.relpath(root, constants.LOCAL_LOG_DIR), f
                    )
                    zip_obj.write(filename, file_path)
    return io_bytes
