# import swagger_parser
#
# swagger_file = '/path/to/swagger/file.yaml'
#
# swagger = swagger_parser.load_file(swagger_file)
#
# swagger_dict = swagger.to_dict()
#
# print(swagger_dict['info']['title'])
#
#
# import yaml
# import json
#
# with open('swagger.yaml') as f:
#     swagger_dict = yaml.safe_load(f)
#
# info_dict = swagger_dict.get('info', {})
# paths_dict = swagger_dict.get('paths', {})
# definitions_dict = swagger_dict.get('definitions', {})
#
# info_obj = json_to_objects(('Info', json.dumps(info_dict)))
# paths_obj = json_to_objects(('Paths', json.dumps(paths_dict)))
# definitions_obj = json_to_objects(('Definitions', json.dumps(definitions_dict)))
#
# print(info_obj.to_dict())
# print(paths_obj.to_dict())
# print(definitions_obj.to_dict())