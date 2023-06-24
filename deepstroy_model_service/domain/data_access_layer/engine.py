import os
import warnings

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import exc

from deepstroy_model_service.domain.data_access_layer.build_connection_string import build_connection_string


def add_engine_pidguard(engine):
    """Add multiprocessing guards.

    Forces a connection to be reconnected if it is detected
    as having been shared to a sub-process.

    """

    # Called at the moment a particular DBAPI connection is first created for a given Pool.
    @event.listens_for(engine, 'connect')
    def connect(_, connection_record):
        connection_record.info['pid'] = os.getpid()

    # Called when a connection is retrieved from the Pool.
    @event.listens_for(engine, 'checkout')
    def checkout(_, connection_record, connection_proxy):
        pid = os.getpid()
        if connection_record.info['pid'] != pid:
            # substitute log.debug() or similar here as desired
            warnings.warn(
                f'Parent process {connection_record.info["pid"]}s forked ({pid}s) with an open '
                'database connection, '
                'which is being discarded and recreated.')
            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError(
                f'Connection record belongs to pid {connection_record.info["pid"]}, '
                f'attempting to check out in pid {pid}'
            )


app_db_engine = create_engine(
    build_connection_string(),
    isolation_level='READ COMMITTED',
    pool_pre_ping=True,
)
