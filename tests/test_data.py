import os

import numpy as np
import numpy.testing as npt
import tensorflow as tf

from monty import data

TEST_FILE_PATH = 'resources/PBMC_test.csv'


def test_download_file_not_present(mocker):
    try:
        os.remove(TEST_FILE_PATH)
    except OSError:
        pass
    mocked_s3 = mocker.patch('s3fs.S3FileSystem.get')

    assert data.download_if_not_present(local_file_path=TEST_FILE_PATH) == TEST_FILE_PATH
    mocked_s3.assert_called_once_with('pbmcasinglecell/PBMC.csv', TEST_FILE_PATH)


def test_download_file_present(mocker):
    try:
        os.remove(TEST_FILE_PATH)
    except OSError:
        pass
    dataset = open(TEST_FILE_PATH, 'w')
    dataset.write(' ')
    mocked_s3 = mocker.patch('s3fs.S3FileSystem.get')

    assert data.download_if_not_present(local_file_path=TEST_FILE_PATH) == TEST_FILE_PATH
    assert mocked_s3.call_count == 0
    os.remove(TEST_FILE_PATH)


def test_create_dataset():
    sess = tf.Session()
    iterator = data.create_dataset("test_resources/PBMC_test.csv", 5, 1, 1, False, None).make_one_shot_iterator()
    first_batch = sess.run(iterator.get_next())

    assert first_batch.shape == (1, 5)
    npt.assert_array_equal(first_batch, np.array([[2, 1, 0, 1, 0]], dtype=np.float32))
