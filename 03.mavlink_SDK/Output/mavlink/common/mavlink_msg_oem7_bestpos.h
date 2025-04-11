#pragma once
// MESSAGE OEM7_BESTPOS PACKING

#define MAVLINK_MSG_ID_OEM7_BESTPOS 50010


typedef struct __mavlink_oem7_bestpos_t {
 double lat; /*<  BESTPOS latitude (degrees)*/
 double lon; /*<  BESTPOS longitude (degrees)*/
 double hgt; /*<  BESTPOS height above mean sea level (meters)*/
 uint32_t sol_status; /*<  BESTPOS solution status*/
 uint32_t pos_type; /*<  BESTPOS position type*/
 float undulation; /*<  BESTPOS undulation - the relationship between the geoid and the ellipsoid(m) of the chosen datum*/
 uint32_t datum_id; /*<  BESTPOS Datum ID number, 61 = WGS84, 63 = User*/
 float lat_d; /*<  BESTPOS latitude standard deviation(m)*/
 float lon_d; /*<  BESTPOS longitude standard deviation(m)*/
 float hgt_d; /*<  BESTPOS height standard deviation(m)*/
 float diff_age; /*<  BESTPOS different age in seconds*/
 float sol_age; /*<  BESTPOS solution age in seconds*/
 char stn_id[4]; /*<  BESTPOS Station ID*/
 uint8_t solnSVs; /*<  BESTPOS Number of satellites used in solution*/
} mavlink_oem7_bestpos_t;

#define MAVLINK_MSG_ID_OEM7_BESTPOS_LEN 65
#define MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN 65
#define MAVLINK_MSG_ID_50010_LEN 65
#define MAVLINK_MSG_ID_50010_MIN_LEN 65

#define MAVLINK_MSG_ID_OEM7_BESTPOS_CRC 23
#define MAVLINK_MSG_ID_50010_CRC 23

#define MAVLINK_MSG_OEM7_BESTPOS_FIELD_STN_ID_LEN 4

