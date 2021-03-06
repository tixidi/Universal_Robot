/**
*
* @author Jayakrishnan HJ
* 
* @date May 2018
*
*/

#ifndef CROP_H
#define CROP_H

#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"

namespace perception {
class Cropper {
 public:
  Cropper();
  Cropper(const ros::Publisher& pub);
  void Callback(const sensor_msgs::PointCloud2& msg);

 private:
 ros::Publisher pub_;
};
}  // namespace perception

#endif
