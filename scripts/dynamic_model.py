# pandas and numpy for data management
import numpy as np
from scipy.integrate import odeint

# import bokeh graphing libraries
from bokeh.plotting import figure
from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, TableColumn, DataTable, Select
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

# Make a tab with simulation of dynamic model of: 
# 1) water tank example
def dynamic_model_tab():

	# define tank model
	def water_tank(Level, time, c, valve):
		"""
		Calculate derivative of level of the tank
		valve : % valve open (0-100%)
		c : constant, relates valve opening to inlet flow. Set at 50.0 (kg/s / %opsen)
		"""
		rho = 1000.0 # water density kg/m3
		A = 1.0  # tank area in m2
		# calculate derivative of the level
		dLevel_dt = (c/(rho*A)) * valve
		return dLevel_dt
	
	def make_plot(src):
		# Blank plot with correct labels
		p_tank = figure(plot_width = 700, plot_height = 350, title = 'Water level in tank with time', x_axis_label = 'Time', y_axis_label = 'Tank Level', background_fill_color="#fafafa")
		p_tank.scatter('ts', 'z', color="indigo", source=src)
		p_valve = figure(plot_width = 700, plot_height = 350, title = 'Valve perc open with time', x_axis_label = 'Time', y_axis_label = 'Valve', background_fill_color="#fafafa")
		p_valve.line('ts', 'u', line_color="olivedrab", source=src)
		return p_valve, p_tank
		
	# timespan for simulation for 10 seconds, every 0.1 seconds
	ts = np.linspace(0, 10, 101)
	# valve operation
	c = 50.0          # valve coefficient (kg/s / %open)
	u = np.zeros(101) # u = valve % open
	u[21:70] = 100.0  # open valve between 2 and 7 seconds
	# level initial condition
	Level0 = 0
	# for storing the results
	z = np.zeros(101)
	# simulate with ODEINT
	for i in range(100):
		valve = u[i+1]
		y = odeint(water_tank, Level0,[0,0.1], args=(c,valve))
		Level0 = y[-1] # take the last point
		z[i+1] = Level0 # store the level for plotting

	data = {
		'ts' : ts,
		'z' : z,
		'u' : u
	}
	data_src = ColumnDataSource(data= data)
	valve_plot, tank_plot = make_plot(data_src)
	# Create a row layout
	layout = column(valve_plot, tank_plot)
	
	# Make a tab with the layout 
	tab = Panel(child=layout, title = 'Dynamic Model Beginning : Filling a water tank')

	return tab