#if MAVLINK_COMMAND_24BIT
#define MAVLINK_MESSAGE_INFO_OEM7_BESTPOS { \
    50010, \
    "OEM7_BESTPOS", \
    14, \
    {  { "sol_status", NULL, MAVLINK_TYPE_UINT32_T, 0, 24, offsetof(mavlink_oem7_bestpos_t, sol_status) }, \
         { "pos_type", NULL, MAVLINK_TYPE_UINT32_T, 0, 28, offsetof(mavlink_oem7_bestpos_t, pos_type) }, \
         { "lat", NULL, MAVLINK_TYPE_DOUBLE, 0, 0, offsetof(mavlink_oem7_bestpos_t, lat) }, \
         { "lon", NULL, MAVLINK_TYPE_DOUBLE, 0, 8, offsetof(mavlink_oem7_bestpos_t, lon) }, \
         { "hgt", NULL, MAVLINK_TYPE_DOUBLE, 0, 16, offsetof(mavlink_oem7_bestpos_t, hgt) }, \
         { "undulation", NULL, MAVLINK_TYPE_FLOAT, 0, 32, offsetof(mavlink_oem7_bestpos_t, undulation) }, \
         { "datum_id", NULL, MAVLINK_TYPE_UINT32_T, 0, 36, offsetof(mavlink_oem7_bestpos_t, datum_id) }, \
         { "lat_d", NULL, MAVLINK_TYPE_FLOAT, 0, 40, offsetof(mavlink_oem7_bestpos_t, lat_d) }, \
         { "lon_d", NULL, MAVLINK_TYPE_FLOAT, 0, 44, offsetof(mavlink_oem7_bestpos_t, lon_d) }, \
         { "hgt_d", NULL, MAVLINK_TYPE_FLOAT, 0, 48, offsetof(mavlink_oem7_bestpos_t, hgt_d) }, \
         { "stn_id", NULL, MAVLINK_TYPE_CHAR, 4, 60, offsetof(mavlink_oem7_bestpos_t, stn_id) }, \
         { "diff_age", NULL, MAVLINK_TYPE_FLOAT, 0, 52, offsetof(mavlink_oem7_bestpos_t, diff_age) }, \
         { "sol_age", NULL, MAVLINK_TYPE_FLOAT, 0, 56, offsetof(mavlink_oem7_bestpos_t, sol_age) }, \
         { "solnSVs", NULL, MAVLINK_TYPE_UINT8_T, 0, 64, offsetof(mavlink_oem7_bestpos_t, solnSVs) }, \
         } \
}
#else
#define MAVLINK_MESSAGE_INFO_OEM7_BESTPOS { \
    "OEM7_BESTPOS", \
    14, \
    {  { "sol_status", NULL, MAVLINK_TYPE_UINT32_T, 0, 24, offsetof(mavlink_oem7_bestpos_t, sol_status) }, \
         { "pos_type", NULL, MAVLINK_TYPE_UINT32_T, 0, 28, offsetof(mavlink_oem7_bestpos_t, pos_type) }, \
         { "lat", NULL, MAVLINK_TYPE_DOUBLE, 0, 0, offsetof(mavlink_oem7_bestpos_t, lat) }, \
         { "lon", NULL, MAVLINK_TYPE_DOUBLE, 0, 8, offsetof(mavlink_oem7_bestpos_t, lon) }, \
         { "hgt", NULL, MAVLINK_TYPE_DOUBLE, 0, 16, offsetof(mavlink_oem7_bestpos_t, hgt) }, \
         { "undulation", NULL, MAVLINK_TYPE_FLOAT, 0, 32, offsetof(mavlink_oem7_bestpos_t, undulation) }, \
         { "datum_id", NULL, MAVLINK_TYPE_UINT32_T, 0, 36, offsetof(mavlink_oem7_bestpos_t, datum_id) }, \
         { "lat_d", NULL, MAVLINK_TYPE_FLOAT, 0, 40, offsetof(mavlink_oem7_bestpos_t, lat_d) }, \
         { "lon_d", NULL, MAVLINK_TYPE_FLOAT, 0, 44, offsetof(mavlink_oem7_bestpos_t, lon_d) }, \
         { "hgt_d", NULL, MAVLINK_TYPE_FLOAT, 0, 48, offsetof(mavlink_oem7_bestpos_t, hgt_d) }, \
         { "stn_id", NULL, MAVLINK_TYPE_CHAR, 4, 60, offsetof(mavlink_oem7_bestpos_t, stn_id) }, \
         { "diff_age", NULL, MAVLINK_TYPE_FLOAT, 0, 52, offsetof(mavlink_oem7_bestpos_t, diff_age) }, \
         { "sol_age", NULL, MAVLINK_TYPE_FLOAT, 0, 56, offsetof(mavlink_oem7_bestpos_t, sol_age) }, \
         { "solnSVs", NULL, MAVLINK_TYPE_UINT8_T, 0, 64, offsetof(mavlink_oem7_bestpos_t, solnSVs) }, \
         } \
}
#endif

