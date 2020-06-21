from project.data_access_layer import *

Base.metadata.create_all(engine, Base.metadata.tables['regusers'], checkfirst=True)
