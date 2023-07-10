import TimeManagement

me = TimeManagement.LabourTime.LabourTime.create_employee()
vis = TimeManagement.Visualizer.Visualizer.build_visualizer(me)
vis.show_table_pretty()