/**
 * @brief Pack a oem7_bestpos message
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param msg The MAVLink message to compress the data into
 *
 * @param sol_status  BESTPOS solution status
 * @param pos_type  BESTPOS position type
 * @param lat  BESTPOS latitude (degrees)
 * @param lon  BESTPOS longitude (degrees)
 * @param hgt  BESTPOS height above mean sea level (meters)
 * @param undulation  BESTPOS undulation - the relationship between the geoid and the ellipsoid(m) of the chosen datum
 * @param datum_id  BESTPOS Datum ID number, 61 = WGS84, 63 = User
 * @param lat_d  BESTPOS latitude standard deviation(m)
 * @param lon_d  BESTPOS longitude standard deviation(m)
 * @param hgt_d  BESTPOS height standard deviation(m)
 * @param stn_id  BESTPOS Station ID
 * @param diff_age  BESTPOS different age in seconds
 * @param sol_age  BESTPOS solution age in seconds
 * @param solnSVs  BESTPOS Number of satellites used in solution
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_bestpos_pack(uint8_t system_id, uint8_t component_id, mavlink_message_t* msg,
                               uint32_t sol_status, uint32_t pos_type, double lat, double lon, double hgt, float undulation, uint32_t datum_id, float lat_d, float lon_d, float hgt_d, const char *stn_id, float diff_age, float sol_age, uint8_t solnSVs)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_BESTPOS_LEN];
    _mav_put_double(buf, 0, lat);
    _mav_put_double(buf, 8, lon);
    _mav_put_double(buf, 16, hgt);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, pos_type);
    _mav_put_float(buf, 32, undulation);
    _mav_put_uint32_t(buf, 36, datum_id);
    _mav_put_float(buf, 40, lat_d);
    _mav_put_float(buf, 44, lon_d);
    _mav_put_float(buf, 48, hgt_d);
    _mav_put_float(buf, 52, diff_age);
    _mav_put_float(buf, 56, sol_age);
    _mav_put_uint8_t(buf, 64, solnSVs);
    _mav_put_char_array(buf, 60, stn_id, 4);
        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN);
#else
    mavlink_oem7_bestpos_t packet;
    packet.lat = lat;
    packet.lon = lon;
    packet.hgt = hgt;
    packet.sol_status = sol_status;
    packet.pos_type = pos_type;
    packet.undulation = undulation;
    packet.datum_id = datum_id;
    packet.lat_d = lat_d;
    packet.lon_d = lon_d;
    packet.hgt_d = hgt_d;
    packet.diff_age = diff_age;
    packet.sol_age = sol_age;
    packet.solnSVs = solnSVs;
    mav_array_memcpy(packet.stn_id, stn_id, sizeof(char)*4);
        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_BESTPOS;
    return mavlink_finalize_message(msg, system_id, component_id, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_CRC);
}

/**
 * @brief Pack a oem7_bestpos message
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param status MAVLink status structure
 * @param msg The MAVLink message to compress the data into
 *
 * @param sol_status  BESTPOS solution status
 * @param pos_type  BESTPOS position type
 * @param lat  BESTPOS latitude (degrees)
 * @param lon  BESTPOS longitude (degrees)
 * @param hgt  BESTPOS height above mean sea level (meters)
 * @param undulation  BESTPOS undulation - the relationship between the geoid and the ellipsoid(m) of the chosen datum
 * @param datum_id  BESTPOS Datum ID number, 61 = WGS84, 63 = User
 * @param lat_d  BESTPOS latitude standard deviation(m)
 * @param lon_d  BESTPOS longitude standard deviation(m)
 * @param hgt_d  BESTPOS height standard deviation(m)
 * @param stn_id  BESTPOS Station ID
 * @param diff_age  BESTPOS different age in seconds
 * @param sol_age  BESTPOS solution age in seconds
 * @param solnSVs  BESTPOS Number of satellites used in solution
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_bestpos_pack_status(uint8_t system_id, uint8_t component_id, mavlink_status_t *_status, mavlink_message_t* msg,
                               uint32_t sol_status, uint32_t pos_type, double lat, double lon, double hgt, float undulation, uint32_t datum_id, float lat_d, float lon_d, float hgt_d, const char *stn_id, float diff_age, float sol_age, uint8_t solnSVs)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_BESTPOS_LEN];
    _mav_put_double(buf, 0, lat);
    _mav_put_double(buf, 8, lon);
    _mav_put_double(buf, 16, hgt);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, pos_type);
    _mav_put_float(buf, 32, undulation);
    _mav_put_uint32_t(buf, 36, datum_id);
    _mav_put_float(buf, 40, lat_d);
    _mav_put_float(buf, 44, lon_d);
    _mav_put_float(buf, 48, hgt_d);
    _mav_put_float(buf, 52, diff_age);
    _mav_put_float(buf, 56, sol_age);
    _mav_put_uint8_t(buf, 64, solnSVs);
    _mav_put_char_array(buf, 60, stn_id, 4);
        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN);
#else
    mavlink_oem7_bestpos_t packet;
    packet.lat = lat;
    packet.lon = lon;
    packet.hgt = hgt;
    packet.sol_status = sol_status;
    packet.pos_type = pos_type;
    packet.undulation = undulation;
    packet.datum_id = datum_id;
    packet.lat_d = lat_d;
    packet.lon_d = lon_d;
    packet.hgt_d = hgt_d;
    packet.diff_age = diff_age;
    packet.sol_age = sol_age;
    packet.solnSVs = solnSVs;
    mav_array_memcpy(packet.stn_id, stn_id, sizeof(char)*4);
        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_BESTPOS;
#if MAVLINK_CRC_EXTRA
    return mavlink_finalize_message_buffer(msg, system_id, component_id, _status, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_CRC);
#else
    return mavlink_finalize_message_buffer(msg, system_id, component_id, _status, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN);
#endif
}

/**
 * @brief Pack a oem7_bestpos message on a channel
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param chan The MAVLink channel this message will be sent over
 * @param msg The MAVLink message to compress the data into
 * @param sol_status  BESTPOS solution status
 * @param pos_type  BESTPOS position type
 * @param lat  BESTPOS latitude (degrees)
 * @param lon  BESTPOS longitude (degrees)
 * @param hgt  BESTPOS height above mean sea level (meters)
 * @param undulation  BESTPOS undulation - the relationship between the geoid and the ellipsoid(m) of the chosen datum
 * @param datum_id  BESTPOS Datum ID number, 61 = WGS84, 63 = User
 * @param lat_d  BESTPOS latitude standard deviation(m)
 * @param lon_d  BESTPOS longitude standard deviation(m)
 * @param hgt_d  BESTPOS height standard deviation(m)
 * @param stn_id  BESTPOS Station ID
 * @param diff_age  BESTPOS different age in seconds
 * @param sol_age  BESTPOS solution age in seconds
 * @param solnSVs  BESTPOS Number of satellites used in solution
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_bestpos_pack_chan(uint8_t system_id, uint8_t component_id, uint8_t chan,
                               mavlink_message_t* msg,
                                   uint32_t sol_status,uint32_t pos_type,double lat,double lon,double hgt,float undulation,uint32_t datum_id,float lat_d,float lon_d,float hgt_d,const char *stn_id,float diff_age,float sol_age,uint8_t solnSVs)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_BESTPOS_LEN];
    _mav_put_double(buf, 0, lat);
    _mav_put_double(buf, 8, lon);
    _mav_put_double(buf, 16, hgt);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, pos_type);
    _mav_put_float(buf, 32, undulation);
    _mav_put_uint32_t(buf, 36, datum_id);
    _mav_put_float(buf, 40, lat_d);
    _mav_put_float(buf, 44, lon_d);
    _mav_put_float(buf, 48, hgt_d);
    _mav_put_float(buf, 52, diff_age);
    _mav_put_float(buf, 56, sol_age);
    _mav_put_uint8_t(buf, 64, solnSVs);
    _mav_put_char_array(buf, 60, stn_id, 4);
        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN);
#else
    mavlink_oem7_bestpos_t packet;
    packet.lat = lat;
    packet.lon = lon;
    packet.hgt = hgt;
    packet.sol_status = sol_status;
    packet.pos_type = pos_type;
    packet.undulation = undulation;
    packet.datum_id = datum_id;
    packet.lat_d = lat_d;
    packet.lon_d = lon_d;
    packet.hgt_d = hgt_d;
    packet.diff_age = diff_age;
    packet.sol_age = sol_age;
    packet.solnSVs = solnSVs;
    mav_array_memcpy(packet.stn_id, stn_id, sizeof(char)*4);
        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_BESTPOS;
    return mavlink_finalize_message_chan(msg, system_id, component_id, chan, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_CRC);
}

/**
 * @brief Encode a oem7_bestpos struct
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param msg The MAVLink message to compress the data into
 * @param oem7_bestpos C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_bestpos_encode(uint8_t system_id, uint8_t component_id, mavlink_message_t* msg, const mavlink_oem7_bestpos_t* oem7_bestpos)
{
    return mavlink_msg_oem7_bestpos_pack(system_id, component_id, msg, oem7_bestpos->sol_status, oem7_bestpos->pos_type, oem7_bestpos->lat, oem7_bestpos->lon, oem7_bestpos->hgt, oem7_bestpos->undulation, oem7_bestpos->datum_id, oem7_bestpos->lat_d, oem7_bestpos->lon_d, oem7_bestpos->hgt_d, oem7_bestpos->stn_id, oem7_bestpos->diff_age, oem7_bestpos->sol_age, oem7_bestpos->solnSVs);
}

/**
 * @brief Encode a oem7_bestpos struct on a channel
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param chan The MAVLink channel this message will be sent over
 * @param msg The MAVLink message to compress the data into
 * @param oem7_bestpos C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_bestpos_encode_chan(uint8_t system_id, uint8_t component_id, uint8_t chan, mavlink_message_t* msg, const mavlink_oem7_bestpos_t* oem7_bestpos)
{
    return mavlink_msg_oem7_bestpos_pack_chan(system_id, component_id, chan, msg, oem7_bestpos->sol_status, oem7_bestpos->pos_type, oem7_bestpos->lat, oem7_bestpos->lon, oem7_bestpos->hgt, oem7_bestpos->undulation, oem7_bestpos->datum_id, oem7_bestpos->lat_d, oem7_bestpos->lon_d, oem7_bestpos->hgt_d, oem7_bestpos->stn_id, oem7_bestpos->diff_age, oem7_bestpos->sol_age, oem7_bestpos->solnSVs);
}

/**
 * @brief Encode a oem7_bestpos struct with provided status structure
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param status MAVLink status structure
 * @param msg The MAVLink message to compress the data into
 * @param oem7_bestpos C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_bestpos_encode_status(uint8_t system_id, uint8_t component_id, mavlink_status_t* _status, mavlink_message_t* msg, const mavlink_oem7_bestpos_t* oem7_bestpos)
{
    return mavlink_msg_oem7_bestpos_pack_status(system_id, component_id, _status, msg,  oem7_bestpos->sol_status, oem7_bestpos->pos_type, oem7_bestpos->lat, oem7_bestpos->lon, oem7_bestpos->hgt, oem7_bestpos->undulation, oem7_bestpos->datum_id, oem7_bestpos->lat_d, oem7_bestpos->lon_d, oem7_bestpos->hgt_d, oem7_bestpos->stn_id, oem7_bestpos->diff_age, oem7_bestpos->sol_age, oem7_bestpos->solnSVs);
}

/**
 * @brief Send a oem7_bestpos message
 * @param chan MAVLink channel to send the message
 *
 * @param sol_status  BESTPOS solution status
 * @param pos_type  BESTPOS position type
 * @param lat  BESTPOS latitude (degrees)
 * @param lon  BESTPOS longitude (degrees)
 * @param hgt  BESTPOS height above mean sea level (meters)
 * @param undulation  BESTPOS undulation - the relationship between the geoid and the ellipsoid(m) of the chosen datum
 * @param datum_id  BESTPOS Datum ID number, 61 = WGS84, 63 = User
 * @param lat_d  BESTPOS latitude standard deviation(m)
 * @param lon_d  BESTPOS longitude standard deviation(m)
 * @param hgt_d  BESTPOS height standard deviation(m)
 * @param stn_id  BESTPOS Station ID
 * @param diff_age  BESTPOS different age in seconds
 * @param sol_age  BESTPOS solution age in seconds
 * @param solnSVs  BESTPOS Number of satellites used in solution
 */
