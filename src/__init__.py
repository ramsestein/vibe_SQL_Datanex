"""
Módulo para descargar y procesar la wiki de Datanex.
Versión 2.1: Output ligero sin diccionarios.
"""

from .download_wiki import download_wiki_pages, filter_useful_pages, download_linked_pages
from .extract_text import extract_text
from .unify_markdown import unify_markdowns
from .create_final_output import create_final_output

__all__ = ['download_wiki_pages', 'filter_useful_pages', 'download_linked_pages', 'extract_text', 'unify_markdowns', 'create_final_output']

