import json
class JSONTypeComparator:
    def __init__(self, json1, json2):
        self.json1 = json1
        self.json2 = json2
        self.differences = []

    def compare_types(self, path="", obj1=None, obj2=None):
        if obj1 is None:
            obj1 = self.json1
        if obj2 is None:
            obj2 = self.json2

        if type(obj1) != type(obj2):
            self.differences.append(f"{path}: Different data types ({type(obj1)} vs {type(obj2)})")
            return

        if isinstance(obj1, dict):
            keys1 = set(obj1.keys())
            keys2 = set(obj2.keys())
            common_keys = keys1.intersection(keys2)

            for key in common_keys:
                self.compare_types(f"{path}.{key}", obj1[key], obj2[key])

            extra_keys1 = keys1 - keys2
            extra_keys2 = keys2 - keys1

            for key in extra_keys1:
                self.differences.append(f"{path}.{key}: Key only exists in JSON1")
            for key in extra_keys2:
                self.differences.append(f"{path}.{key}: Key only exists in JSON2")

        elif isinstance(obj1, list):
            if len(obj1) != len(obj2):
                self.differences.append(f"{path}: Different list lengths ({len(obj1)} vs {len(obj2)})")

            for i, (item1, item2) in enumerate(zip(obj1, obj2)):
                self.compare_types(f"{path}[{i}]", item1, item2)

    def get_differences(self):
        return self.differences


# 示例用法
json1 = json.loads('{"prefix": "88.529/adsfdffds", "version": "1.0.0", "industryCategory": "A", "industrySpecific": "01", "industryTrade": "011", "industrySubclass": "0111", "type": 1, "description": "English display ok", "items": [{"name": "", "idType": "", "idIndex": "3000", "metadata": {"type": "String", "minLength": 1, "maxLength": 10}, "required": false}, {"name": "", "idType": "99999", "idIndex": "3000", "metadata": {"type": "String", "minLength": 1, "maxLength": 10}, "required": true}]}')

json2 = {
    "prefix": "88.101.5",
    "version": "1.0.0",
    "industryCategory": "A",
    "industrySpecific": "01",
    "industryTrade": "011",
    "industrySubclass": "0111",
    "type": 1,
    "description": "测试模板",
    "items": [
        {
            "name": "e1",
            "idType": "ip",
            "idIndex": "2000",
            "metadata": {
                "type": "string",
                "minLength": 1,
                "maxLength": 10
            },
            "required": False
        }
    ]
    }


comparator = JSONTypeComparator(json1, json2)
comparator.compare_types()
differences = comparator.get_differences()

if differences:
    print("Differences found:")
    for diff in differences:
        print(diff)
else:
    print("No differences found.")
