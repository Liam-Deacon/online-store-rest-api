"""Module providing different gift list implemenations and a factory class.

Examples
--------
>>> from .gift_list import GiftListFactory
>>> gift_list = GiftListFactory('me')
>>> type(gift_list)
BasicGiftList

"""
import json
import sqlalchemy.exc

from typing import Any, Union, Dict, List, Iterable, Optional
from collections import defaultdict
from sqlalchemy.orm.query import Query
from loguru import logger

from .models.item import ItemModel
from .models.database import db
from .models.user import UserModel
from .models.gift import GiftListModel, GiftModel
from .utils.model_serialisers.json_encoder import AlchemyEncoder

from abc import ABC, abstractmethod


class AbstractGiftList(ABC):
    """Defines interface for implementations of gift lists to adhere to."""

    @abstractmethod
    def __init__(self, username_or_id) -> None:
        """Initialise gift list instance."""
        raise NotImplementedError

    @abstractmethod
    def get_user(self, username_or_id: Union[int, str]) -> Union[int, str]:
        """Get the user associated with `username_or_id`."""
        raise NotImplementedError

    @abstractmethod
    def create_list(self) -> object:
        """Create a new gift list."""
        raise NotImplementedError

    @abstractmethod
    def add_item(self, item):
        """Add item to gift list."""
        raise NotImplementedError

    @abstractmethod
    def remove_item(self, item):
        """Remove item from gift list."""
        raise NotImplementedError

    @abstractmethod
    def create_report(self):
        """Create a report of purchased and available items in gift list."""
        raise NotImplementedError

    @abstractmethod
    def get_list(self) -> Iterable[Any]:
        """Return the list of gifts..."""
        raise NotImplementedError

    @abstractmethod
    def purchase_item(self, *args, **kwargs):
        """Purchase gift item."""
        raise NotImplementedError


class BasicGiftList(AbstractGiftList):
    """A simple gift list implemenatation using Python's list class."""

    def __init__(self, username_or_id):
        self.user = self.get_user(username_or_id)
        self.gift_list = self.create_list()
        self._availability_map = defaultdict(lambda: 0, {})
        self._purchase_map = defaultdict(lambda: 0, {})

    def __repr__(self) -> str:
        """Create user friendly representation of gift list."""
        return f'{self.user} -> {self.get_list()}'

    def get_user(self, username_or_id: Union[int, str]) -> Union[int, str]:
        """Return user."""
        return username_or_id  # dummy method

    def create_list(self) -> List[Dict[str, Any]]:
        """Create a new gift list."""
        self.gift_list = []
        return self.gift_list

    def add_item(self, item: Dict[str, Any], quantity: int = 1):
        """
        Add item to gift list.

        Parameters
        ----------
        item: Dict[str, Any]
            A JSON compatible dictionary representation of item.

        Notes
        -----
        It is up to the user to correctly represent the item when adding.
        """
        if item not in self.gift_list:
            self.gift_list.append(item)
        self._availability_map[frozenset(item.items())] += quantity

    def remove_item(self, item: Dict[str, Any]):
        """Remove item from gift list.

        Warnings
        --------
        Does not consider availability or purchased totals when removing.
        """
        self.gift_list.remove(item)

    def create_report(self):
        """Print report of purchased and available gift items in list."""  
        available = []
        purchased = []
        for item in self.get_list():
            if isinstance(item, dict):
                hashable_item = frozenset(item.items())
                num_purchased = self._purchase_map[hashable_item]
                if num_purchased:
                    purchased.append((item, num_purchased))
                num_available = self._availability_map[hashable_item]
                if num_available:
                    available.append((item, num_available))
            else:
                # FIXME: force object to correct representation
                raise ValueError(f'item {item!r} must be a dict, '
                                 f'not {type(item)}')
        print(f'Gift List Report for {self.user}:')
        print("=" * 30)
        print('Purchased items:')
        if purchased:
            print('   - ' + '\n  - '.join(['{} (quantity: {})'.format(*item)
                                           for item in purchased]))
        print('-' * 30)
        print('Available items:')
        if available:
            print('  - ' + '\n  - '.join(['{} (quantity: {})'.format(*item)
                                          for item in available]))

    def get_list(self) -> List[Dict[str, Any]]:
        """Return the gift list."""
        return self.gift_list

    def purchase_item(self, gift: Dict[str, Any], quantity: int = 1):
        """Purchase gift item from gift list.

        Specifically, the number of available items is decreased
        by `quantity` and the number of purchased items is increased
        by `quantity`.

        Raises
        ------
        ValueError:
            If `gift` is not in gift list or quantity is greater than available
            number of desired gifts.
        """
        hashable_gift = frozenset(gift.items())
        available = self._availability_map[hashable_gift]
        if quantity > available:
            raise ValueError('Cannot purchase more items than available')

        self._purchase_map[hashable_gift] += quantity
        self._availability_map[hashable_gift] -= quantity


