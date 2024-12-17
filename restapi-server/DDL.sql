-- DBMS: Sqlite3
-- Date: 2024-12-17
-- Version: 1.0.0

CREATE TABLE "music_table" (
    "music_id" TEXT NOT NULL DEFAULT (hex(randomblob(16))) CHECK ("music_id" <> ''),
    "created_at" REAL NOT NULL DEFAULT (unixepoch('subsec')),
    "title" TEXT NOT NULL DEFAULT ('unknown'),
    "artist_id" TEXT NULL,
    "duration" REAL NOT NULL DEFAULT (0),
    "genre" TEXT  NULL,
    PRIMARY KEY ("music_id")
    FOREIGN KEY ("artist_id") REFERENCES "artist_table" ("artist_id")
);

CREATE TABLE "album_table" (
    "album_id" TEXT NOT NULL DEFAULT (hex(randomblob(16))) CHECK ("album_id" <> ''),
    "created_at" REAL NOT NULL DEFAULT (unixepoch('subsec')),
    "title" TEXT NULL,
    "artist_id" TEXT NULL,
    "length" INTEGER NOT NULL DEFAULT (0),
    PRIMARY KEY ("album_id")
    FOREIGN KEY ("artist_id") REFERENCES "artist_table" ("artist_id")
);

CREATE TABLE "artist_table" (
    "artist_id" TEXT NOT NULL DEFAULT (hex(randomblob(16))),
    "name" TEXT  NULL,
    PRIMARY KEY ("artist_id")
);

CREATE TABLE "playlist_table" (
    "album_id" TEXT NOT NULL,
    "music_id" TEXT NOT NULL,
    PRIMARY KEY ("album_id", "music_id"),
    FOREIGN KEY ("album_id") REFERENCES "album_table" ("album_id"),
    FOREIGN KEY ("music_id") REFERENCES "music_table" ("music_id")
);

CREATE TABLE "chunk_table" (
    "chunk_id" TEXT NOT NULL DEFAULT (hex(randomblob(16))),
    "chunk" BLOB  NULL CHECK (length("chunk") > 0),
    PRIMARY KEY ("chunk_id")
);

CREATE TABLE "music_chunk_index" (
    "chunk_id" TEXT  NOT NULL,
    "music_id" TEXT  NOT NULL,
    "start_time" REAL NOT NULL,
    "end_time" REAL NOT NULL,
    PRIMARY KEY ("chunk_id", "music_id"),
    FOREIGN KEY ("chunk_id") REFERENCES "chunk_table" ("chunk_id"),
    FOREIGN KEY ("music_id") REFERENCES "music_table" ("music_id")
);

CREATE TABLE "image_chunk_index" (
    "chunk_id" TEXT NOT NULL,
    "album_id" TEXT NOT NULL,
    PRIMARY KEY ("chunk_id", "album_id"),
    FOREIGN KEY ("chunk_id") REFERENCES "chunk_table" ("chunk_id"),
    FOREIGN KEY ("album_id") REFERENCES "album_table" ("album_id")
);