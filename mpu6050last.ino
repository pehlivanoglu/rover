#include "Wire.h"
#include <MPU6050_light.h>
#include <ros.h>
//#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/String.h>
#include <string.h>

char msg[100];
char xmsg[10];
char ymsg[10];
char zmsg[10];


MPU6050 mpu(Wire);
ros::NodeHandle  nh;

long timer = 0;

std_msgs::String imu_msg;
ros::Publisher imu_pub("IMU_XYZ", &imu_msg);


void setup() {
  
  
  Wire.begin();
  byte status = mpu.begin();
  while(status!=0){ }
  delay(1000);
  //mpu.calcOffsets(); // gyro and accelero // offsets will be calculated manually
  nh.initNode();
  nh.advertise(imu_pub);
  
}

void loop() {

    mpu.update();

    dtostrf(mpu.getAngleX(), 4, 2, xmsg);
    dtostrf(mpu.getAngleY(), 4, 2, ymsg);
    dtostrf(mpu.getAngleZ(), 4, 2, zmsg);
    
    sprintf(msg, "%s %s %s",xmsg,ymsg,zmsg);
    
    imu_msg.data = msg;
    imu_pub.publish(&imu_msg);

    nh.spinOnce();

}
