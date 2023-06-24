import io
import logging
from typing import TYPE_CHECKING, Optional

import boto3

from deepstroy_model_service.config import s3_config
from deepstroy_model_service.helpers.s3_paths import append_prefix, get_parent_path, create_folder_path, build_object_url

ACL_PRIVATE = 'private'
ACL_PUBLIC_READ = 'public-read'

if TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client
    from mypy_boto3_s3.service_resource import S3ServiceResource, Bucket
else:
    S3Client = object
    S3ServiceResource = object
    Bucket = object


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class S3Helper(metaclass=Singleton):
    def __init__(self):
        self.session = boto3.session.Session(
            aws_access_key_id=s3_config.s3_access_key_id,
            aws_secret_access_key=s3_config.s3_secret_access_key,
        )

    def get_client(self) -> S3Client:
        client: S3Client = self.session.client(
            's3',
            endpoint_url=s3_config.s3_endpoint,
            use_ssl=s3_config.s3_use_ssl
        )
        return client

    def get_resource(self) -> S3ServiceResource:
        resource: S3ServiceResource = self.session.resource(
            's3',
            endpoint_url=s3_config.s3_endpoint,
            use_ssl=s3_config.s3_use_ssl,
        )
        return resource

    @staticmethod
    def s3_get_full_file_url(
            file_path_in_bucket: str,
            s3_bucket_name: Optional[str] = s3_config.s3_bucket_name,
            s3_prefix: Optional[str] = s3_config.s3_prefix,
    ):
        result_path_in_bucket = append_prefix(path=file_path_in_bucket, prefix=s3_prefix)

        return build_object_url(
            endpoint_url=s3_config.s3_endpoint,
            bucket=s3_bucket_name,
            path=result_path_in_bucket,
        )

    def list_buckets(self):
        client = self.get_client()
        buckets_response = client.list_buckets()

        # check buckets list returned successfully
        if buckets_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            for s3_buckets in buckets_response['Buckets']:
                logging.debug(f' *** Bucket Name: {s3_buckets["Name"]} - Created on {s3_buckets["CreationDate"]} \n')
        else:
            logging.debug(' *** Failed while trying to get buckets list from your account')

        return buckets_response['Buckets']

    def s3_upload_file(
            self,
            file_path_in_bucket: str,
            file_bytes: bytes,
            s3_bucket_name: str = s3_config.s3_bucket_name,
            s3_prefix: Optional[str] = s3_config.s3_prefix,
            public: Optional[bool] = False,
            create_subdirs: Optional[bool] = False,
    ):
        bucket: Bucket = self.get_resource().Bucket(s3_bucket_name)
        result_path_in_bucket = append_prefix(path=file_path_in_bucket, prefix=s3_prefix)

        if create_subdirs:
            print(f'Create subdir: {get_parent_path(result_path_in_bucket)}')
            self._ensure_dir(get_parent_path(result_path_in_bucket))

        logging.warning(f'Started upload to bucket={s3_bucket_name} with key={result_path_in_bucket}')
        with io.BytesIO(file_bytes) as buffer:
            extra_args = {'ACL': ACL_PRIVATE if not public else ACL_PUBLIC_READ}
            bucket.upload_fileobj(Key=result_path_in_bucket,
                                  Fileobj=buffer,
                                  ExtraArgs=extra_args)

        logging.warning(f'File uploaded to bucket={s3_bucket_name} with key={result_path_in_bucket}')

        return result_path_in_bucket

    def s3_set_existed_object_acl(
            self,
            file_path_in_bucket: str,
            s3_bucket_name: str = s3_config.s3_bucket_name,
            s3_prefix: Optional[str] = s3_config.s3_prefix,
            public: Optional[bool] = False,
    ):
        resource: S3ServiceResource = self.get_resource()
        result_path_in_bucket = append_prefix(path=file_path_in_bucket, prefix=s3_prefix)

        object_acl = resource.ObjectAcl(s3_bucket_name, result_path_in_bucket)

        logging.warning(f'Started setting ACL to {ACL_PUBLIC_READ if public else ACL_PRIVATE} to object with'
                        f' key={result_path_in_bucket} in the bucket={s3_bucket_name}')
        if public:
            _ = object_acl.put(ACL=ACL_PUBLIC_READ)
        else:
            _ = object_acl.put(ACL=ACL_PRIVATE)

    def s3_create_folder(
            self,
            file_path_in_bucket: str,
            s3_bucket_name: str = s3_config.s3_bucket_name,
            s3_prefix: Optional[str] = s3_config.s3_prefix,
            is_path_absolute: bool = False,
            create_subdirs: bool = False,
    ):
        s3_resource = self.get_resource()
        bucket: Bucket = s3_resource.Bucket(s3_bucket_name)

        if is_path_absolute:
            file_path_in_bucket_with_prefix = file_path_in_bucket
        else:
            file_path_in_bucket_with_prefix = append_prefix(path=file_path_in_bucket, prefix=s3_prefix)

        result_folder_path_in_bucket = create_folder_path(path=file_path_in_bucket_with_prefix)

        if create_subdirs:
            self._ensure_dir(get_parent_path(result_folder_path_in_bucket))

        with io.BytesIO() as buffer:
            bucket.upload_fileobj(Key=result_folder_path_in_bucket, Fileobj=buffer, ExtraArgs={'ACL': 'private'})

        logging.warning(f'Folder created into bucket={s3_bucket_name} with key={result_folder_path_in_bucket}')

    def s3_download_file(
            self,
            file_path_in_bucket,
            s3_bucket_name: str = s3_config.s3_bucket_name,
            s3_prefix: Optional[str] = s3_config.s3_prefix,
    ) -> bytes:
        bucket: Bucket = self.get_resource().Bucket(s3_bucket_name)
        result_path_in_bucket = append_prefix(path=file_path_in_bucket, prefix=s3_prefix)
        print(result_path_in_bucket)
        with io.BytesIO() as buffer:
            bucket.download_fileobj(Key=result_path_in_bucket, Fileobj=buffer)
            result = buffer.getvalue()
        logging.warning(
            f'File downloaded from bucket={s3_bucket_name} with key={result_path_in_bucket} data[:10]={result[:min(10, len(result))]}')
        return result

    def s3_delete_file(
            self,
            file_path_in_bucket,
            s3_bucket_name: str = s3_config.s3_bucket_name,
            s3_prefix: Optional[str] = s3_config.s3_prefix,
    ):
        bucket: Bucket = self.get_resource().Bucket(s3_bucket_name)
        result_path_in_bucket = append_prefix(path=file_path_in_bucket, prefix=s3_prefix)

        bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': result_path_in_bucket,
                    },
                ],
            },
        )
        logging.warning(
            f'File deleted from bucket={s3_bucket_name} with key={result_path_in_bucket}')

    def _ensure_dir(self, path: str, s3_bucket_name: str = s3_config.s3_bucket_name):
        bucket: Bucket = self.get_resource().Bucket(s3_bucket_name)

        if path in ('', '/', '.'):
            return
        print(f'Prefix: {path}')
        print(len(list(bucket.objects.filter(Prefix=path))))

        if len(list(bucket.objects.filter(Prefix=path))) == 0:
            logging.debug(f'Want to create dir: {path}')
            self.s3_create_folder(file_path_in_bucket=path, is_path_absolute=True, create_subdirs=True)
