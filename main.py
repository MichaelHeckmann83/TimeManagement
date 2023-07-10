import TimeManagement

me = TimeManagement.LabourTime.LabourTime.create_employee(data=True)
vis = TimeManagement.Visualizer.Visualizer.build_visualizer(me)
vis.show_table_pretty()
