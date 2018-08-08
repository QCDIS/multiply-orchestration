"""
Description
===========

This module containes functionality to create symbolic links. This is only supported for unix-based systems.
"""

from typing import List, Sequence, Optional
from multiply_core.observations import get_data_type_path, get_valid_type
from multiply_core.util import FileRef
import glob
import os

__author__ = 'Tonio Fincke (Brockmann Consult GmbH)'


def create_sym_link(file_ref: FileRef, folder: str, data_type: Optional[str] = None):
    """
    Puts a symbolic link to the file referenced by the fileref object into the designated folder. Only supported for
    linux.
    :param file_ref: A file to be referenced from another folder.
    :param folder: The folder into which the data shall be placed.
    :param data_type: The data type of the file ref. Will be determined if not given.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    if data_type is None:
        data_type = get_valid_type(file_ref.url)
    relative_path = get_data_type_path(data_type, file_ref.url)
    file_name = file_ref.url.split('/')[-1]
    new_file = os.path.join(folder, relative_path, file_name)
    if os.path.isdir(file_ref.url):
        # new_file is folder, too
        os.makedirs(new_file)
        globbed_files = glob.glob('{}**'.format(file_ref.url), recursive=True)
        for file in globbed_files:
            if os.path.isdir(file):
                continue
            relative_file_name = file.replace(file_ref.url, '')
            split_relative_file_name = relative_file_name.split('/')
            if len(split_relative_file_name) > 1:
                new_sub_dir = os.path.join(new_file, '/'.join(split_relative_file_name[:-1]))
                if not os.path.exists(new_sub_dir):
                    os.makedirs(new_sub_dir)
            new_sub_file = os.path.join(new_file, relative_file_name)
            os.symlink(file, new_sub_file)
    else:
        os.symlink(file_ref.url, new_file)


def create_sym_links(file_refs: List[FileRef], folder: str, data_type: Optional[str] = None):
    """
    Puts symbolic links to the files referenced by the fileref object into the designated folder. Only supported for
    linux.
    :param file_ref: A list of files to be referenced from another folder.
    :param folder: The folder into which the data shall be placed.
    :param data_type: The data type of the file refs. Will be determined if not given. It is assumed that all data is
    of the same data type.
    """
    if len(file_refs) == 0:
        return
    if data_type is None:
        data_type = get_valid_type(file_refs[0].url)
    for file_ref in file_refs:
        create_sym_link(file_ref, folder, data_type)
