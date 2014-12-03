from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.project import dashboard


class Mypanel(horizon.Panel):
    name = _("Application Catalogue")
    slug = "applications"


dashboard.Project.register(Mypanel)