#ifdef MAVLINK_USE_CONVENIENCE_FUNCTIONS

static inline void mavlink_msg_oem7_bestpos_send(mavlink_channel_t chan, uint32_t sol_status, uint32_t pos_type, double lat, double lon, double hgt, float undulation, uint32_t datum_id, float lat_d, float lon_d, float hgt_d, const char *stn_id, float diff_age, float sol_age, uint8_t solnSVs)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_BESTPOS_LEN];
    _mav_put_double(buf, 0, lat);
    _mav_put_double(buf, 8, lon);
    _mav_put_double(buf, 16, hgt);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, pos_type);
    _mav_put_float(buf, 32, undulation);
    _mav_put_uint32_t(buf, 36, datum_id);
    _mav_put_float(buf, 40, lat_d);
    _mav_put_float(buf, 44, lon_d);
    _mav_put_float(buf, 48, hgt_d);
    _mav_put_float(buf, 52, diff_age);
    _mav_put_float(buf, 56, sol_age);
    _mav_put_uint8_t(buf, 64, solnSVs);
    _mav_put_char_array(buf, 60, stn_id, 4);
    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTPOS, buf, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_CRC);
#else
    mavlink_oem7_bestpos_t packet;
    packet.lat = lat;
    packet.lon = lon;
    packet.hgt = hgt;
    packet.sol_status = sol_status;
    packet.pos_type = pos_type;
    packet.undulation = undulation;
    packet.datum_id = datum_id;
    packet.lat_d = lat_d;
    packet.lon_d = lon_d;
    packet.hgt_d = hgt_d;
    packet.diff_age = diff_age;
    packet.sol_age = sol_age;
    packet.solnSVs = solnSVs;
    mav_array_memcpy(packet.stn_id, stn_id, sizeof(char)*4);
    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTPOS, (const char *)&packet, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_CRC);
