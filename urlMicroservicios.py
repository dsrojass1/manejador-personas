import os

PATH_AUTH = "http://" + os.environ.get("VARIABLES_HOST", "localhost") + ":" + os.environ.get("VARIABLES_PORT", "8080") + "/api/registrar/"