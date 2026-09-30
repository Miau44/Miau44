# Recursos del perfil

Los SVG se guardan en el repositorio: el README no necesita servicios externos para renderizar imágenes.

## Actualizar el banner

La foto original está en `assets/source/portrait.png`. Edita `YAML_ROWS` en `scripts/banner/generate.py` para cambiar la presentación.

```sh
python -m pip install -r scripts/banner/requirements.txt
python scripts/banner/generate.py
```

El generador crea las variantes clara y oscura del retrato vectorial y la animación de código y bases de datos. La preferencia de movimiento reducido muestra el retrato estático.

## Actualizar mapas y etiquetas

```sh
python scripts/profile_assets.py
```

Este script usa la biblioteca estándar de Python. Los mapas representan áreas y lenguajes del perfil; no son estadísticas de GitHub ni valoraciones de dominio.

La tarjeta de presentación se edita directamente en `assets/whoami-citypop.svg`. El texto alternativo y la información profesional están en `README.md`.

## Créditos

- Diseño, tarjeta city-pop y generador de partículas adaptados de [macu-dev/macu-dev](https://github.com/macu-dev/macu-dev).
- Foto: Mauricio Morales Fernandez, proporcionada para este perfil.
- Los archivos `assets/stack-*.svg` son copias de [Skill Icons](https://skillicons.dev), distribuidos bajo la [licencia MIT incluida](../assets/SKILL-ICONS-LICENSE).
- Los mapas, etiquetas y símbolos de código y bases de datos se generan localmente.
