from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class PowerBIWorkspaces(BaseSettings):
    licensees_1c: str = "167f58c8-304a-42e9-954a-f7ff905e5614"


class PowerBIDatasets(BaseSettings):
    licensees_1c: str = "5fff00f1-1f07-4cc2-99d1-ed4927053b76"


class PowerBITables(BaseSettings):
    licensees_1c: List[str] = [
        "Менеджеры",
        "Doc Товары-РеализацияТоваровУслуг",
        "Doc РеализацияТоваровУслуг",
        "Cat СоглашенияСКлиентами",
        "Cat Партнеры",
        "Cat Организации",
        "Cat Номенклатура",
        "Cat Валюты",
        "Doc ЗаказКлиента",
        "AR РасчетыСКлиентами",
        "Cat Бренды"
    ]


class PowerBIAPISettings(BaseSettings):
    """ Power BI для Riki

        == Создаем аппку ==
        Инструкция: https://www.sqlshack.com/how-to-access-power-bi-rest-apis-programmatically/

        1. Заходим на https://app.powerbi.com/embedsetup/
        2. Создаем приложение, называем его, даем ему нужные права, здесь только админ может

        https://portal.azure.com/ (Все действия в Azure Active Directory)
        1. App registration => All applications => выбираем свое
        2. Заходим в Authentication и ставим галочку на Access tokens (used for implicit flows) и Enable the following mobile and desktop flows => Сохраняем
        3. Заходим в API Permissions проверяем разрешения
        4. Заходим в Certificates & secrets и создаем New client secret
        5. Заходим в Overview и копируем Application (client) ID, Directory (tenant) ID

        == Разрешаем API в https://app.powerbi.com/admin-portal/
        Инструкция: https://learn.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal#step-3---enable-the-power-bi-service-admin-settings

        -- 1. В Groups создаем security group
        -- 2. Tenant settings -> Developer settings
        -- 3. Активируем Embed content in apps
        -- 4. Активируем Allow service principals to use Power BI APIs
        -- 5. В Specific security groups применяем настройки к ранее созданной security group

        https://app.powerbi.com/
        --1. Заходим в нужный Workspace -> Workspase access и добавляем название приложения, задаем роль

        == Python ==
        1. Устанавливаем пакет pip install msal -- Microsoft authentication library

        Справочник API: https://learn.microsoft.com/en-us/rest/api/power-bi/

    """
    app_name: str = ""
    app_id: str = ""
    secret_value: str = ""
    secret_id: str = ""
    tenant_id: str = ""
    user: str = ""
    password: str = ""
    authority_url: str = f"https://login.microsoftonline.com/{tenant_id}"
    scopes: List[str] = ["https://analysis.windows.net/powerbi/api/.default"]

    workspaces: PowerBIWorkspaces = PowerBIWorkspaces()

    datasets: PowerBIDatasets = PowerBIDatasets()

    tables: PowerBITables = PowerBITables()

    model_config = SettingsConfigDict(
        env_prefix="RIKI_POWERBI__"
    )