#endif
}

/**
 * @brief Send a oem7_bestpos message
 * @param chan MAVLink channel to send the message
 * @param struct The MAVLink struct to serialize
 */
static inline void mavlink_msg_oem7_bestpos_send_struct(mavlink_channel_t chan, const mavlink_oem7_bestpos_t* oem7_bestpos)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    mavlink_msg_oem7_bestpos_send(chan, oem7_bestpos->sol_status, oem7_bestpos->pos_type, oem7_bestpos->lat, oem7_bestpos->lon, oem7_bestpos->hgt, oem7_bestpos->undulation, oem7_bestpos->datum_id, oem7_bestpos->lat_d, oem7_bestpos->lon_d, oem7_bestpos->hgt_d, oem7_bestpos->stn_id, oem7_bestpos->diff_age, oem7_bestpos->sol_age, oem7_bestpos->solnSVs);
#else
    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTPOS, (const char *)oem7_bestpos, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_CRC);
#endif
}

#if MAVLINK_MSG_ID_OEM7_BESTPOS_LEN <= MAVLINK_MAX_PAYLOAD_LEN
/*
  This variant of _send() can be used to save stack space by re-using
  memory from the receive buffer.  The caller provides a
  mavlink_message_t which is the size of a full mavlink message. This
  is usually the receive buffer for the channel, and allows a reply to an
  incoming message with minimum stack space usage.
 */
