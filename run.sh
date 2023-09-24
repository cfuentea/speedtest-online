docker run --rm -w /tmp -v /home/soporte/speedtest-online:/tmp -h $(hostname) --dns 200.28.4.130 --dns 200.28.4.129 cfuentealba/speedtest:latest python3 prueba.py
