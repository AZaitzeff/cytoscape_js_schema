# Cytoscape.js Schema
This repository provides a schema for the [javascript implementation of Cytoscape](https://js.cytoscape.org/#core/initialisation).

The schema follows the conventions of [JSON Schema](https://json-schema.org/).

Provided is python code that when ran outputs a JSON file of the schema and the JSON schema of the aforementioned function.

You can use the python dictionary to validate a json written for cytoscape using tools like [python's jsonschema](https://github.com/Julian/jsonschema) ([full list on JSON Schema](https://json-schema.org/implementations.html#validators)).

Most of the Cytoscape schema is implemented, however, it is currently not complete, notably, keys whose values are functions are missing.
