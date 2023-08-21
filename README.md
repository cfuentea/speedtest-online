# speedtest-online
Script para mediciones básicas de velocidad, latencia, intermitencia (pérdida de paquetes), resolución de DNS.

### Ejecutar

```shell
docker run --rm -w /tmp -v $(pwd):/tmp -h $(hostname) cfuentealba/speedtest:latest python3 prueba.py
```


### Dockerhub
https://hub.docker.com/r/cfuentealba/speedtest/tags
