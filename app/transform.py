import jsonschema

class SchemaTransformer:
    def __init__(self):
        self.input_schema = None
        self.output_schema = None
        self.mapping = None

    def set_schema(self, schema):
        self.input_schema = schema.get('input')
        self.output_schema = schema.get('output')
        self.mapping = schema.get('mapping')

    def transform(self, data):
        if self.input_schema:
            jsonschema.validate(data, self.input_schema)
        if self.mapping and self.output_schema:
            out = {k: data[v] for k, v in self.mapping.items() if v in data}
            jsonschema.validate(out, self.output_schema)
            return out
        return data
