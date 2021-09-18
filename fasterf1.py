import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt

'''TODO:
*make time and speed work and add axis labels
*add dropdown to slloe for choosing year, circuit, drivers to compare
*add ability to toggle tpeed trace, braking trace, gear trace
*choose line colour
*add reactive titles
*enable zooming 
*learn about how cache works
'''

plotting.setup_mpl()

ff1.Cache.enable_cache('cache')  # optional but recommended

def get_fastest(driver, year, track, session):
    session = ff1.get_session(year, track, session)
    laps = session.load_laps(with_telemetry=True)

    fast_driver = laps.pick_driver(driver).pick_fastest()
    driver_car_data = fast_driver.get_car_data()

    return driver_car_data

'''
driver1 = 'RIC'
driver2 = 'NOR'


monza_quali = ff1.get_session(2021, 'Monza', 'Q')
laps = monza_quali.load_laps(with_telemetry=True)

fast_driver1 = laps.pick_driver(driver1).pick_fastest()
fast_driver2 = laps.pick_driver(driver2).pick_fastest()
driver1_car_data = fast_driver1.get_car_data()
driver2_car_data = fast_driver2.get_car_data()

fig, ax = plt.subplots()
ax.plot(driver1_car_data['Time'], driver1_car_data['Speed'], color='red')
ax.plot(driver2_car_data['Time'], driver2_car_data['Speed'], color='cyan')
ax.set_title(f'{driver1} vs {driver2}')
ax.set_xlabel('Time')
ax.set_ylabel("Speed [km/h]")
plt.show()
'''