static inline void mavlink_msg_oem7_bestpos_send_buf(mavlink_message_t *msgbuf, mavlink_channel_t chan,  uint32_t sol_status, uint32_t pos_type, double lat, double lon, double hgt, float undulation, uint32_t datum_id, float lat_d, float lon_d, float hgt_d, const char *stn_id, float diff_age, float sol_age, uint8_t solnSVs)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char *buf = (char *)msgbuf;
    _mav_put_double(buf, 0, lat);
    _mav_put_double(buf, 8, lon);
    _mav_put_double(buf, 16, hgt);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, pos_type);
    _mav_put_float(buf, 32, undulation);
    _mav_put_uint32_t(buf, 36, datum_id);
    _mav_put_float(buf, 40, lat_d);
    _mav_put_float(buf, 44, lon_d);
    _mav_put_float(buf, 48, hgt_d);
    _mav_put_float(buf, 52, diff_age);
    _mav_put_float(buf, 56, sol_age);
    _mav_put_uint8_t(buf, 64, solnSVs);
    _mav_put_char_array(buf, 60, stn_id, 4);
    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTPOS, buf, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_CRC);
#else
    mavlink_oem7_bestpos_t *packet = (mavlink_oem7_bestpos_t *)msgbuf;
    packet->lat = lat;
    packet->lon = lon;
    packet->hgt = hgt;
    packet->sol_status = sol_status;
    packet->pos_type = pos_type;
    packet->undulation = undulation;
    packet->datum_id = datum_id;
    packet->lat_d = lat_d;
    packet->lon_d = lon_d;
    packet->hgt_d = hgt_d;
    packet->diff_age = diff_age;
    packet->sol_age = sol_age;
    packet->solnSVs = solnSVs;
    mav_array_memcpy(packet->stn_id, stn_id, sizeof(char)*4);
    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTPOS, (const char *)packet, MAVLINK_MSG_ID_OEM7_BESTPOS_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN, MAVLINK_MSG_ID_OEM7_BESTPOS_CRC);
