import os

PATH_AUTH = "http://" + os.environ.get("VARIABLES_HOST", "10.128.0.8") + ":" + os.environ.get("VARIABLES_PORT", "8080") + "/api/registrar/"
