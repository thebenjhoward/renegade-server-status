import functools


def dict_property(yaml_path):
    """Simple decorator for mapping dictionary values that are expected to
    easy-to-use properties, which function like variables. The root of the
    data dict is expected to be 'self.data'

    Args:
        yaml_path (string): path through the the dictionary using '.' as the
        separator. Identical syntax to JSON objects or YAML
    """
    def decorator_dict_property(func):
        path = yaml_path.split('.')
        
        @functools.wraps(func)
        def prop_get(self):
            curr_data = self.data
            for index in path:
                curr_data = curr_data[index]
            return curr_data
        
        def prop_set(self, val):
            curr_data = self.data
            for index in path[:-1]:
                curr_data = curr_data[index]
            curr_data[path[-1]] = val

        def prop_del(self):
            curr_data = self.data
            for index in path[:-1]:
                curr_data = curr_data[index]
            del curr_data[path[-1]]
            
        return property(prop_get, prop_set, prop_del);
    return decorator_dict_property