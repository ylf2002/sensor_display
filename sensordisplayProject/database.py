import sqlite3

cx = sqlite3.connect("db.sqlite3")
cu=cx.cursor()

# cu.execute("SELECT * FROM sensor_temperature")
# print(cu.fetchall())

# cu.execute("DROP TABLE sensor_temperature")

# cu.execute("CREATE TABLE sensor_temperature(captime varchar(20),captemperature varchar(10))")
# cu.execute("CREATE TABLE sensor_temperature(id int PRIMARY KEY NOT NULL, captime varchar(20),captemperature varchar(10))")


# cu.execute("SELECT * FROM sensor_sensors")
# print(cu.fetchall())

# cu.execute('DELETE FROM sensor_sensors WHERE id>50')
# print(1)
cu.execute("SELECT * FROM sensor_sensors where id=782")
print(cu.fetchall())

