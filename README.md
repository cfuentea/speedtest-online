# speedtest-online
Script para mediciones básicas de velocidad, latencia, intermitencia (pérdida de paquetes), resolución de DNS.

### Ejecutar

```shell
docker run --rm -w /tmp -v $(pwd):/tmp -h $(hostname) --dns 200.28.4.130 --dns 200.28.4.129 cfuentealba/speedtest:latest python3 prueba.py
```

Usar test\_selenium.py para ejecutar test hacia beta.speedtest.net

### Dockerhub
https://hub.docker.com/r/cfuentealba/speedtest/tags
