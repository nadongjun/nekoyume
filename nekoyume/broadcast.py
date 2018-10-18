import datetime
import os
from typing import Mapping, Optional
import urllib.parse

from requests import Response, post
from requests.exceptions import ConnectionError, Timeout
from sqlalchemy.orm.query import Query

from .block import Block
from .node import Node
from .orm import db


__all__ = (
    'BROADCAST_LIMIT',
    'POST_BLOCK_ENDPOINT',
    'POST_MOVE_ENDPOINT',
    'POST_NODE_ENDPOINT',
    'BlockBroadcaster',
    'MoveBroadcaster',
    'NodeBroadcaster',
)

BROADCAST_LIMIT = os.environ.get('BROADCAST_LIMIT', 100)
POST_BLOCK_ENDPOINT = '/blocks'
POST_MOVE_ENDPOINT = '/moves'
POST_NODE_ENDPOINT = '/nodes'


class Broadcaster:

    @classmethod
    def broadcast(
            cls,
            serialized: Mapping[str, object],
            sent_node: Optional[Node]=None,
            my_node: Optional[Node]=None,
    ):
        for node in filter_nodes(sent_node):
            try:
                cls._broadcast(
                    serialized=serialized,
                    sent_node=node,
                    my_node=my_node
                )
            except (ConnectionError, Timeout):
                continue
        db.session.commit()

    @classmethod
    def _broadcast(
            cls,
            serialized: Mapping[str, object],
            sent_node: Optional[Node]=None,
            my_node: Optional[Node]=None,
    ) -> None:
        raise NotImplementedError


class BlockBroadcaster(Broadcaster):

    @classmethod
    def _broadcast(
            cls,
            serialized: Mapping[str, object],
            sent_node: Optional[Node]=None,
            my_node: Optional[Node]=None,
    ):
        """
        It broadcast this block to every nodes you know.

        :param      serialized: serialized :class:`nekoyume.block.Block`.
                                that will be broadcasted.
        :param       sent_node: sent :class:`nekoyume.node.Node`.
                                this node ignore sent node.
        :param         my_node: my :class:`nekoyume.node.Node`.
                                received node ignore my node when they
                                broadcast received object.
        """
        url = urllib.parse.urljoin(sent_node.url, POST_BLOCK_ENDPOINT)
        res = broadcasting(url, serialized, sent_node, my_node)
        if res.status_code == 403:
            result = res.json()
            # 0 is Genesis block.
            block_id = result.get('block_id', 0)
            query = db.session.query(Block).filter(
                Block.id.between(block_id, serialized['id'])
            ).order_by(Block.id)
            offset = 0
            while True:
                sync_blocks = query[
                    offset:offset+BROADCAST_LIMIT
                ]
                # TODO bulk api
                for block in sync_blocks:
                    s = block.serialize(
                        use_bencode=False,
                        include_suffix=True,
                        include_moves=True,
                        include_hash=True
                    )
                    broadcasting(url, s)
                offset += BROADCAST_LIMIT
                if len(sync_blocks) < BROADCAST_LIMIT:
                    break


class MoveBroadcaster(Broadcaster):

    @classmethod
    def _broadcast(
            cls,
            serialized: Mapping[str, object],
            sent_node: Optional[Node]=None,
            my_node: Optional[Node]=None,
    ) -> None:
        """
        It broadcast this move to every nodes you know.

        :param      serialized: serialized :class:`nekoyume.move.Move`.
                                that will be broadcasted.
        :param       sent_node: sent :class:`nekoyume.node.Node`.
                                this node ignore sent node.
        :param         my_node: my :class:`nekoyume.node.Node`.
                                received node ignore my node when they
                                broadcast received object.
        """
        url = urllib.parse.urljoin(sent_node.url, POST_MOVE_ENDPOINT)
        broadcasting(url, serialized, sent_node, my_node)


class NodeBroadcaster(Broadcaster):

    @classmethod
    def _broadcast(
            cls,
            serialized: Mapping[str, str],
            sent_node: Optional[Node]=None,
            my_node: Optional[Node]=None,
    ) -> None:
        """
        It broadcast node to every nodes you know.

        :param      serialized: serialized :class:`nekoyume.node.Node`.
                                that will be broadcasted.
        :param       sent_node: sent :class:`nekoyume.node.Node`.
                                this node ignore sent node.
        :param         my_node: my :class:`nekoyume.node.Node`.
                                received node ignore my node when they
                                broadcast received object.
        """
        url = urllib.parse.urljoin(sent_node.url, POST_NODE_ENDPOINT)
        broadcasting(url, serialized, sent_node, my_node)


def filter_nodes(sent_node: Optional[Node]=None) -> Query:
    query = db.session.query(Node)
    if sent_node:
        query = query.filter(
            Node.url != sent_node.url
        )
    return query


def broadcasting(url: str, serialized: Mapping[str, object],
                 node: Optional[Node]=None,
                 sent_node: Optional[Node]=None) -> Response:
    if sent_node:
        serialized['sent_node'] = sent_node.url
    res = post(url, json=serialized, timeout=3)
    if node:
        node.last_connected_at = datetime.datetime.utcnow()
        db.session.add(node)
    return res
