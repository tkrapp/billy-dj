from typed_app_settings import typed_settings_dict

@typed_settings_dict(settings_attr="BILLY_CUSTOMER")
class Settings:
    INDEX_PAGE_SIZE: int = 20

settings = Settings()
