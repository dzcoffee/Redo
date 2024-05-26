import logging

# 로그 포맷 설정
log_format = '[%(levelname)s %(asctime)s - %(filename)s:%(lineno)d line]: %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=log_format,
                    datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)