#endif
}
#endif

#endif

// MESSAGE OEM7_BESTPOS UNPACKING


/**
 * @brief Get field sol_status from oem7_bestpos message
 *
 * @return  BESTPOS solution status
 */
static inline uint32_t mavlink_msg_oem7_bestpos_get_sol_status(const mavlink_message_t* msg)
{
    return _MAV_RETURN_uint32_t(msg,  24);
}

/**
 * @brief Get field pos_type from oem7_bestpos message
 *
 * @return  BESTPOS position type
 */
static inline uint32_t mavlink_msg_oem7_bestpos_get_pos_type(const mavlink_message_t* msg)
{
    return _MAV_RETURN_uint32_t(msg,  28);
}

/**
 * @brief Get field lat from oem7_bestpos message
 *
 * @return  BESTPOS latitude (degrees)
 */
static inline double mavlink_msg_oem7_bestpos_get_lat(const mavlink_message_t* msg)
{
    return _MAV_RETURN_double(msg,  0);
}

/**
 * @brief Get field lon from oem7_bestpos message
 *
 * @return  BESTPOS longitude (degrees)
 */
static inline double mavlink_msg_oem7_bestpos_get_lon(const mavlink_message_t* msg)
{
    return _MAV_RETURN_double(msg,  8);
}

/**
 * @brief Get field hgt from oem7_bestpos message
 *
 * @return  BESTPOS height above mean sea level (meters)
 */
static inline double mavlink_msg_oem7_bestpos_get_hgt(const mavlink_message_t* msg)
{
    return _MAV_RETURN_double(msg,  16);
}

/**
 * @brief Get field undulation from oem7_bestpos message
 *
 * @return  BESTPOS undulation - the relationship between the geoid and the ellipsoid(m) of the chosen datum
 */
static inline float mavlink_msg_oem7_bestpos_get_undulation(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  32);
}

/**
 * @brief Get field datum_id from oem7_bestpos message
 *
 * @return  BESTPOS Datum ID number, 61 = WGS84, 63 = User
 */
static inline uint32_t mavlink_msg_oem7_bestpos_get_datum_id(const mavlink_message_t* msg)
{
    return _MAV_RETURN_uint32_t(msg,  36);
}

/**
 * @brief Get field lat_d from oem7_bestpos message
 *
 * @return  BESTPOS latitude standard deviation(m)
 */
