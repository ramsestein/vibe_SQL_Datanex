# Vibe SQL Copilot - DataNex

Este repositorio contiene el archivo `vibe_SQL_copilot.txt`, una base de conocimiento consolidada de la wiki de DataNex, optimizada para ser utilizada como contexto en asistentes de IA (LLMs) para generación de consultas SQL.

## 📋 ¿Qué contiene este archivo?

El archivo `vibe_SQL_copilot.txt` incluye:

1. **Prompt base**: Instrucciones para el asistente de IA sobre cómo generar consultas SQL
2. **Documentación de la wiki**: Contenido completo de las páginas útiles de la wiki de DataNex, incluyendo:
   - Estructura de todas las tablas (atributos, tipos de datos, claves)
   - Descripciones detalladas de cada campo
   - Relaciones entre tablas (foreign keys)
   - Valores posibles para campos codificados

## 🚀 Cómo usar este archivo

### Con Claude, ChatGPT u otros LLMs

1. **Copia el contenido completo** del archivo `vibe_SQL_copilot.txt`
2. **Pégalo al inicio de tu conversación** con el asistente de IA
3. **Haz tu pregunta** sobre consultas SQL o análisis de datos de DataNex

Ejemplo:
```
[Pegar contenido de vibe_SQL_copilot.txt]

Usuario: "Necesito una consulta SQL que me muestre todos los pacientes 
que tuvieron una cirugía en los últimos 6 meses"
```

### Con Cursor AI o similares

1. **Añade el archivo como contexto** usando `@vibe_SQL_copilot.txt`
2. El asistente tendrá acceso automático a toda la información
3. **Haz tus preguntas** directamente

### Con APIs de OpenAI, Anthropic, etc.

```python
# Ejemplo con OpenAI API
with open('vibe_SQL_copilot.txt', 'r', encoding='utf-8') as f:
    context = f.read()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": "Tu consulta SQL aquí"}
    ]
)
```

## 📊 Estructura del archivo

```
┌─────────────────────────────────────┐
│ PROMPT BASE                         │
│ (Instrucciones para el asistente)  │
├─────────────────────────────────────┤
│ DOCUMENTACIÓN DE LA WIKI            │
│ - Estructura de tablas              │
│ - Descripciones de campos           │
│ - Relaciones (foreign keys)         │
│ - Valores codificados               │
│ - Ejemplos de uso                   │
└─────────────────────────────────────┘
```

## ✅ Ventajas de este formato

### Tamaño optimizado
- El archivo tiene aproximadamente **~600 líneas**
- Ocupa alrededor de **~50-80 KB** de texto plano
- **Compatible con todos los LLMs**, incluyendo:
  - GPT-4: ✅ Sin problemas
  - Claude 3: ✅ Sin problemas
  - GPT-3.5: ✅ Sin problemas
  - Modelos locales: ✅ Sin problemas

### Sin necesidad de dividir
El archivo es lo suficientemente compacto para usarse completo en cualquier LLM moderno.

### Actualización
Este archivo se actualiza automáticamente mediante un pipeline que:
- Descarga las últimas páginas de la wiki de DataNex
- Filtra páginas según criterios de utilidad
- Extrae la documentación de estructura de tablas
- Genera el archivo final consolidado y compacto

## 🔄 Última actualización

El archivo se actualiza automáticamente cada vez que se ejecuta el pipeline de DataNex.

Para ver la fecha exacta de la última actualización, revisa la fecha del último commit en este repositorio.

## 📚 Más información

Para más detalles sobre el proyecto DataNex y el pipeline de generación:
- **Repositorio principal**: [pipeline_datanex](https://github.com/ramsestein/vibe_SQL_Datanex)
- **Wiki de DataNex**: [DataScope Wiki](https://gitlab.com/dsc-clinic/datascope/-/wikis/home)

## 📄 Licencia

Este contenido está basado en la documentación de DataNex/DataScope.

