#pragma once
// MESSAGE OEM7_BESTVEL PACKING

#define MAVLINK_MSG_ID_OEM7_BESTVEL 50011


typedef struct __mavlink_oem7_bestvel_t {
 double hor_spd; /*<  BESTVEL horizontal speed over ground, in meters per second*/
 double trk_gnd; /*<  BESTVEL acutal direction of motion over ground with respect to True North, in degrees*/
 double vert_spd; /*<  BESTVEL vertical speed, in meters per second, where positive values indicate increasing altitude(up) and negative values indicate decreasing altitude(down)*/
 uint32_t sol_status; /*<  BESTVEL solution status*/
 uint32_t vel_type; /*<  BESTVEL velocity type*/
 float latency; /*<  BESTVEL a measure of the latency in the velocity time tag in seconds*/
 float age; /*<  BESTVEL Differential age in seconds*/
} mavlink_oem7_bestvel_t;

#define MAVLINK_MSG_ID_OEM7_BESTVEL_LEN 40
#define MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN 40
#define MAVLINK_MSG_ID_50011_LEN 40
#define MAVLINK_MSG_ID_50011_MIN_LEN 40

#define MAVLINK_MSG_ID_OEM7_BESTVEL_CRC 63
#define MAVLINK_MSG_ID_50011_CRC 63



#if MAVLINK_COMMAND_24BIT
#define MAVLINK_MESSAGE_INFO_OEM7_BESTVEL { \
    50011, \
    "OEM7_BESTVEL", \
    7, \
    {  { "sol_status", NULL, MAVLINK_TYPE_UINT32_T, 0, 24, offsetof(mavlink_oem7_bestvel_t, sol_status) }, \
         { "vel_type", NULL, MAVLINK_TYPE_UINT32_T, 0, 28, offsetof(mavlink_oem7_bestvel_t, vel_type) }, \
         { "latency", NULL, MAVLINK_TYPE_FLOAT, 0, 32, offsetof(mavlink_oem7_bestvel_t, latency) }, \
         { "age", NULL, MAVLINK_TYPE_FLOAT, 0, 36, offsetof(mavlink_oem7_bestvel_t, age) }, \
         { "hor_spd", NULL, MAVLINK_TYPE_DOUBLE, 0, 0, offsetof(mavlink_oem7_bestvel_t, hor_spd) }, \
         { "trk_gnd", NULL, MAVLINK_TYPE_DOUBLE, 0, 8, offsetof(mavlink_oem7_bestvel_t, trk_gnd) }, \
         { "vert_spd", NULL, MAVLINK_TYPE_DOUBLE, 0, 16, offsetof(mavlink_oem7_bestvel_t, vert_spd) }, \
         } \
}
#else
#define MAVLINK_MESSAGE_INFO_OEM7_BESTVEL { \
    "OEM7_BESTVEL", \
    7, \
    {  { "sol_status", NULL, MAVLINK_TYPE_UINT32_T, 0, 24, offsetof(mavlink_oem7_bestvel_t, sol_status) }, \
         { "vel_type", NULL, MAVLINK_TYPE_UINT32_T, 0, 28, offsetof(mavlink_oem7_bestvel_t, vel_type) }, \
         { "latency", NULL, MAVLINK_TYPE_FLOAT, 0, 32, offsetof(mavlink_oem7_bestvel_t, latency) }, \
         { "age", NULL, MAVLINK_TYPE_FLOAT, 0, 36, offsetof(mavlink_oem7_bestvel_t, age) }, \
         { "hor_spd", NULL, MAVLINK_TYPE_DOUBLE, 0, 0, offsetof(mavlink_oem7_bestvel_t, hor_spd) }, \
         { "trk_gnd", NULL, MAVLINK_TYPE_DOUBLE, 0, 8, offsetof(mavlink_oem7_bestvel_t, trk_gnd) }, \
         { "vert_spd", NULL, MAVLINK_TYPE_DOUBLE, 0, 16, offsetof(mavlink_oem7_bestvel_t, vert_spd) }, \
         } \
}
#endif

