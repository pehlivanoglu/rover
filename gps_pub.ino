#include <TinyGPS.h> //Arduino lib. for gps module
#include <ros.h> //ROS lib. for using arduino card as ros node
#include <std_msgs/String.h> // ROS message type library for communication


float lat, lon; //Longitude and latitude variable for storing data
TinyGPS gps; // create gps object



char msg[100];   //Message to be published
char msglat[15]; //Latitude msg
char msglng[15]; //Longitude msg

ros::NodeHandle nh;


std_msgs::String gps_msg; 
ros::Publisher gps_pub("gps_pub", &gps_msg);

void setup()
{

  Serial.begin(57600); // connect serial

  Serial1.begin(9600); // connect gps sensor

  nh.initNode();
  nh.advertise(gps_pub);

}

void loop()
{
  if (gps.encode(Serial1.read())) // encode gps data
  {
    gps.f_get_position(&lat, &lon); // get latitude and longitude

    dtostrf(lat, 15, 12, msglat); //formatting string latitude msg

    dtostrf(lon, 15, 12, msglng); //formatting string longitude msg

    sprintf(msg, "%s %s", msglat, msglng); //merging latitude and longitude data

    gps_msg.data = msg;

  } else { //If there is no signal, we dont need to publish data every iteration, we can wait for 1sec.
    delay(1000); 
    gps_msg.data = "No Signal";
  }
  gps_pub.publish(&gps_msg);
  nh.spinOnce();
    }
}
