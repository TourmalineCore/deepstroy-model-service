import json

from deepstroy_model_service.helpers.s3_helper import S3Helper


class MessagePacker:
    def __init__(self):
        pass

    @staticmethod
    def unpack_the_message_body(message_body):
        message_str = message_body.decode('utf-8')
        message = json.loads(message_str)

        file_id = message["file_id"]
        file_bytes = S3Helper() \
            .s3_download_file(file_path_in_bucket=f'/{message["path"]}')

        return file_id, file_bytes