/**
 * @brief Pack a oem7_bestvel message
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param msg The MAVLink message to compress the data into
 *
 * @param sol_status  BESTVEL solution status
 * @param vel_type  BESTVEL velocity type
 * @param latency  BESTVEL a measure of the latency in the velocity time tag in seconds
 * @param age  BESTVEL Differential age in seconds
 * @param hor_spd  BESTVEL horizontal speed over ground, in meters per second
 * @param trk_gnd  BESTVEL acutal direction of motion over ground with respect to True North, in degrees
 * @param vert_spd  BESTVEL vertical speed, in meters per second, where positive values indicate increasing altitude(up) and negative values indicate decreasing altitude(down)
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_bestvel_pack(uint8_t system_id, uint8_t component_id, mavlink_message_t* msg,
                               uint32_t sol_status, uint32_t vel_type, float latency, float age, double hor_spd, double trk_gnd, double vert_spd)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_BESTVEL_LEN];
    _mav_put_double(buf, 0, hor_spd);
    _mav_put_double(buf, 8, trk_gnd);
    _mav_put_double(buf, 16, vert_spd);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, vel_type);
    _mav_put_float(buf, 32, latency);
    _mav_put_float(buf, 36, age);

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN);
#else
    mavlink_oem7_bestvel_t packet;
    packet.hor_spd = hor_spd;
    packet.trk_gnd = trk_gnd;
    packet.vert_spd = vert_spd;
    packet.sol_status = sol_status;
    packet.vel_type = vel_type;
    packet.latency = latency;
    packet.age = age;

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_BESTVEL;
    return mavlink_finalize_message(msg, system_id, component_id, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_CRC);
}

/**
 * @brief Pack a oem7_bestvel message
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param status MAVLink status structure
 * @param msg The MAVLink message to compress the data into
 *
 * @param sol_status  BESTVEL solution status
 * @param vel_type  BESTVEL velocity type
 * @param latency  BESTVEL a measure of the latency in the velocity time tag in seconds
 * @param age  BESTVEL Differential age in seconds
 * @param hor_spd  BESTVEL horizontal speed over ground, in meters per second
 * @param trk_gnd  BESTVEL acutal direction of motion over ground with respect to True North, in degrees
 * @param vert_spd  BESTVEL vertical speed, in meters per second, where positive values indicate increasing altitude(up) and negative values indicate decreasing altitude(down)
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_bestvel_pack_status(uint8_t system_id, uint8_t component_id, mavlink_status_t *_status, mavlink_message_t* msg,
                               uint32_t sol_status, uint32_t vel_type, float latency, float age, double hor_spd, double trk_gnd, double vert_spd)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_BESTVEL_LEN];
    _mav_put_double(buf, 0, hor_spd);
    _mav_put_double(buf, 8, trk_gnd);
    _mav_put_double(buf, 16, vert_spd);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, vel_type);
    _mav_put_float(buf, 32, latency);
    _mav_put_float(buf, 36, age);

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN);
#else
    mavlink_oem7_bestvel_t packet;
    packet.hor_spd = hor_spd;
    packet.trk_gnd = trk_gnd;
    packet.vert_spd = vert_spd;
    packet.sol_status = sol_status;
    packet.vel_type = vel_type;
    packet.latency = latency;
    packet.age = age;

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_BESTVEL;
#if MAVLINK_CRC_EXTRA
    return mavlink_finalize_message_buffer(msg, system_id, component_id, _status, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_CRC);
#else
    return mavlink_finalize_message_buffer(msg, system_id, component_id, _status, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN);
#endif
}

/**
 * @brief Pack a oem7_bestvel message on a channel
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param chan The MAVLink channel this message will be sent over
 * @param msg The MAVLink message to compress the data into
 * @param sol_status  BESTVEL solution status
 * @param vel_type  BESTVEL velocity type
 * @param latency  BESTVEL a measure of the latency in the velocity time tag in seconds
 * @param age  BESTVEL Differential age in seconds
 * @param hor_spd  BESTVEL horizontal speed over ground, in meters per second
 * @param trk_gnd  BESTVEL acutal direction of motion over ground with respect to True North, in degrees
 * @param vert_spd  BESTVEL vertical speed, in meters per second, where positive values indicate increasing altitude(up) and negative values indicate decreasing altitude(down)
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_bestvel_pack_chan(uint8_t system_id, uint8_t component_id, uint8_t chan,
                               mavlink_message_t* msg,
                                   uint32_t sol_status,uint32_t vel_type,float latency,float age,double hor_spd,double trk_gnd,double vert_spd)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_BESTVEL_LEN];
    _mav_put_double(buf, 0, hor_spd);
    _mav_put_double(buf, 8, trk_gnd);
    _mav_put_double(buf, 16, vert_spd);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, vel_type);
    _mav_put_float(buf, 32, latency);
    _mav_put_float(buf, 36, age);

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN);
#else
    mavlink_oem7_bestvel_t packet;
    packet.hor_spd = hor_spd;
    packet.trk_gnd = trk_gnd;
    packet.vert_spd = vert_spd;
    packet.sol_status = sol_status;
    packet.vel_type = vel_type;
    packet.latency = latency;
    packet.age = age;

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_BESTVEL;
    return mavlink_finalize_message_chan(msg, system_id, component_id, chan, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_CRC);
}

/**
 * @brief Encode a oem7_bestvel struct
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param msg The MAVLink message to compress the data into
 * @param oem7_bestvel C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_bestvel_encode(uint8_t system_id, uint8_t component_id, mavlink_message_t* msg, const mavlink_oem7_bestvel_t* oem7_bestvel)
{
    return mavlink_msg_oem7_bestvel_pack(system_id, component_id, msg, oem7_bestvel->sol_status, oem7_bestvel->vel_type, oem7_bestvel->latency, oem7_bestvel->age, oem7_bestvel->hor_spd, oem7_bestvel->trk_gnd, oem7_bestvel->vert_spd);
}

/**
 * @brief Encode a oem7_bestvel struct on a channel
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param chan The MAVLink channel this message will be sent over
 * @param msg The MAVLink message to compress the data into
 * @param oem7_bestvel C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_bestvel_encode_chan(uint8_t system_id, uint8_t component_id, uint8_t chan, mavlink_message_t* msg, const mavlink_oem7_bestvel_t* oem7_bestvel)
{
    return mavlink_msg_oem7_bestvel_pack_chan(system_id, component_id, chan, msg, oem7_bestvel->sol_status, oem7_bestvel->vel_type, oem7_bestvel->latency, oem7_bestvel->age, oem7_bestvel->hor_spd, oem7_bestvel->trk_gnd, oem7_bestvel->vert_spd);
}

/**
 * @brief Encode a oem7_bestvel struct with provided status structure
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param status MAVLink status structure
 * @param msg The MAVLink message to compress the data into
 * @param oem7_bestvel C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_bestvel_encode_status(uint8_t system_id, uint8_t component_id, mavlink_status_t* _status, mavlink_message_t* msg, const mavlink_oem7_bestvel_t* oem7_bestvel)
{
    return mavlink_msg_oem7_bestvel_pack_status(system_id, component_id, _status, msg,  oem7_bestvel->sol_status, oem7_bestvel->vel_type, oem7_bestvel->latency, oem7_bestvel->age, oem7_bestvel->hor_spd, oem7_bestvel->trk_gnd, oem7_bestvel->vert_spd);
}

/**
 * @brief Send a oem7_bestvel message
 * @param chan MAVLink channel to send the message
 *
 * @param sol_status  BESTVEL solution status
 * @param vel_type  BESTVEL velocity type
 * @param latency  BESTVEL a measure of the latency in the velocity time tag in seconds
 * @param age  BESTVEL Differential age in seconds
 * @param hor_spd  BESTVEL horizontal speed over ground, in meters per second
 * @param trk_gnd  BESTVEL acutal direction of motion over ground with respect to True North, in degrees
 * @param vert_spd  BESTVEL vertical speed, in meters per second, where positive values indicate increasing altitude(up) and negative values indicate decreasing altitude(down)
 */
