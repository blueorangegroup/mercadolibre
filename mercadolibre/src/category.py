
def get_main_categories(meli_site):
    return meli_site.get_with_token('/categories')


def get_category(meli, category_id):
    return meli.get_with_token('/categories/{}'.format(category_id))


class Category(object):

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id
        self.child_ids = []

    @staticmethod
    def get_main_categories_instances(meli_site):
        return [Category(category.get('name'), category.get('id'))
                for category in get_main_categories(meli_site).json()]

    @staticmethod
    def get_children_categories(meli, category_id):
        return [Category(category.get('name'), category.get('id'))
                for category in get_category(meli, category_id).json().get('children_categories', [])]
