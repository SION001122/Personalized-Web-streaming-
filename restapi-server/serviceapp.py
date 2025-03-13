# =============================================================================
# SPDX 가이드: https://reuse.software/spec/
# SPDX-FileCopyrightText: © 2024 bytecakelake <creator@bytecake.dev>
# SPDX-License-Identifier: AGPL-3.0 license
# =============================================================================
# ++ 목차 ++
# 
# =============================================================================
# ++ 할일 목록 ++
# TODO: 목차를 완성하세요.
# =============================================================================
# TITLE: 모듈 실행 방지
# DESCRIPTION: 모듈을 커맨드 라인에서 실행하는것을 방지합니다.
if __name__ == "__main__": raise RuntimeError("이 스크립트는 직접 실행할 수 없습니다.")
# =============================================================================
# TITLE: 모듈 불러오기
# DESCRIPTION: FastAPI 모듈을 불러옵니다.
from fastapi import FastAPI 
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# =============================================================================
# TITLE: 서브패키지 불러오기
# DESCRIPTION: 이 앱의 서브패키지을 불러옵니다.
import endpoints
# =============================================================================
# TITLE: 서버 인스턴스 생성
# DESCRIPTION: FastAPI 서버 인스턴스를 생성합니다.
server = FastAPI(
    # INFO: API 제목
    title="Personal Music Streaming Service API",
    # INFO: API 설명
    description="This is a RESTful API for a personal music streaming service.",
    # INFO: 최신 API 버전 
    version="1.0.0"
)
# =============================================================================
# TITLE: 미들웨어 등록
# DESCRIPTION: 서버 인스턴스에 미들웨어를 추가합니다.
# TMI: 자동으로 비보안 HTTP 요청을 HTTPS로 변경합니다.
server.add_middleware(HTTPSRedirectMiddleware)
# TMI: gzip 압축알고리즘을 사용하여 트래픽을 최적화합니다. 또한 작은 크기(1KB)의 응답은 압축하면 오버헤드가 발생할수 있으므로 압축하지 않습니다.
server.add_middleware(GZipMiddleware, minimum_size=1024, compresslevel=9)
# =============================================================================
# TITLE: 엔드포인트 등록
# DESCRIPTION: 모든 엔드포인트를 순차적으로 등록합니다.
# TMI: API 버전별 엔드포인트를 등록합니다.
for api_version_tag, api_router in endpoints.apis.items():
    # INFO: API 버전에 따라 엔드포인트 기본경로는 /api/{버전} 형식으로 지정됩니다.
    server.include_router(api_router, prefix="/api/%s" % api_version_tag)
# =============================================================================
# EOC: serviceapp.py
# =============================================================================