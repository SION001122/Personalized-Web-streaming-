# =============================================================================
# SPDX 가이드: https://reuse.software/spec/
# SPDX-FileCopyrightText: © 2024 bytecakelake <creator@bytecake.dev>
# SPDX-License-Identifier: AGPL-3.0 license
# =============================================================================

from time import time as nowtime
from sqlmodel import SQLModel, Field as F

class BlockTable(SQLModel, table=True):
    __tablename__ = 'block_table'
    block_key: str = F(default=None, primary_key=True)
    num_bytes: int = F(default=None)
    status_code: int = F(default=None)

class PartitionTable(SQLModel, table=True):
    __tablename__ = 'partition_table'
    partition_key: str = F(default=None, primary_key=True)
    block_key: str = F(default=None, foreign_key='block_table.block_key', index=True)
    status_code: int = F(default=None)

class AlbumTable(SQLModel, table=True):
    __tablename__ = 'album_table'
    album_id: str = F(default=None, primary_key=True)
    released_at: int = F(default_factory=lambda: int(nowtime()))
    title: str | None = F(default=None)
    artist_name: str | None = F(default=None)
    cover_block_key: str = F(default=None, foreign_key='block_table.block_key')

class MusicTable(SQLModel, table=True):
    __tablename__ = 'music_table'
    music_id: str = F(default=None, primary_key=True)
    album_id: str = F(default=None, foreign_key='album_table.album_id', index=True)
    title: str = F(default=None)
    length: int = F(default=None)

class StreamSequenceTable(SQLModel, table=True):
    __tablename__ = 'stream_sequence_table'
    sequence: int = F(default=None, primary_key=True)
    music_id: str = F(default=None, foreign_key='music_table.music_id', index=True)
    block_key: str = F(default=None, foreign_key='block_table.block_key')