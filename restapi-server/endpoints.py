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
# DESCRIPTION: API 엔드포인트에서 반환하는 응답 모델을 정의합니다.
# NOTE: 임시로 정의된 응답 모델입니다. 실제 데이터베이스와 연동하여 데이터를 가져올 때, 데이터베이스의 스키마에 맞게 수정해야 합니다.
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

@apis["v1"].post("/music/{id}/define", response_model=None, tags=["music", "define", "create"])
async def music_define_query(id: str) -> dict[str, any]:
    """
    ## CREATE: 음악 오브젝트를 생성합니다.
    
    ### Request
    - `path parameter`
        - `id`: 음악 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: MusicGeneralInfo
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `410`: HTTPException{"요청하신 음원을 생성할 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass

@apis["v1"].post("/music/{id}/info", response_model=MusicGeneralInfo, tags=["music", "info", "read"])
async def music_info_query(id: str) -> dict[str, any]:
    """
    ## READ: 데이터베이스에서 기본적인 음원정보를 조회합니다.
    
    ### Request
    - `path parameter`
        - `id`: 음악 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `200`: MusicGeneralInfo
        - `404`: HTTPException{"요청하신 음원을 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    # TODO: 음악 정보를 가져오는 코드를 작성하세요.
    pass

@apis["v1"].post("/music/{id}/modify", response_model=None, tags=["music", "modify", "update"])
async def music_modify_query(id: str) -> dict[str, any]:
    """
    ## UPDATE: 음악 오브젝트를 수정합니다.
    
    ### Request
    - `path parameter`
        - `id`: 음악 ID
    - `body`
        - `id`: 변경될 음악 ID, 선택사항입니다.
        - `title`: 변경될 음악 제목, 선택사항입니다.
        - `hls_endpoint`: 변경될 음악 HLS 엔드포인트, 선택사항입니다.
        - `artist`: 변경될 아티스트 정보, 선택사항입니다.
        - `album`: 변경될 앨범 정보, 선택사항입니다.
        
    ### Response
    
    - `status code` 상태 설명
        - `200`: MusicGeneralInfo
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 음원을 수정할 권한이 없습니다."}
        - `404`: HTTPException{"등록된 음원을 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
        
    """
    pass

@apis["v1"].post("/music/{id}/remove", tags=["music", "remove", "delete"])
async def music_remove_query(id: str) -> dict[str, any]:
    """
    ## DELETE: 음악 오브젝트를 삭제합니다.
    
    ### Request
    - `path parameter`
        - `id`: 음악 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: HTTPException{"요청하신 음원을 삭제했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 음원을 삭제할 권한이 없습니다."}
        - `404`: HTTPException{"요청하신 음원을 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass

# =============================================================================
# EOC: endpoints.py
# =============================================================================