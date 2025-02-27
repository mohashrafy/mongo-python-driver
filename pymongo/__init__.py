# Copyright 2009-present MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python driver for MongoDB."""

from typing import ContextManager, Optional, Tuple, Union

ASCENDING = 1
"""Ascending sort order."""
DESCENDING = -1
"""Descending sort order."""

GEO2D = "2d"
"""Index specifier for a 2-dimensional `geospatial index`_.

.. _geospatial index: http://mongodb.com/docs/manual/core/2d/
"""

GEOSPHERE = "2dsphere"
"""Index specifier for a `spherical geospatial index`_.

.. versionadded:: 2.5

.. _spherical geospatial index: http://mongodb.com/docs/manual/core/2dsphere/
"""

HASHED = "hashed"
"""Index specifier for a `hashed index`_.

.. versionadded:: 2.5

.. _hashed index: http://mongodb.com/docs/manual/core/index-hashed/
"""

TEXT = "text"
"""Index specifier for a `text index`_.

.. seealso:: MongoDB's `Atlas Search
   <https://docs.atlas.mongodb.com/atlas-search/>`_ which offers more advanced
   text search functionality.

.. versionadded:: 2.7.1

.. _text index: http://mongodb.com/docs/manual/core/index-text/
"""

version_tuple: Tuple[Union[int, str], ...] = (4, 2, 0, ".dev2")


def get_version_string() -> str:
    if isinstance(version_tuple[-1], str):
        return ".".join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return ".".join(map(str, version_tuple))


__version__: str = get_version_string()
version = __version__

"""Current version of PyMongo."""

from pymongo import _csot
from pymongo.collection import ReturnDocument  # noqa: F401
from pymongo.common import (  # noqa: F401
    MAX_SUPPORTED_WIRE_VERSION,
    MIN_SUPPORTED_WIRE_VERSION,
)
from pymongo.cursor import CursorType  # noqa: F401
from pymongo.mongo_client import MongoClient  # noqa: F401
from pymongo.operations import (  # noqa: F401
    DeleteMany,
    DeleteOne,
    IndexModel,
    InsertOne,
    ReplaceOne,
    UpdateMany,
    UpdateOne,
)
from pymongo.read_preferences import ReadPreference  # noqa: F401
from pymongo.write_concern import WriteConcern  # noqa: F401


def has_c() -> bool:
    """Is the C extension installed?"""
    try:
        from pymongo import _cmessage  # type: ignore[attr-defined] # noqa: F401

        return True
    except ImportError:
        return False


def timeout(seconds: Optional[float]) -> ContextManager:
    """**(Provisional)** Apply the given timeout for a block of operations.

    .. note:: :func:`~pymongo.timeout` is currently provisional. Backwards
       incompatible changes may occur before becoming officially supported.

    Use :func:`~pymongo.timeout` in a with-statement::

      with pymongo.timeout(5):
          client.db.coll.insert_one({})
          client.db.coll2.insert_one({})

    When the with-statement is entered, a deadline is set for the entire
    block. When that deadline is exceeded, any blocking pymongo operation
    will raise a timeout exception. For example::

      try:
          with pymongo.timeout(5):
              client.db.coll.insert_one({})
              time.sleep(5)
              # The deadline has now expired, the next operation will raise
              # a timeout exception.
              client.db.coll2.insert_one({})
      except (ServerSelectionTimeoutError, ExecutionTimeout, WTimeoutError,
              NetworkTimeout) as exc:
          print(f"block timed out: {exc!r}")

    When nesting :func:`~pymongo.timeout`, the newly computed deadline is capped to at most
    the existing deadline. The deadline can only be shortened, not extended.
    When exiting the block, the previous deadline is restored::

      with pymongo.timeout(5):
          coll.find_one()  # Uses the 5 second deadline.
          with pymongo.timeout(3):
              coll.find_one() # Uses the 3 second deadline.
          coll.find_one()  # Uses the original 5 second deadline.
          with pymongo.timeout(10):
              coll.find_one()  # Still uses the original 5 second deadline.
          coll.find_one()  # Uses the original 5 second deadline.

    :Parameters:
      - `seconds`: A non-negative floating point number expressing seconds, or None.

    :Raises:
      - :py:class:`ValueError`: When `seconds` is negative.

    .. versionadded:: 4.2
    """
    if not isinstance(seconds, (int, float, type(None))):
        raise TypeError("timeout must be None, an int, or a float")
    if seconds and seconds < 0:
        raise ValueError("timeout cannot be negative")
    if seconds is not None:
        seconds = float(seconds)
    return _csot._TimeoutContext(seconds)