#ifdef MAVLINK_USE_CONVENIENCE_FUNCTIONS

static inline void mavlink_msg_oem7_bestvel_send(mavlink_channel_t chan, uint32_t sol_status, uint32_t vel_type, float latency, float age, double hor_spd, double trk_gnd, double vert_spd)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_BESTVEL_LEN];
    _mav_put_double(buf, 0, hor_spd);
    _mav_put_double(buf, 8, trk_gnd);
    _mav_put_double(buf, 16, vert_spd);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, vel_type);
    _mav_put_float(buf, 32, latency);
    _mav_put_float(buf, 36, age);

    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTVEL, buf, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_CRC);
#else
    mavlink_oem7_bestvel_t packet;
    packet.hor_spd = hor_spd;
    packet.trk_gnd = trk_gnd;
    packet.vert_spd = vert_spd;
    packet.sol_status = sol_status;
    packet.vel_type = vel_type;
    packet.latency = latency;
    packet.age = age;

    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTVEL, (const char *)&packet, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_CRC);
#endif
}

/**
 * @brief Send a oem7_bestvel message
 * @param chan MAVLink channel to send the message
 * @param struct The MAVLink struct to serialize
 */
static inline void mavlink_msg_oem7_bestvel_send_struct(mavlink_channel_t chan, const mavlink_oem7_bestvel_t* oem7_bestvel)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    mavlink_msg_oem7_bestvel_send(chan, oem7_bestvel->sol_status, oem7_bestvel->vel_type, oem7_bestvel->latency, oem7_bestvel->age, oem7_bestvel->hor_spd, oem7_bestvel->trk_gnd, oem7_bestvel->vert_spd);
#else
    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTVEL, (const char *)oem7_bestvel, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_CRC);
