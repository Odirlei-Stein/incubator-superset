import re
import superset.models.core as models

from .base import (
    api,
    BaseSupersetView,
    check_ownership,
    CsvResponse,
    data_payload_response,
    DeleteMixin,
    generate_download_headers,
    get_error_msg,
    get_user_roles,
    handle_api_exception,
    json_error_response,
    json_success,
    SupersetFilter,
    SupersetModelView,
)

from sqlalchemy import and_, or_, select
from superset import (
    app,
    appbuilder,
    cache,
    conf,
    dataframe,
    db,
    event_logger,
    get_feature_flags,
    is_feature_enabled,
    results_backend,
    results_backend_use_msgpack,
    security_manager,
    sql_lab,
    talisman,
    viz,
)
def get_current_tenant_id():
    regex = r"\_(\d+)$"
    result = re.findall(regex,security_manager.current_user.username)
    if len(result)>0:
        return result[0]
    return None

class TenantFilter(SupersetFilter):
    def apply(self, query, func):
        
        tenant_id = get_current_tenant_id()
        if tenant_id:
            # raise Exception(tenant_id)
            return query.filter(or_(self.model.tenant_id==tenant_id,self.model.tenant_id == None))
        
        return query
        # if security_manager.all_datasource_access():
        #     return query
        # perms = self.get_view_menus("datasource_access")
        # # TODO(bogdan): add `schema_access` support here
        # return query.filter(self.model.perm.in_(perms))

class TenantDashboardFilter(SupersetFilter):
    def apply(self, query, func):
        Dash = models.Dashboard
        tenant_id = get_current_tenant_id()
        if tenant_id:
            # raise Exception(tenant_id)
            query = query.filter(or_(Dash.tenant_id==tenant_id,Dash.tenant_id == None))
            # raise Exception(query)
        
        return query