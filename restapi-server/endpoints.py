# =============================================================================
# SPDX 가이드: https://reuse.software/spec/
# SPDX-FileCopyrightText: © 2024 bytecakelake <creator@bytecake.dev>
# SPDX-License-Identifier: AGPL-3.0 license
# =============================================================================
# ++ 목차 ++
# 
# =============================================================================
# ++ 할일 목록 ++
# TODO: 버전 1의 모든 엔드포인트 기획 및 구성을 완료하세요.
# TODO: 아직 미쳐 작성하지 못한 주석들을 작성하세요.
# TODO: 목차를 완성하세요.
# TODO: sqlite3 데이터베이스의 데이터 아키텍처를 설계한 후, 할일 목록을 업데이트하세요.
# =============================================================================
# TITLE: 모듈 실행 방지
# DESCRIPTION: 모듈을 커맨드 라인에서 실행하는것을 방지합니다.
if __name__ == "__main__": raise RuntimeError("이 스크립트는 직접 실행할 수 없습니다.")
# =============================================================================
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
# =============================================================================
# TITLE: 버전별 API 라우터 정의

apis: dict[str, APIRouter] = { # 버전별 API 라우터 객체 [버전, API 라우터 인스턴스]
    "v1": APIRouter(
        default_response_class=ORJSONResponse
    ),
}
# =============================================================================
# TITLE: 응답 모델 정의
#
class ArtistSimpleInfo(BaseModel):
    profile_url: str
    name: str
#
class AlbumSimpleInfo(BaseModel):
    id: int
    title: str
    cover_url: str
#
class MusicGeneralInfo(BaseModel):
    id: int
    title: str
    hls_endpoint: str
    artist: ArtistSimpleInfo
    album: AlbumSimpleInfo
# =============================================================================
# TITLE: 엔드포인트 정의
#
# NOTE: 무분별한 크롤링을 방지하기 위해 GET 메서드를 지양하고 POST 메서드를 권장합니다.
#


## TITLE: 사용자 맞춤형 추천
## DESCRIPTION: 사용자의 선호도에 따라 추천 서비스을 제공합니다.


## TITLE: 쿼리 기능
## DESCRIPTION: 인덱스 검색 및 오브젝트 목록 조회 기능을 제공합니다.


## TITLE: 사용자 기능
## DESCRIPTION: 사용자의 생성, 조회, 수정, 삭제을 처리합니다.


## TITLE: 엘범 기능
## DESCRIPTION: (공식/사용자 커스텀)엘범 오브젝트의 생성, 조회, 수정, 삭제 기능을 제공합니다.


## TITLE: 아티스트 기능
## DESCRIPTION: 아티스트 오브젝트의 생성, 조회, 수정, 삭제 기능을 제공합니다.


## TITLE: 음악 기능
## DESCRIPTION: 음악 오브젝트의 생성, 조회, 수정, 삭제 기능을 제공합니다.


# =============================================================================
# EOC: endpoints.py
# =============================================================================