static inline float mavlink_msg_oem7_bestpos_get_lat_d(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  40);
}

/**
 * @brief Get field lon_d from oem7_bestpos message
 *
 * @return  BESTPOS longitude standard deviation(m)
 */
static inline float mavlink_msg_oem7_bestpos_get_lon_d(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  44);
}

/**
 * @brief Get field hgt_d from oem7_bestpos message
 *
 * @return  BESTPOS height standard deviation(m)
 */
static inline float mavlink_msg_oem7_bestpos_get_hgt_d(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  48);
}

/**
 * @brief Get field stn_id from oem7_bestpos message
 *
 * @return  BESTPOS Station ID
 */
static inline uint16_t mavlink_msg_oem7_bestpos_get_stn_id(const mavlink_message_t* msg, char *stn_id)
{
    return _MAV_RETURN_char_array(msg, stn_id, 4,  60);
}

/**
 * @brief Get field diff_age from oem7_bestpos message
 *
 * @return  BESTPOS different age in seconds
 */
static inline float mavlink_msg_oem7_bestpos_get_diff_age(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  52);
}

/**
 * @brief Get field sol_age from oem7_bestpos message
 *
 * @return  BESTPOS solution age in seconds
 */
static inline float mavlink_msg_oem7_bestpos_get_sol_age(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  56);
}

/**
 * @brief Get field solnSVs from oem7_bestpos message
 *
 * @return  BESTPOS Number of satellites used in solution
 */
static inline uint8_t mavlink_msg_oem7_bestpos_get_solnSVs(const mavlink_message_t* msg)
{
    return _MAV_RETURN_uint8_t(msg,  64);
}

/**
 * @brief Decode a oem7_bestpos message into a struct
 *
 * @param msg The message to decode
 * @param oem7_bestpos C-struct to decode the message contents into
 */
static inline void mavlink_msg_oem7_bestpos_decode(const mavlink_message_t* msg, mavlink_oem7_bestpos_t* oem7_bestpos)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    oem7_bestpos->lat = mavlink_msg_oem7_bestpos_get_lat(msg);
    oem7_bestpos->lon = mavlink_msg_oem7_bestpos_get_lon(msg);
    oem7_bestpos->hgt = mavlink_msg_oem7_bestpos_get_hgt(msg);
    oem7_bestpos->sol_status = mavlink_msg_oem7_bestpos_get_sol_status(msg);
    oem7_bestpos->pos_type = mavlink_msg_oem7_bestpos_get_pos_type(msg);
    oem7_bestpos->undulation = mavlink_msg_oem7_bestpos_get_undulation(msg);
    oem7_bestpos->datum_id = mavlink_msg_oem7_bestpos_get_datum_id(msg);
    oem7_bestpos->lat_d = mavlink_msg_oem7_bestpos_get_lat_d(msg);
    oem7_bestpos->lon_d = mavlink_msg_oem7_bestpos_get_lon_d(msg);
    oem7_bestpos->hgt_d = mavlink_msg_oem7_bestpos_get_hgt_d(msg);
    oem7_bestpos->diff_age = mavlink_msg_oem7_bestpos_get_diff_age(msg);
    oem7_bestpos->sol_age = mavlink_msg_oem7_bestpos_get_sol_age(msg);
    mavlink_msg_oem7_bestpos_get_stn_id(msg, oem7_bestpos->stn_id);
    oem7_bestpos->solnSVs = mavlink_msg_oem7_bestpos_get_solnSVs(msg);
#else
        uint8_t len = msg->len < MAVLINK_MSG_ID_OEM7_BESTPOS_LEN? msg->len : MAVLINK_MSG_ID_OEM7_BESTPOS_LEN;
        memset(oem7_bestpos, 0, MAVLINK_MSG_ID_OEM7_BESTPOS_LEN);
    memcpy(oem7_bestpos, _MAV_PAYLOAD(msg), len);
#endif
}
