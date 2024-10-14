import OpenOPC
opc = OpenOPC.client()
opc.servers('192.168.0.102')
opc.connect('OPCServer.WinCC.1', '192.168.0.102')
opc.info()
opc.read('FIR1_121_PV_act')
opc.close()
quit()