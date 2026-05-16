# Guía paso a paso para depositar en Zenodo y obtener el DOI

Esta guía te lleva del paquete preparado al DOI activo. Tiempo estimado: 20–30 min.

---

## 1. Crear cuenta y vincular ORCID

1. Ir a https://zenodo.org y hacer login con GitHub o ORCID (recomendado: ORCID).
2. Si no tienes ORCID, créalo gratis en https://orcid.org y luego vincúlalo a Zenodo.
3. Asegúrate de que el ORCID del autor de correspondencia (Gleiston Cicerón Guerrero-Ulloa) esté activo y vinculado.

> **Importante:** asociar ORCID es lo que hace que Zenodo reconozca a los autores correctamente. Sin ORCID, el DOI funciona pero la atribución es manual y menos visible en buscadores académicos.

---

## 2. Iniciar el depósito

1. En Zenodo, hacer clic en **+ New Upload** (esquina superior derecha).
2. Subir el archivo **`RutAI_replication_package_v1.0.zip`** (280 MB).
   - Puedes subir también `RutAI_replication_package_v1.0_lite.zip` (474 KB) como archivo adicional, o crear un depósito separado para la versión lite.
3. Esperar a que la barra de progreso llegue al 100%. Con conexión razonable, son 5–10 minutos.

---

## 3. Llenar los metadatos

Usa los valores del archivo `zenodo_metadata.json` (incluido en `06_supplementary/` dentro del paquete) como guía. Los campos clave del formulario web son:

### Tipo de carga
- **Resource type:** Dataset

### Título
```
RutAI replication package: Geofence accuracy, bandit benchmark, TAM pilot, and deployment characterization in Quevedo, Ecuador
```

### Autores
1. Reyes Palacios, Luis Aaron — Universidad Técnica Estatal de Quevedo, Ecuador
2. Guerrero-Ulloa, Gleiston Cicerón — Universidad Técnica Estatal de Quevedo, Ecuador (ORCID: 0000-0003-0167-8480 — verificar el ORCID real del Dr. Guerrero antes de submitir)

### Descripción
Copiar el texto del campo `description` en `zenodo_metadata.json`. Es texto HTML enriquecido y Zenodo lo renderiza correctamente.

### Versión
`1.0`

### Fecha de publicación
`2026-05-05` (o la fecha del día en que hagas el depósito).

### Licencia
**Creative Commons Attribution 4.0 International (CC BY 4.0)**

### Comunidades
Sugerir las siguientes (no son obligatorias, pero ayudan a la visibilidad):
- `zenodo` (por defecto)
- Si la UTEQ tiene una comunidad propia en Zenodo, añadirla

### Identificadores relacionados
Por ahora dejar el campo `Related identifiers` vacío. Una vez aceptado el paper, se puede editar el depósito y añadir:
- **Relation:** *Is supplement to*
- **Identifier:** DOI del paper publicado
- **Resource type:** Publication / Article

### Palabras clave
Copiar las del JSON, una por línea:
```
geofencing
mobile sensing
multi-armed bandits
Thompson Sampling
technology acceptance model
TAM
urban mobility
Latin America
Ecuador
Android
location-based services
reproducibility
```

### Idioma
English

### Notas adicionales
> The TAM pilot dataset is anonymized; participants signed informed-consent forms held separately by the host institution. The Battery and Latency components include transparent disclosure of data-quality issues and infrastructure constraints in their respective CODEBOOK.md files; users are advised to read these before drawing quantitative conclusions from those components.

---

## 4. Asignar el DOI

Hay dos formas:

### Opción A — DOI reservado antes de publicar (recomendado)
1. Antes de pulsar "Publish", hacer clic en **"Reserve DOI"** en la barra superior del formulario.
2. Zenodo asigna inmediatamente un DOI con formato `10.5281/zenodo.XXXXXXX`.
3. Copiar ese DOI y reemplazarlo en:
   - El paper (sección "Data and code availability"): "A permanent DOI will be assigned upon acceptance via Zenodo" → cambiar por el DOI real.
   - `README.md` del paquete (línea de citación).
   - `LICENSE.txt` (línea de atribución).
   - `CITATION.cff` (no tiene DOI hardcoded, no requiere cambios).
4. Re-empaquetar el ZIP con esos archivos actualizados y reemplazarlo en Zenodo (mientras el depósito esté en estado "draft", se puede reemplazar libremente).
5. Publicar.

### Opción B — DOI tras publicar
1. Llenar metadatos sin reservar DOI.
2. Pulsar "Publish".
3. Zenodo asigna el DOI automáticamente y lo activa.
4. Si después quieres referenciarlo en archivos del paquete, se puede subir una versión `1.1` con los archivos actualizados — Zenodo mantendrá el historial.

> **Recomendación:** ir por **Opción A**. Es 10 minutos extra de trabajo pero deja el paquete autoconsistente desde el primer momento.

---

## 5. Verificar el depósito publicado

Una vez publicado:

1. Visitar la página del DOI: `https://doi.org/10.5281/zenodo.XXXXXXX`.
2. Verificar:
   - Que los archivos descarguen correctamente.
   - Que la descripción se vea completa y bien formateada.
   - Que aparezcan ambos autores.
   - Que la cita preformateada incluya el DOI.
3. Descargar el ZIP y ejecutar `sha256sum -c MANIFEST.txt` (después de extraerlo) para confirmar integridad.

---

## 6. Actualizar el paper

En el manuscrito, antes de re-submitir:

```
Sección 7 (Conclusions) y Declarations:
"A permanent DOI will be assigned upon acceptance via Zenodo"
                          ↓
"Data and code are publicly available at https://doi.org/10.5281/zenodo.XXXXXXX"
```

También actualizar la lista de referencias para citar el dataset:

```
[XX] L. A. Reyes Palacios, G. C. Guerrero-Ulloa, RutAI replication package
     (Version 1.0), Zenodo, 2026. doi:10.5281/zenodo.XXXXXXX.
```

---

## 7. Versionado posterior

Si tras revisión por pares hay que añadir o corregir datos:

1. Volver al depósito y pulsar **"New version"**.
2. Subir el ZIP corregido. Zenodo asigna un nuevo DOI con sufijo (`.X`) y mantiene el DOI principal apuntando siempre a la versión más reciente.
3. Documentar el cambio en `README.md` → sección "Version history" → añadir fila para la nueva versión.

---

## Checklist final antes de pulsar "Publish"

- [ ] ZIP cargado correctamente (verificar tamaño 280 MB)
- [ ] Título, autores y afiliación correctos
- [ ] Descripción copiada del JSON sin caracteres rotos
- [ ] Licencia: CC BY 4.0
- [ ] Tipo: Dataset
- [ ] DOI reservado y reemplazado en archivos internos del paquete (Opción A)
- [ ] Notas sobre datos anonimizados visibles
- [ ] ORCID del autor de correspondencia verificado
- [ ] Versión: 1.0
- [ ] Re-leer toda la descripción una vez antes de publicar — tras publicar, ciertos campos quedan inmutables

---

## Soporte

- Zenodo FAQ: https://help.zenodo.org
- Zenodo Sandbox (para probar antes): https://sandbox.zenodo.org
- Email Zenodo: info@zenodo.org

Si hay duda sobre un campo, mejor depositar en Sandbox primero (es idéntico pero los DOIs son de prueba, no se mantienen). Una vez confirmado que todo se ve bien, replicar en el Zenodo real.
