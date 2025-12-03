import os

import better_than_yesterday

if __name__ == '__main__':
    app_host = os.environ.get('HOST', '0.0.0.0')
    app_port = int(os.environ.get('PORT', 5000))
    system = better_than_yesterday.create_api()
    system.run(host=app_host, port=app_port)
