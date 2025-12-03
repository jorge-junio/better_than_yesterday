from jjsystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, collection, routes=[]):
        super().__init__(collection, routes)

    @property
    def routes(self):
        settings_endpoint = '/settings'
        return super().routes + [
            {
                'action': 'Update settings do Tarefa',
                'method': 'PUT',
                'url': self.resource_url + settings_endpoint,
                'callback': 'update_settings'
            },
            {
                'action': 'Remove settings do Tarefa',
                'method': 'DELETE',
                'url': self.resource_url + settings_endpoint,
                'callback': 'remove_settings'
            },
            {
                'action': 'Busca uma key no json das settigns do Tarefa',
                'method': 'GET',
                'url': self.resource_url + settings_endpoint,
                'callback': 'get_settings_by_keys'
            }
        ]
