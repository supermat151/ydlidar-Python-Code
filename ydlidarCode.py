import os
import ydlidar

if __name__ == "__main__":
    ydlidar.os_init();
    laser = ydlidar.CYdLidar();
    ports = ydlidar.lidarPortList();
    port = "/dev/ttyUSB0";
    for key, value in ports.items():
        port = value;
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port);
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200);
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TOF);
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL);
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0);
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 20);
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True);

    #This will initialize SDK and Lidar
    #Checks to see if: 
    #Serial port is not connected
    #Serial port does not have read and write permissions
    #Lidar Baud rate is set correctly for specific lidar
    #Incorrect lidar settings for specific lidar 
    ret = laser.initialize();
    
    #Check to see if ret condition is successful
    if ret:
        
        #This will turn on the lidar while it is true, will return false if:
        #Lidar stalls
        #Lidar power supply is unstable
        ret = laser.turnOn();
        
        #This will start scanning the lidar
        scan = ydlidar.LaserScan()
        
        #ydlidar.os_isok() allows for ctrl-c handling input. Will return false if:
        #it detects a ctrl-c input
        #if ydlidar.os_shutdown() is called upon from another part of the code
        while ret and ydlidar.os_isOk() :
            r = laser.doProcessSimple(scan);
            if r:
                print("Scan received[",scan.stamp,"]:",scan.points.size(),"ranges is [",1.0/scan.config.scan_time,"]Hz");
            else :
                print("Failed to get Lidar Data.")
        
        #Strp the device scanning thread and disable motor
        laser.turnOff();
    
    #Uninitialize the SDK and disconnect the lidar
    laser.disconnecting();
