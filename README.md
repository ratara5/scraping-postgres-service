Para probar solo cambios en main.py que pertenece al service: scraping_service del docker compose en scraping_project
```docker compose build scraping_service```
```docker compose up scraping_service```
Esto recrea el container scraping_service_v2
IMPORTANTE: Agregar al Dockerfile -> CMD [ "python", "main.py" ]