# Import the basic framework components.
from softioc import softioc, builder
import cothread

PREFIX = "SISSY2EX:PWR00"
IP = "172.17.9.11"
# Set the record prefix
builder.SetDeviceName(PREFIX)
builder.SetBlocking(True)
update_rate = 0.5
# Define a class which represents a device
from easysnmp import Session

class SNMP_Power_Supply:

    def __init__(self,hostname):

        self._hostname = hostname
        self._session = self.get_session()


    def get_session(self):

        session = Session(hostname=self._hostname, community='private', version=2)
        return session
    
    def get_port_name(self, port_num):
                
        oid = 'iso.3.6.1.4.1.28507.30.1.3.1.2.1.2.' + str(port_num)
        description = self._session.get(oid)
        return str(description.value)
    
    def get_port_status(self, port_num):
                
        oid = 'iso.3.6.1.4.1.28507.30.1.3.1.2.1.3.' + str(port_num)
        description = self._session.get(oid)
        return int(description.value)
    
    def set_port_status(self, port_num,value):


        oid = 'iso.3.6.1.4.1.28507.30.1.3.1.2.1.3.' + str(port_num)
        snmp_type = 'INTEGER'
        response = self._session.set(oid,value,snmp_type)
        return response

   




# Connect to the device
pwr_dev = SNMP_Power_Supply(IP)


# Create the required records

records = {}
for channel in range(1,5):
    channel_name = "ch"+str(channel)
    pv_suffix = channel_name.upper()
    records[channel] = {}
    records[channel]["name"] = builder.stringIn(pv_suffix +':NAME')
    records[channel]["readback"] = builder.boolIn(pv_suffix +':RB',ZNAM="Off", ONAM="On")

records[1]["set"] = builder.boolOut('CH1:SP',ZNAM="Off", ONAM="On",always_update = True, on_update=lambda v: pwr_dev.set_port_status(1,v))
records[2]["set"] = builder.boolOut('CH2:SP',ZNAM="Off", ONAM="On",always_update = True,on_update=lambda v: pwr_dev.set_port_status(2,v))
records[3]["set"] = builder.boolOut('CH3:SP',ZNAM="Off", ONAM="On",always_update = True,on_update=lambda v: pwr_dev.set_port_status(3,v))
records[4]["set"] = builder.boolOut('CH4:SP',ZNAM="Off", ONAM="On",always_update = True,on_update=lambda v: pwr_dev.set_port_status(4,v))


# Boilerplate get the IOC started
builder.LoadDatabase()
softioc.iocInit()

# Start processes required to be run after iocInit
def update():
    while True:
        for channel_name, channel_pvs in records.items():
            num = int(channel_name)
            channel_pvs["name"].set(pwr_dev.get_port_name(num))
            channel_pvs["readback"].set(pwr_dev.get_port_status(num))
        cothread.Sleep(update_rate)


cothread.Spawn(update)

# Finally leave the IOC running with an interactive shell.
softioc.interactive_ioc(globals())