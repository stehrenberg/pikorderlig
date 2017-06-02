from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.install_dependencies")

default_task = ['install_dependencies']

@init
def initialize(project):
  project.set_property('dir_source_main_python', '/src')
  project.set_property('dir_install_logs', 'logs')
  init_dependencies(project)

def init_dependencies(project):
    project.build_depends_on('unicornhat')
    project.build_depends_on('sounddevice')
    project.build_depends_on('soundfile')
