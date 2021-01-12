import logging
import os
import shutil
import tarfile
import time
import zipfile
from datetime import datetime
from os import listdir
from os.path import isdir

import mgzip

import sequarchtool_config as cfg


def logging_bucket(messages):
    logging.basicConfig(filename='sequarchtool.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)
    logging.info('%s', messages)
    print(str(datetime.now()) + messages)


def directory_list(path):
    res = [f for f in listdir(path) if isdir(path)]
    return res


def compress_zip(src_fullpath, dest_full_path_w_filename):
    dest_full_path_w_filename += ".zip"
    with zipfile.ZipFile(dest_full_path_w_filename, 'w') as zip_:
        rootpath = src_fullpath
        for (paths, dir__, files) in os.walk(src_fullpath):
            for f in files:
                fullpath = os.path.join(paths, f)
                relpath = os.path.relpath(fullpath, rootpath)
                zip_.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
        zip_.close()


def archive_tarball(src_fullpath, dirname):
    dest_filename = dirname + ".tar"
    tar = tarfile.open(cfg.origin_path + "/" + dest_filename, "x:")
    tar.add(src_fullpath, arcname=dirname)
    tar.close()


def compress_gzip(target_fullpath_w_filename):
    output_fullpath_w_filename = target_fullpath_w_filename + ".gz"
    target_filestream = open(target_fullpath_w_filename, "rb")
    output_gz = mgzip.open(output_fullpath_w_filename, "wb", compresslevel=9)
    data = target_filestream.read()
    output_gz.write(data)
    output_gz.close()


def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def get_file_size(file_path) -> str:
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return str(convert_bytes(file_info.st_size))


if __name__ == "__main__":
    if not os.path.isdir(cfg.destination_path):
        logging_bucket(" >> Not found destination path.")
        exit()

    if not os.path.isdir(cfg.origin_path):
        logging_bucket(" >> Not found origin path.")
        exit()

    try:
        join_path_dsstore = os.path.join(cfg.origin_path, ".DS_Store")
        os.remove(join_path_dsstore)
        logging_bucket(" >> .DS_Store removed.")
    except:
        pass

    for dirname in directory_list(cfg.origin_path):
        filename_w_tar = dirname + ".tar"
        filename_w_tar_gz = filename_w_tar + ".gz"
        join_fullpath_path = os.path.join(cfg.origin_path, dirname)
        # example) "/Volume/User/Catalog" + "Potrait" = "/Volume/User/Catalog/Portrait"
        join_fullpath_w_tar_filename = os.path.join(cfg.origin_path, filename_w_tar)
        # example) "/Volume/User/Catalog" + "Portrait" + ".tar" = "/Volume/User/Catalog/Portrait.tar"
        join_fullpath_w_gz_filename = os.path.join(cfg.origin_path, filename_w_tar_gz)
        # example) "/Volume/User/Catalog" + "Portrait" + ".tar.gz" = "/Volume/User/Catalog/Portrait.tar.gz"
        join_destination_fullpath_w_tar_filename = os.path.join(cfg.destination_path, filename_w_tar)
        # example) "/Volume/ExternalNAS/CatalogBackup" + "Portrait" + ".tar"
        #
        join_destination_fullpath_w_gz_filename = os.path.join(cfg.destination_path, filename_w_tar_gz)
        # example) "/Volume/ExternalNAS/CatalogBackup" + "Portrait" + ".tar.gz"
        #                                                       = "/Volume/ExternalNAS/CatalogBackup/Portrait.tar.gz"

        # Archive tarball
        logging_bucket(" >> Archiving " + dirname + ".")
        arch_tic = time.process_time()
        # compress_zip(join_fullpath_path, join_fullpath_with_filename)

        archive_tarball(join_fullpath_path, dirname)
        file_size = get_file_size(join_fullpath_w_tar_filename)
        logging_bucket(" >>>> Tarball size :" + str(file_size) + ".")

        # # Compress tarball to gzip
        # compress_gzip(join_fullpath_w_tar_filename)
        # os.remove(join_fullpath_w_tar_filename)
        arch_toc = time.process_time()
        # file_size = get_file_size(join_fullpath_w_gz_filename)
        # logging_bucket(" >>>> Compressed file size :" + str(file_size) + ".")
        arch_proctime = str("{0:.2f}".format(arch_toc - arch_tic))
        logging_bucket(" >> Archiving time : " + str(arch_proctime) + "s.")

        # Transfer to remote point
        # logging_bucket(" >> Moving " + filename_w_tar_gz)
        logging_bucket(" >> Moving " + filename_w_tar)
        move_tic = time.process_time()
        shutil.move(join_fullpath_w_tar_filename, join_destination_fullpath_w_tar_filename)
        # shutil.move(join_fullpath_w_gz_filename, join_destination_fullpath_w_gz_filename)
        move_toc = time.process_time()
        move_proctime = str("{0:.2f}".format(move_toc - move_tic))
        logging_bucket(" >> File trasfer time: " + str(move_proctime) + "s.")

    logging_bucket(" >> Done Archiving.")