#endif
}

#if MAVLINK_MSG_ID_OEM7_BESTVEL_LEN <= MAVLINK_MAX_PAYLOAD_LEN
/*
  This variant of _send() can be used to save stack space by re-using
  memory from the receive buffer.  The caller provides a
  mavlink_message_t which is the size of a full mavlink message. This
  is usually the receive buffer for the channel, and allows a reply to an
  incoming message with minimum stack space usage.
 */
static inline void mavlink_msg_oem7_bestvel_send_buf(mavlink_message_t *msgbuf, mavlink_channel_t chan,  uint32_t sol_status, uint32_t vel_type, float latency, float age, double hor_spd, double trk_gnd, double vert_spd)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char *buf = (char *)msgbuf;
    _mav_put_double(buf, 0, hor_spd);
    _mav_put_double(buf, 8, trk_gnd);
    _mav_put_double(buf, 16, vert_spd);
    _mav_put_uint32_t(buf, 24, sol_status);
    _mav_put_uint32_t(buf, 28, vel_type);
    _mav_put_float(buf, 32, latency);
    _mav_put_float(buf, 36, age);

    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTVEL, buf, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_CRC);
#else
    mavlink_oem7_bestvel_t *packet = (mavlink_oem7_bestvel_t *)msgbuf;
    packet->hor_spd = hor_spd;
    packet->trk_gnd = trk_gnd;
    packet->vert_spd = vert_spd;
    packet->sol_status = sol_status;
    packet->vel_type = vel_type;
    packet->latency = latency;
    packet->age = age;

    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_BESTVEL, (const char *)packet, MAVLINK_MSG_ID_OEM7_BESTVEL_MIN_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN, MAVLINK_MSG_ID_OEM7_BESTVEL_CRC);