class SqlDatabaseGiftList(AbstractGiftList):
    """A gift list implementation using SQL ORM models."""
    def __init__(self, username_or_id):
        self.user = self.get_user(username_or_id)
        self.gift_list = (
            GiftListModel.query.filter_by(user_id=self._get_user_id()).first()
            or self.create_giftlist()
        )

    def _get_user_id(self) -> int:
        """Helper method to return a user id."""
        return getattr(self.get_user, 'id', -1)

    def get_user(self, username_or_id: Union[int, str]) -> UserModel:
        if isinstance(username_or_id, str):
            user = \
                UserModel.query.filter_by(username=username_or_id).first()
        else:
            user = \
                UserModel.query.filter_by(id=int(username_or_id or -1)).first()
        return user

    def create_list(self) -> GiftListModel:
        """Create a new gift list."""
        gift_list = GiftListModel(user_id=self._get_user_id())
        db.session.add(gift_list)
        db.session.commit()
        logger.info(f'Added {gift_list} to '
                    f'{GiftListModel.__tablename__} table')
        return gift_list

    def add_item(self, item) -> bool:
        """Add item to gift list with boolean indicating success."""
        successful = True

        def get(x: str, default: Optional[str] = None) -> object:
            """Helper for getting data from item in duck type fashion."""
            if isinstance(item, dict):
                return item.get(x, default)
            else:
                return getattr(item, x, default)

        try:
            item_id = get('item_id') or int(item)
            gift = GiftModel(item_id=item_id,
                             list_id=self.gift_list.id,
                             available=get('quantity', 1))
            db.session.add(gift)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as err:
            logger.exception(err)
            db.session.rollback()
            successful = False
        return successful

    def remove_item(self, item) -> bool:
        """Remove item from gift list with boolean result indicating success."""
        gift = GiftModel.query \
                        .filter_by(id=getattr(item, 'id', None) or int(item)) \
                        .first()
        if gift:
            db.session.delete(gift)
            db.session.commit()
            success = False
        else:
            success = True
        return success

    def purchase_item(self, gift: Union[int, GiftModel], quantity: int = 1):
        """Purchase the given `quantity` of `gift` item from gift list."""
        if isinstance(gift, int):
            gift = GiftModel(id=gift)
        item = ItemModel(id=gift.item_id)

        if quantity > gift.available:
            raise ValueError('quantity greater than available gift number')

        item.in_stock_quantity = item.in_stock_quantity or 10

        item.in_stock_quantity -= quantity
        gift.available -= quantity
        gift.purchased += quantity

        if item.in_stock_quantity < 0:
            db.session.rollback()
            raise ValueError('not enough stock of gift item')
        else:
            db.session.commit()

    def create_report(self) -> dict:
        """Create a report of purchased and available gift items in JSON 
        compatible representation.
        """
        available = []
        purchased = []
        for gift_orm in self.get_list():
            item_orm = ItemModel.query.filter_by(id=gift_orm.item_id).first()
            item_data = self.item_as_json(item_orm)
            if gift_orm.available > 0:
                data = data = item_data.copy()
                data['quantity'] = gift_orm.available
                available.append(data)
            if gift_orm.purchased > 0:
                data = data = item_data.copy()
                data['quantity'] = gift_orm.available
                purchased.append(data)
        return {
            'user': getattr(self.user, 'id'),
            'purchased': purchased,
            'available': available
        }

    def get_list(self) -> Query:
        """Return the gift list as an ORM query object."""
        return GiftModel.query.filter_by(list_id=self.gift_list.id)

    @classmethod
    def item_as_json(cls, item):
        """Helper method for encoding item into JSON compatible format."""
        return json.loads(json.dumps(item, cls=AlchemyEncoder))


class GiftListFactory:
    """A factory class for obtaining each user's gift list.

    Attributes
    ----------
    CLASSES: Dict[str, AbstractGiftList]
        A dictionary mapping shorthand string names to
        classes derived from AbstractGiftList.
        Default is to use BasicGiftList when key doesn't exist.
    GIFT_LISTS: Dict[Union[int, str], AbstractGiftList]
        A mapping between each user and their gift list.

    """

    CLASSES: Dict[str, AbstractGiftList] = \
        defaultdict(lambda: BasicGiftList, {
            'sql': SqlDatabaseGiftList
        })

    GIFT_LISTS: dict = {}

    def __new__(cls, user_name_or_id: Union[int, str],
                gift_list_cls: AbstractGiftList = BasicGiftList
                ) -> AbstractGiftList:
        """Get a gift list for the given user's name or id.

        Parameters
        ----------
        user_name_or_id: Union[int, str]
            The username or id.
        gift_list_cls: AbstractGiftList
            The gift list class to use.

        Returns
        -------
        AbstractGiftList
            An instance of `gift_list_cls` for the given `user_name_or_id`. 
        """
        if isinstance(gift_list_cls, str):
            gift_list_cls = cls.CLASSES[gift_list_cls]
        if user_name_or_id not in cls.GIFT_LISTS:
            cls.GIFT_LISTS[user_name_or_id] = gift_list_cls(user_name_or_id)
        return cls.GIFT_LISTS[user_name_or_id]
