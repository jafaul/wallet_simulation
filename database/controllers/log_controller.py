from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session

from api.schemas import WalletNumberType
from api.constants import DATETIME_FORMAT
from database.models import TransferLog

from sqlalchemy.sql import false as sql_false


class LogController:
    def __init__(self, db: Session):
        self.db = db

    def _get_all_logs_by_wallet_number(self, wallet_number: WalletNumberType) -> list[Type[TransferLog]]:
        return self.db.query(TransferLog).filter(
            (TransferLog.receiver == wallet_number) | (TransferLog.sender == wallet_number)
        ).all()

    @staticmethod
    def _get_date_time_object(date_time: str):
        return datetime.strptime(date_time, DATETIME_FORMAT)

    @staticmethod
    def _get_from_to_as_date_time_objects(date_from: str, date_to: str) -> tuple[datetime, datetime]:
        date_from = LogController._get_date_time_object(date_from)
        date_to = LogController._get_date_time_object(date_to)
        return date_from, date_to

    def _get_logs_from_to_time(
            self,
            date_from: str,
            date_to: str
    ):
        date_from, date_to = LogController._get_from_to_as_date_time_objects(date_from=date_from, date_to=date_to)
        return self.db.query(TransferLog).filter(
            date_from < TransferLog.paid_on, TransferLog.paid_on  < date_to
        )

    def get_logs_using_operation_types(
            self,
            operation_types: list[str],
            wallet_number: WalletNumberType,
            date_from: str,
            date_to: str,
            data_limit: int|None = None
    ) -> list[Type[TransferLog]]:

        transfer_logs_filter = sql_false()
        if "in" in operation_types:
            transfer_logs_filter |= TransferLog.receiver == wallet_number
        if "out" in operation_types:
            transfer_logs_filter |= TransferLog.sender == wallet_number

        logs = self._get_logs_from_to_time(date_from=date_from, date_to=date_to)
        filtered_logs = logs.filter(transfer_logs_filter).order_by(
            TransferLog.paid_on.desc()
        )
        if data_limit:
            filtered_logs = filtered_logs.limit(data_limit)
        return filtered_logs.all()

