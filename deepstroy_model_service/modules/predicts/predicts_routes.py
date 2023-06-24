import datetime
from http import HTTPStatus

from flask import Blueprint, jsonify

from deepstroy_model_service.modules.predicts.queries.get_forecasted_file import GetForecastedFileQuery

predict_blueprint = Blueprint('predict', __name__, url_prefix='/predict')


@predict_blueprint.route('/<int:file_id>', methods=['GET'])
def get_path_to_file_with_predicts(file_id):
    forecasted_file = GetForecastedFileQuery().by_id(file_id)

    if forecasted_file:
        return jsonify({
            "path": forecasted_file.path,
        }), HTTPStatus.OK
    else:
        return 'Doesnt exist', HTTPStatus.OK

    # file_bytes = request.get_data()
    # forecasting_file_entity = ForecastingFile(
    #                                         file_name=file_name,
    #                                         date_of_upload=datetime.datetime.utcnow(),
    #                                         path=create_path_for_file_forecasting()
    #                                     )
    # S3Helper().s3_upload_file(
    #     file_path_in_bucket=forecasting_file_entity.path,
    #     file_bytes=file_bytes,
    #     public=True,
    # )
    # id = NewForecastingFileCommand().create(forecasting_file_entity)
    # message_with_file_parameters = {
    #     'file_id': id,
    #     'path_to_file_in_s3': forecasting_file_entity.path,
    # }
    #
    # RabbitMqMessagePublisher().publish_message_to_exchange(exchange_name=rabbitmq_models_exchange_name,
    #                                                        message=message_with_file_parameters)

    return str(id), HTTPStatus.OK