#endif
}
#endif

#endif

// MESSAGE OEM7_BESTVEL UNPACKING


/**
 * @brief Get field sol_status from oem7_bestvel message
 *
 * @return  BESTVEL solution status
 */
static inline uint32_t mavlink_msg_oem7_bestvel_get_sol_status(const mavlink_message_t* msg)
{
    return _MAV_RETURN_uint32_t(msg,  24);
}

/**
 * @brief Get field vel_type from oem7_bestvel message
 *
 * @return  BESTVEL velocity type
 */
static inline uint32_t mavlink_msg_oem7_bestvel_get_vel_type(const mavlink_message_t* msg)
{
    return _MAV_RETURN_uint32_t(msg,  28);
}

/**
 * @brief Get field latency from oem7_bestvel message
 *
 * @return  BESTVEL a measure of the latency in the velocity time tag in seconds
 */
static inline float mavlink_msg_oem7_bestvel_get_latency(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  32);
}

/**
 * @brief Get field age from oem7_bestvel message
 *
 * @return  BESTVEL Differential age in seconds
 */
static inline float mavlink_msg_oem7_bestvel_get_age(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  36);
}

/**
 * @brief Get field hor_spd from oem7_bestvel message
 *
 * @return  BESTVEL horizontal speed over ground, in meters per second
 */
static inline double mavlink_msg_oem7_bestvel_get_hor_spd(const mavlink_message_t* msg)
{
    return _MAV_RETURN_double(msg,  0);
}

/**
 * @brief Get field trk_gnd from oem7_bestvel message
 *
 * @return  BESTVEL acutal direction of motion over ground with respect to True North, in degrees
 */
static inline double mavlink_msg_oem7_bestvel_get_trk_gnd(const mavlink_message_t* msg)
{
    return _MAV_RETURN_double(msg,  8);
}

/**
 * @brief Get field vert_spd from oem7_bestvel message
 *
 * @return  BESTVEL vertical speed, in meters per second, where positive values indicate increasing altitude(up) and negative values indicate decreasing altitude(down)
 */
static inline double mavlink_msg_oem7_bestvel_get_vert_spd(const mavlink_message_t* msg)
{
    return _MAV_RETURN_double(msg,  16);
}

/**
 * @brief Decode a oem7_bestvel message into a struct
 *
 * @param msg The message to decode
 * @param oem7_bestvel C-struct to decode the message contents into
 */
static inline void mavlink_msg_oem7_bestvel_decode(const mavlink_message_t* msg, mavlink_oem7_bestvel_t* oem7_bestvel)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    oem7_bestvel->hor_spd = mavlink_msg_oem7_bestvel_get_hor_spd(msg);
    oem7_bestvel->trk_gnd = mavlink_msg_oem7_bestvel_get_trk_gnd(msg);
    oem7_bestvel->vert_spd = mavlink_msg_oem7_bestvel_get_vert_spd(msg);
    oem7_bestvel->sol_status = mavlink_msg_oem7_bestvel_get_sol_status(msg);
    oem7_bestvel->vel_type = mavlink_msg_oem7_bestvel_get_vel_type(msg);
    oem7_bestvel->latency = mavlink_msg_oem7_bestvel_get_latency(msg);
    oem7_bestvel->age = mavlink_msg_oem7_bestvel_get_age(msg);
#else
        uint8_t len = msg->len < MAVLINK_MSG_ID_OEM7_BESTVEL_LEN? msg->len : MAVLINK_MSG_ID_OEM7_BESTVEL_LEN;
        memset(oem7_bestvel, 0, MAVLINK_MSG_ID_OEM7_BESTVEL_LEN);
    memcpy(oem7_bestvel, _MAV_PAYLOAD(msg), len);
#endif
}
