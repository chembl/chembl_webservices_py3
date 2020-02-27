from pymongo import MongoClient



collection = client['ci_cache'][collection_name]


def check_have_docs(res_name):
    for doc in collection.find({"resource_name": res_name}):
        print('FOUND AT LEAST 1')
        return
    print('FOUND NONE')

def delete_res_name_cache(res_name):
    print('DELETING . . .')
    collection.delete_many({"resource_name": res_name})

resource_to_delete = 'drug'


check_have_docs(resource_to_delete)
delete_res_name_cache(resource_to_delete)
check_have_docs(resource_to_delete)
