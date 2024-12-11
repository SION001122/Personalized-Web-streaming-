# =============================================================================
# SPDX 가이드: https://reuse.software/spec/
# SPDX-FileCopyrightText: © 2024 bytecakelake <creator@bytecake.dev>
# SPDX-License-Identifier: AGPL-3.0 license
# =============================================================================
# ++ 목차 ++
# 
# =============================================================================
# ++ 할일 목록 ++
# TODO: 아직 미쳐 작성하지 못한 주석들을 작성하세요.
# TODO: 목차를 완성하세요.
# =============================================================================
import uvicorn
from serviceapp import server
from sys import argv

if len(argv) <= 1:
    print("사용법: python -m restapi-server run {--host [host]} {--port [port]}")

match argv[1]:
    case "run":
        # 메모: run 명령어는 서버를 실행합니다.

        match argv[2:]:
            case []:
                host = "0.0.0.0"
                port = 433
            case ["--host", host]:
                port = 433
            case ["--port", port]:
                host = "0.0.0.0"
            case ["--host", host, "--port", port]:
                pass
            case _:
                # 메모: 잘못된 인자가 입력되었을 때 종료합니다.
                raise "사용법: python -m restapi-server run {--host [host]} {--port [port]}"
                
        uvicorn.run(server, host=host, port=port)


