# markdown

Marker-converted Markdown version of the Yahboom course PDFs in [`../pdf-source/`](../pdf-source/). This is the corpus indexed by [`../sqlite-rag/`](../sqlite-rag/) and [`../lance-db-rag/`](../lance-db-rag/).

The conversion preserves headings, text, tables, and extracted figures well enough for retrieval, but it also contains PDF-conversion artifacts. Retrieval code handles those artifacts where needed; source documents are otherwise treated as fixed.

See [`convert.log`](convert.log) for the conversion run.
