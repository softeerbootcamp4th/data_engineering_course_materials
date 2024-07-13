from jupyter_server.auth import passwd

c = get_config()
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.open_browser = False
c.ServerApp.port = 8888
c.ServerApp.password = passwd('softeer@dlawork9888')
c.ServerApp.allow_origin = '*'
