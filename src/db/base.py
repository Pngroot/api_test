from sqlalchemy.orm import registry


Base = registry().generate_base()

