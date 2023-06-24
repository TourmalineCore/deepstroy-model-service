from deepstroy_model_service.domain.data_access_layer.db import db


class ForecastedFile(db.Model):
    __tablename__ = 'forecasting_files'

    id = db.Column(db.BigInteger, primary_key=True)
    path = db.Column(db.String(2048), nullable=False)

    def __repr__(self):
        return f'<Forecast {self.id!r}  path: {self.path!r}>'
