import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


import_file_name = examples.download_file('mixing_elbow.pmdb','pyfluent/mixing_elbow')
meshing = pyfluent.launch_fluent(mode="meshing",precision=pyfluent.Precision.SINGLE,processor_count=8)
wt = meshing.watertight()
wt.import_geometry.file_name.set_state(import_file_name)
wt.import_geometry.length_unit.set_state('in')
wt.import_geometry()

wt.add_local_sizing.add_child_to_task()
wt.add_local_sizing()

csm = wt.create_surface_mesh
csmc = csm.cfd_surface_mesh_controls
csmc.max_size.set_state(0.3)
wt.create_surface_mesh()

wt.describe_geometry.update_child_tasks(
setup_type_changed=False)
wt.describe_geometry.setup_type.set_state("The geometry consists of only fluid regions with no voids")
wt.describe_geometry.update_child_tasks(setup_type_changed=True)
wt.describe_geometry()

ub = wt.update_boundaries
ub.boundary_label_list.set_state(["wall-inlet"])
ub.boundary_label_type_list.set_state(["wall"])
ub.old_boundary_label_list.set_state(["wall-inlet"])
ub.old_boundary_label_type_list.set_state(["velocity-inlet"])
ub()

wt.update_regions()

wt.add_boundary_layer.add_child_to_task()
wt.add_boundary_layer.bl_control_name.set_state("smooth-transition_1")
wt.add_boundary_layer.insert_compound_child_task()
wt.add_boundary_layer_child_1()

wt.create_volume_mesh.volume_fill.set_state("poly-hexcore")
vfc = wt.create_volume_mesh.volume_fill_controls
vfc.hex_max_cell_length.set_state(0.3)
wt.create_volume_mesh()