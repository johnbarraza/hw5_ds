"""Local MCP server for datosabiertos.gob.pe interactions.

Persona 1 owns the implementation.
"""


def buscar_datasets(query: str):
    raise NotImplementedError("Persona 1: implement CKAN package_search.")


def obtener_detalle_dataset(dataset_id: str):
    raise NotImplementedError("Persona 1: implement CKAN package_show.")


def inspeccionar_esquema_csv(url_csv: str, max_rows: int = 10):
    raise NotImplementedError("Persona 1: inspect at most 10 rows.")


def consultar_datastore_filtrado(resource_id: str, sql_or_filters):
    raise NotImplementedError("Persona 1: implement filtered datastore query.")


def obtener_ultimas_actualizaciones(limit: int = 10):
    raise NotImplementedError("Persona 1: implement recent updates lookup.")


def listar_entidades_publicas():
    raise NotImplementedError("Persona 1: implement public entity listing.")
