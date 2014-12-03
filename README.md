OpenstackApplicationCatalogue
=============================

Application Catalogue for Openstack.  The application provides a visual catalogue for Heat templates.  This integrates into Horizon to provide easy 1 click deployment of services

Clone the repo
git clone https://github.com/davejohnston/OpenstackApplicationCatalogue.git

Copy the horizon panel into the project dashboard
cp -R OpenstackApplicationCatalogue/horizon/openstack_dashboard/dashboards/project /usr/share/openstack-dashboard/openstack_dashboard/dashboards/

cp -R OpenstackApplicationCatalogue/horizon/openstack_dashboard/static /usr/share/openstack-dashboard/

Copy the database to the catalogue directory
cp -R OpenstackApplicationCatalogue/catalogue /etc/

Update the project dashboard by adding 'applications' to the list of pannels under the Orchestration PanelGroup
/usr/share/openstack-dashboard/openstack_dashboard/dashboards/project/dashboard.py
  
*** 49,55 ****
  class OrchestrationPanels(horizon.PanelGroup):
      name = _("Orchestration")
      slug = "orchestration"
!     panels = ('stacks', 'applications')
  
  
  class DatabasePanels(horizon.PanelGroup):
--- 49,55 ----
  class OrchestrationPanels(horizon.PanelGroup):
      name = _("Orchestration")
      slug = "orchestration"
!     panels = ('stacks',)
  
  
  class DatabasePanels(horizon.PanelGroup):
  
  Restart httpd 
  service httpd restart


