-- SPDX 가이드: https://reuse.software/spec/
-- SPDX-FileCopyrightText: © 2024 bytecakelake <creator@bytecake.dev>
-- SPDX-License-Identifier: AGPL-3.0 license

-- DBMS: Sqlite3
-- Date: 2024-12-17
-- Version: 2.1.1

-- 외래 키 활성화
PRAGMA foreign_keys = ON;

-- 앨범 테이블
CREATE TABLE album_table (
    album_id TEXT PRIMARY KEY,
    released_at INTEGER, -- 타임스탬프 형식
    title TEXT NOT NULL, -- 앨범 제목
    length INTEGER, -- 음악의 개수
    artist_name TEXT, -- 아티스트 이름
    cover_block_key INTEGER, -- 외래 키
    FOREIGN KEY (cover_block_key) REFERENCES block_table (block_key)
);

-- 음악 테이블
CREATE TABLE music_table (
    music_id TEXT PRIMARY KEY, -- 음악 ID
    album_id TEXT NOT NULL, -- 외래 키
    title TEXT NOT NULL, -- 음악 제목
    length REAL, -- 음악의 길이(초)
    FOREIGN KEY (album_id) REFERENCES album_table (album_id)
);

-- 파일 블록 테이블
CREATE TABLE block_table (
    block_key INTEGER PRIMARY KEY,
    num_bytes INTEGER, -- 크기(바이트 단위)
    status_code INTEGER -- 상태 코드
);

-- 파티션 테이블
CREATE TABLE partition_table (
    partition_id TEXT PRIMARY KEY,
    block_key INTEGER NOT NULL, -- 외래 키
    status_code INTEGER, -- 상태 코드
    FOREIGN KEY (block_key) REFERENCES block_table (block_key)
);

-- 스트리밍 순서 테이블
CREATE TABLE stream_sequence_table (
    sequence INTEGER PRIMARY KEY AUTOINCREMENT, -- 순서 자동 증가
    music_id TEXT NOT NULL, -- 외래 키
    block_key INTEGER NOT NULL, -- 외래 키
    FOREIGN KEY (music_id) REFERENCES music_table (music_id),
    FOREIGN KEY (block_key) REFERENCES block_table (block_key)
);

-- 인덱스 생성
CREATE INDEX idx_music_album_id ON music_table(album_id); -- 앨범 ID로 인덱스 생성
CREATE INDEX idx_stream_music_id ON stream_sequence_table(music_id); -- 음악 ID로 인덱스 생성

