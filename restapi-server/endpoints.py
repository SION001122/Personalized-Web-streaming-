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
# TODO: 요청 및 응답 모델을 재설계하세요.
# =============================================================================
# TITLE: 모듈 실행 방지
# DESCRIPTION: 모듈을 커맨드 라인에서 실행하는것을 방지합니다.
if __name__ == "__main__": raise RuntimeError("이 스크립트는 직접 실행할 수 없습니다.")
# =============================================================================
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlmodel import create_engine, Session, select, SQLModel
from pathlib import Path
import dbmodel as DA
from sqlalchemy.exc import NoResultFound, IntegrityError
# =============================================================================
# TITLE: 버전별 API 라우터 정의

apis: dict[str, APIRouter] = { # 버전별 API 라우터 객체 [버전, API 라우터 인스턴스]
    "v1": APIRouter(
        default_response_class=ORJSONResponse,
    ),
}
# =============================================================================
# db 조작 및 관리 클래스
class Database:
    path: Path = Path.home() / ".pws-restapi-server"
    name: str = "main_v1.db"
    def __init__(self):
        self.engine = self.create_engine()
    def new_session(self):
        return Session(self.engine)
    def create_engine(self):
        path = self.path / self.name
        if not path.exists():
            path.mkdir()
        return create_engine(f"sqlite:///{path}")

db = Database()
# =============================================================================
# TITLE: 응답 모델 정의
# DESCRIPTION: API 엔드포인트에서 반환하는 응답 모델을 정의합니다.
# NOTE: 임시로 정의된 응답 모델입니다. 
# TODO: 데이터 아키텍처 설계 후 수정이 필요합니다.
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

## =============================================================================
## TITLE: 사용자 맞춤형 추천
## DESCRIPTION: 사용자의 선호도에 따라 추천 서비스을 제공합니다.
## NOTE: 추후 버전에서 사용자 맞춤형 추천 서비스를 제공할 예정입니다.
# >> ignore-endpoints (/recommended/*/**) {

## ENDPOINT: /recommended/{id}/music
## DESCRIPTION: 사용자에게 추천할 음악을 제공합니다.

## ENDPOINT: /recommended/{id}/artist
## DESCRIPTION: 사용자에게 추천할 아티스트를 제공합니다.

## ENDPOINT: /recommended/{id}/album
## DESCRIPTION: 사용자에게 추천할 앨범을 제공합니다.

