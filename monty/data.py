import logging
import os

import s3fs
import tensorflow as tf

logger = logging.getLogger(__name__)


def download_if_not_present(local_file_path):
    s3bucket = 'pbmcasinglecell/'
    key = 'PBMC.csv'

    if not os.path.isfile(local_file_path):
        logging.info('downloading dataset')
        s3 = s3fs.S3FileSystem(anon=True)
        s3.get(s3bucket + key, local_file_path)

    logger.info('done downloading dataset')
    return local_file_path


def create_dataset(csv_file, num_features, num_epochs, batch_size, shuffle, shuffle_buffer_size):
    dataset = tf.contrib.data.CsvDataset(csv_file,
                                         record_defaults=[tf.float32] * num_features,
                                         header=True,
                                         select_cols=list(range(1, num_features + 1)))
    if shuffle:
        dataset = dataset.shuffle(shuffle_buffer_size)

    return dataset \
        .repeat(num_epochs) \
        .batch(batch_size=batch_size, drop_remainder=True) \
        .map(lambda *x: tf.stack(x)) \
        .map(lambda x: tf.transpose(x))
