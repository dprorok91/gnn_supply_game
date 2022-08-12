from pandas import DataFrame, Series
from pandas._typing import Axes, Dtype
from pandas import concat

from abc import ABC, abstractmethod

from typing import Dict, Any, NewType, Optional

InvColumn = NewType('InvColumn', str)
InvDataType = NewType('InvDataType', Any)


class AbstractInventory(ABC, DataFrame):
    """Implements template for Inventory classess.

    The AbstractInventory specifies the methods and method
    signatures that all inventories have to implement.

    Specific implementations of these methods is required in concrete
    inventories.

    Parameters
    ----------
    __inventory_data : DataFrame, the DataFrame containing all existaing
    inventory positions
    """
    PROD_ID = 'PROD_ID'
    VOLUMES = 'VOLUMES'
    CAPACITY = 'CAPACITY'

    ENFORCED_COLUMNS = [
        PROD_ID,
        VOLUMES,
        CAPACITY
    ]

    def __init__(self, data: InvDataType = None,
                 index: Optional[Axes] = None,
                 columns: Optional[Axes] = None,
                 dtype: Optional[Dtype] = None,
                 copy: Optional[bool] = None,
                 enforce_columns: bool = False) -> None:

        data = self._format_inventory_data(data=data)

        super().__init__(data=data, index=index, columns=columns,
                         dtype=dtype, copy=copy)

        if enforce_columns:
            self.__enforce_columns()

        self.__check_structure()

    def __enforce_columns(self):
        columns = self.columns
        enforced_cols = self.__class__.ENFORCED_COLUMNS
        missing_cols = set(enforced_cols)-set(columns)
        self[list(missing_cols)] = None

    def __check_structure(self) -> None:
        columns = self.columns
        enforced_columns = set(self.__class__.ENFORCED_COLUMNS)

        assert enforced_columns.issubset(columns), "Enforced columns are \
            not in inventory data"

    @abstractmethod
    def _format_inventory_data(self,
                               data: InvDataType) -> DataFrame:
        """Transforms inventory data used in intitiatin into
        DataFrame format"""

        return data

    def read_volume(self) -> Series:
        self.__check_structure()
        return self._read_volume()

    @abstractmethod
    def _read_volume(self) -> Series:
        pass

    def update_inventory(self, new_data: DataFrame) -> None:
        """Updates inventory data with the new data provided"""
        # TODO Test this function
        self.__check_structure()
        self.update(new_data)

    def add_product(self, new_product: Dict[InvColumn, float]) -> None:
        """Adds new product to the inventory"""
        # TODO Test this function
        self.__check_structure()
        self = concat(self, new_product)


class SimpleDFInventory(AbstractInventory):

    def _format_inventory_data(self,
                               data: InvDataType) -> DataFrame:
        return data

    def _read_volume(self) -> Series:
        return self[[self.__class__.PROD_ID, self.__class__.VOLUMES]]