## } ignore-endpoints <<
## =============================================================================
## TITLE: 쿼리 기능
## DESCRIPTION: 인덱스 검색 및 오브젝트 목록 조회 기능을 제공합니다.
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/query/serach", response_model=None, tags=["query", "search", "read"])
async def query_search() -> dict[str, object]:
    """
    ## READ: 데이터베이스에서 검색어에 맞는 오브젝트 목록을 조회합니다.
    
    ### Request
    - `body`
        - `target-types`: 검색 대상, 기본값은 `all`입니다.
        - `target-keyword`: 검색어
        - `batch-size`: 한 번에 가져올 오브젝트의 개수, 기본값은 `10`입니다.
        - `offset`: 가져올 오브젝트의 시작 위치, 기본값은 `0`입니다.
        
    ### Response
    
    - `status code` 상태 설명
        - `200`: object[]
        - `201`: HTTPException{"검색 결과가 없습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////

## =============================================================================
## TITLE: 사용자 기능
## DESCRIPTION: 사용자의 인증, 생성, 조회, 수정, 삭제을 처리합니다.
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/user/{id}/auth/sso", response_model=None, tags=["user", "auth", "sso"])
async def user_auth_sso_query(id: str) -> dict[str, object]:
    """
    ## AUTH: 사용자를 SSO로 인증합니다.
    
    ### Request
    - `path parameter`
        - `id`: 사용자 ID
    - `body`
        - `token`: SSO 토큰
    
    ### Response
    
    - `status code` 상태 설명
        - `200`: object
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `401`: HTTPException{"인증에 실패했습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/user/{id}/auth/login", response_model=None, tags=["user", "auth", "login"])
async def user_auth_login_query(id: str) -> dict[str, object]:
    """
    ## AUTH: 사용자를 로그인합니다.
    
    ### Request
    - `path parameter`
        - `id`: 사용자 ID
    - `body`
        - `email`: 사용자 이메일
        - `password`: 사용자 비밀번호
    
    ### Response
    
    - `status code` 상태 설명
        - `200`: Cookie{"사용자 인증이 완료되었습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `401`: HTTPException{"인증에 실패했습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
        
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/user/{id}/define", response_model=None, tags=["user", "define", "create"])
async def user_define_query(id: str) -> dict[str, object]:
    """
    ## CREATE: 사용자 오브젝트를 생성합니다.
    
    ### Request
    - `path parameter`
        - `id`: 사용자 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: Message{"요청하신 사용자를 생성했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `410`: HTTPException{"요청하신 사용자를 생성할 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/user/{id}/info", response_model=None, tags=["user", "info", "read"])
async def user_info_query(id: str) -> dict[str, object]:
    """
    ## READ: 데이터베이스에서 사용자 정보를 조회합니다.
    
    ### Request
    - `path parameter`
        - `id`: 사용자 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `200`: object
        - `404`: HTTPException{"요청하신 사용자를 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/user/{id}/modify", response_model=None, tags=["user", "modify", "update"])
async def user_modify_query(id: str) -> dict[str, object]:
    """
    ## UPDATE: 사용자 오브젝트를 수정합니다.
    
    ### Request
    - `path parameter`
        - `id`: 사용자 ID
    - `body`
        - `id`: 변경될 사용자 ID, 선택사항입니다.
        - `name`: 변경될 사용자 이름, 선택사항입니다.
        - `email`: 변경될 사용자 이메일, 선택사항입니다.
        
    ### Response
    
    - `status code` 상태 설명
        - `200`: Message{"요청하신 사용자를 수정했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 사용자를 수정할 권한이 없습니다."}
        - `404`: HTTPException{"등록된 사용자를 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
        
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/user/{id}/remove", tags=["user", "remove", "delete"])
async def user_remove_query(id: str) -> dict[str, object]:
    """
    ## DELETE: 사용자 오브젝트를 삭제합니다.
    
    ### Request
    - `path parameter`
        - `id`: 사용자 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: Message{"요청하신 사용자를 삭제했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 사용자를 삭제할 권한이 없습니다."}
        - `404`: HTTPException{"요청하신 사용자를 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
## =============================================================================
## TITLE: 엘범 기능
## DESCRIPTION: (공식/사용자 커스텀)엘범 오브젝트의 생성, 조회, 수정, 삭제 기능을 제공합니다.
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/album/{id}/define", response_model=None, tags=["album", "define", "create"])
async def album_define_query(id: str) -> dict[str, object]:
    """
    ## CREATE: 앨범 오브젝트를 생성합니다.
    
    ### Request
    - `path parameter`
        - `id`: 앨범 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: Message{"요청하신 앨범을 생성했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `410`: HTTPException{"요청하신 앨범을 생성할 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/album/{id}/info", response_model=AlbumSimpleInfo, tags=["album", "info", "read"])
async def album_info_query(id: str) -> dict[str, object]:
    """
    ## READ: 데이터베이스에서 기본적인 앨범 정보를 조회합니다.
    
    ### Request
    - `path parameter`
        - `id`: 앨범 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `200`: AlbumSimpleInfo
        - `404`: HTTPException{"요청하신 앨범을 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/album/{id}/modify", response_model=None, tags=["album", "modify", "update"])
async def album_modify_query(id: str) -> dict[str, object]:
    """
    ## UPDATE: 앨범 오브젝트를 수정합니다.
    
    ### Request
    - `path parameter`
        - `id`: 앨범 ID
    - `body`
        - `id`: 변경될 앨범 ID, 선택사항입니다.
        - `title`: 변경될 앨범 제목, 선택사항입니다.
        - `cover_url`: 변경될 앨범 커버 URL, 선택사항입니다.
        
    ### Response
    
    - `status code` 상태 설명
        - `200`: Message{"요청하신 앨범을 수정했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 앨범을 수정할 권한이 없습니다."}
        - `404`: HTTPException{"등록된 앨범을 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
        
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/album/{id}/remove", tags=["album", "remove", "delete"])
async def album_remove_query(id: str) -> dict[str, object]:
    """
    ## DELETE: 앨범 오브젝트를 삭제합니다.
    
    ### Request
    - `path parameter`
        - `id`: 앨범 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: Message{"요청하신 앨범을 삭제했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 앨범을 삭제할 권한이 없습니다."}
        - `404`: HTTPException{"요청하신 앨범을 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
        
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
## =============================================================================
## TITLE: 아티스트 기능
## DESCRIPTION: 아티스트 오브젝트의 생성, 조회, 수정, 삭제 기능을 제공합니다.
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/artist/{id}/define", response_model=None, tags=["artist", "define", "create"])
async def artist_define_query(id: str) -> dict[str, object]:
    """
    ## CREATE: 아티스트 오브젝트를 생성합니다.
    
    ### Request
    - `path parameter`
        - `id`: 아티스트 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: Message{"요청하신 아티스트를 생성했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `410`: HTTPException{"요청하신 아티스트를 생성할 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/artist/{id}/info", response_model=ArtistSimpleInfo, tags=["artist", "info", "read"])
async def artist_info_query(id: str) -> dict[str, object]:
    """
    ## READ: 데이터베이스에서 기본적인 아티스트 정보를 조회합니다.
    
    ### Request
    - `path parameter`
        - `id`: 아티스트 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `200`: ArtistSimpleInfo
        - `404`: HTTPException{"요청하신 아티스트를 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/artist/{id}/modify", response_model=None, tags=["artist", "modify", "update"])
async def artist_modify_query(id: str) -> dict[str, object]:
    """
    ## UPDATE: 아티스트 오브젝트를 수정합니다.
    
    ### Request
    - `path parameter`
        - `id`: 아티스트 ID
    - `body`
        - `id`: 변경될 아티스트 ID, 선택사항입니다.
        - `name`: 변경될 아티스트 이름, 선택사항입니다.
        - `profile_url`: 변경될 아티스트 프로필 URL, 선택사항입니다.
        
    ### Response
    
    - `status code` 상태 설명
        - `200`: Message{"요청하신 아티스트를 수정했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 아티스트를 수정할 권한이 없습니다."}
        - `404`: HTTPException{"등록된 아티스트를 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
        
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/artist/{id}/remove", tags=["artist", "remove", "delete"])
async def artist_remove_query(id: str) -> dict[str, object]:
    """
    ## DELETE: 아티스트 오브젝트를 삭제합니다.
    
    ### Request
    - `path parameter`
        - `id`: 아티스트 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: Message{"요청하신 아티스트를 삭제했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 아티스트를 삭제할 권한이 없습니다."}
        - `404`: HTTPException{"요청하신 아티스트를 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    pass
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
## =============================================================================
## TITLE: 음악 기능
## DESCRIPTION: 음악 오브젝트의 생성, 조회, 수정, 삭제 기능을 제공합니다.
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////

class MusicDefineBody(BaseModel):
    title: str
    album_id: str | None = None
    length: int | None = None


@apis["v1"].post("/music/{id}/define", status_code=201, tags=["music", "define", "create"])
async def music_define_query(id: str, body: MusicDefineBody) -> dict[str, object]:
    """
    ## CREATE: 음악 오브젝트를 생성합니다.
    
    ### Request
    - `path parameter`
        - `id`: 음악 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: Message{"요청하신 음원을 생성했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `410`: HTTPException{"요청하신 음원을 생성할 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    try:
        with db.new_session() as session:
            session.add(DA.MusicTable(music_id=id, album_id=body.album_id, title=body.title, length=body.length))
            session.commit()
    except IntegrityError:
        raise HTTPException(status_code=410, detail="요청하신 음악은 이미 존재하는 음악입니다.")
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/music/{id}/info", tags=["music", "info", "read"])
async def music_info_query(id: str):
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
    with db.new_session() as session:
        try:
            music = session.exec(select(DA.MusicTable).where(DA.MusicTable.music_id == id)).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="요청하신 음악이 존재하지 않습니다.")
        return music
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/music/{id}/modify", response_model=None, tags=["music", "modify", "update"])
async def music_modify_query(id: str, body: MusicDefineBody) -> dict[str, object]:
    """
    ## UPDATE: 음악 오브젝트를 수정합니다.
    
    ### Request
    - `path parameter`
        - `id`: 음악 ID
    - `body`
        - `title`: 변경될 음악 제목, 선택사항입니다.
        - `album_id`: 변경될 앨범 아이디 정보, 선택사항입니다.
        - `length`: 변경될 음악 길이 정보, 선택사항입니다.
        
    ### Response
    
    - `status code` 상태 설명
        - `200`: Message{"요청하신 음원을 수정했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 음원을 수정할 권한이 없습니다."}
        - `404`: HTTPException{"등록된 음원을 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
        
    """
    with db.new_session() as session:
        try:
            music = session.exec(select(DA.MusicTable).where(DA.MusicTable.music_id == id)).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="요청하신 음악이 존재하지 않습니다.")
        if body.title != None:
            music.title = body.title
        if body.album_id != None:
            music.album_id = body.album_id
        if body.length != None:
            music.length = body.length
        session.add(music)
        session.commit()
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
@apis["v1"].post("/music/{id}/remove", status_code=201, tags=["music", "remove", "delete"])
async def music_remove_query(id: str) -> dict[str, object]:
    """
    ## DELETE: 음악 오브젝트를 삭제합니다.
    
    ### Request
    - `path parameter`
        - `id`: 음악 ID
    
    ### Response
    
    - `status code` 상태 설명
        - `201`: Message{"요청하신 음원을 삭제했습니다."}
        - `400`: HTTPException{"잘못된 요청입니다."}
        - `403`: HTTPException{"요청하신 음원을 삭제할 권한이 없습니다."}
        - `404`: HTTPException{"요청하신 음원을 찾을 수 없습니다."}
        - `500`: HTTPException{"비정규 오류가 발생하여 요청을 처리하는데 실패했습니다."}
    
    """
    with db.new_session() as session:
        try:
            music = session.exec(select(DA.MusicTable).where(DA.MusicTable.music_id == id)).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="요청하신 음악이 존재하지 않습니다.")
        session.delete(music)
        session.commit()
## ///////////////////////////////////////////////////////////////////////////////////////////////////////////
# =============================================================================
# EOC: endpoints.py
# =============================================================================