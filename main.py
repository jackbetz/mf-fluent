from ansys.fluent.core import examples
import os

import ansys.fluent.core as fluent

# Launch Fluent
solver = fluent.launch_fluent(
    product_version="latest",
    mode="solver",
    precision="single",
    processor_count=2,
)

# Import geometry (cylinder external flow case)
case_path = examples.download_file("cylinder_external_flow.cas.h5", "pyfluent/external_flow")
solver.file.read(file_name=case_path)

# Set up physics
solver.setup.models.viscous.model = "k-epsilon"

# Set boundary conditions
solver.setup.boundary_conditions.velocity_inlet["inlet"].velocity.value = 10  # m/s

# Initialize solution
solver.solution.initialization.initialize_flow_field()

# Set solution controls
solver.solution.run_calculation.iterate(iter_count=100)

# Get results
pressure = solver.solution.report_definitions.field_report.report_files()

print("Simulation complete!")
solver.exit()