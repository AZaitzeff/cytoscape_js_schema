# Cytoscape.js Schema
This repository provides a schema for the [javascript implementation of Cytoscape](https://js.cytoscape.org/#core/initialisation).

The schema follows the conventions of [JSON Schema](https://json-schema.org/).

Provided is python code that when ran outputs a JSON file of the schema. The JSON schema of the aforementioned function is also provided.

You can use the python dictionary or JSON to validate a JSON written for cytoscape initilization using [JSON validator tools](https://json-schema.org/implementations.html#validators). I personally like [python's jsonschema](https://github.com/Julian/jsonschema).

Most of the Cytoscape schema is implemented, however, it is currently not complete. Notably, keys whose values are functions are missing.
