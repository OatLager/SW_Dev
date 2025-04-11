#pragma once
// MESSAGE OEM7_HEADING PACKING

#define MAVLINK_MSG_ID_OEM7_HEADING 50012


typedef struct __mavlink_oem7_heading_t {
 uint32_t sol_status; /*<  DUALANTENNAHEADING solution status*/
 uint32_t pos_type; /*<  DUALANTENNAHEADING position type*/
 float length; /*<  DUALANTENNAHEADING baseline length in meters*/
 float heading; /*<  DUALANTENNAHEADING heading in degree(0 ~ 359.999)*/
 float pitch; /*<  DUALANTENNAHEADING pitch (+-90 degrees)*/
 float hdg_std_dev; /*<  DUALANTENNAHEADING heading standard deviation in degrees*/
 float ptch_std_dev; /*<  DUALANTENNAHEADING pitch standard deviation in degrees*/
} mavlink_oem7_heading_t;

#define MAVLINK_MSG_ID_OEM7_HEADING_LEN 28
#define MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN 28
#define MAVLINK_MSG_ID_50012_LEN 28
#define MAVLINK_MSG_ID_50012_MIN_LEN 28

#define MAVLINK_MSG_ID_OEM7_HEADING_CRC 107
#define MAVLINK_MSG_ID_50012_CRC 107



#if MAVLINK_COMMAND_24BIT
#define MAVLINK_MESSAGE_INFO_OEM7_HEADING { \
    50012, \
    "OEM7_HEADING", \
    7, \
    {  { "sol_status", NULL, MAVLINK_TYPE_UINT32_T, 0, 0, offsetof(mavlink_oem7_heading_t, sol_status) }, \
         { "pos_type", NULL, MAVLINK_TYPE_UINT32_T, 0, 4, offsetof(mavlink_oem7_heading_t, pos_type) }, \
         { "length", NULL, MAVLINK_TYPE_FLOAT, 0, 8, offsetof(mavlink_oem7_heading_t, length) }, \
         { "heading", NULL, MAVLINK_TYPE_FLOAT, 0, 12, offsetof(mavlink_oem7_heading_t, heading) }, \
         { "pitch", NULL, MAVLINK_TYPE_FLOAT, 0, 16, offsetof(mavlink_oem7_heading_t, pitch) }, \
         { "hdg_std_dev", NULL, MAVLINK_TYPE_FLOAT, 0, 20, offsetof(mavlink_oem7_heading_t, hdg_std_dev) }, \
         { "ptch_std_dev", NULL, MAVLINK_TYPE_FLOAT, 0, 24, offsetof(mavlink_oem7_heading_t, ptch_std_dev) }, \
         } \
}
#else
#define MAVLINK_MESSAGE_INFO_OEM7_HEADING { \
    "OEM7_HEADING", \
    7, \
    {  { "sol_status", NULL, MAVLINK_TYPE_UINT32_T, 0, 0, offsetof(mavlink_oem7_heading_t, sol_status) }, \
         { "pos_type", NULL, MAVLINK_TYPE_UINT32_T, 0, 4, offsetof(mavlink_oem7_heading_t, pos_type) }, \
         { "length", NULL, MAVLINK_TYPE_FLOAT, 0, 8, offsetof(mavlink_oem7_heading_t, length) }, \
         { "heading", NULL, MAVLINK_TYPE_FLOAT, 0, 12, offsetof(mavlink_oem7_heading_t, heading) }, \
         { "pitch", NULL, MAVLINK_TYPE_FLOAT, 0, 16, offsetof(mavlink_oem7_heading_t, pitch) }, \
         { "hdg_std_dev", NULL, MAVLINK_TYPE_FLOAT, 0, 20, offsetof(mavlink_oem7_heading_t, hdg_std_dev) }, \
         { "ptch_std_dev", NULL, MAVLINK_TYPE_FLOAT, 0, 24, offsetof(mavlink_oem7_heading_t, ptch_std_dev) }, \
         } \
}
#endif

/**
 * @brief Pack a oem7_heading message
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param msg The MAVLink message to compress the data into
 *
 * @param sol_status  DUALANTENNAHEADING solution status
 * @param pos_type  DUALANTENNAHEADING position type
 * @param length  DUALANTENNAHEADING baseline length in meters
 * @param heading  DUALANTENNAHEADING heading in degree(0 ~ 359.999)
 * @param pitch  DUALANTENNAHEADING pitch (+-90 degrees)
 * @param hdg_std_dev  DUALANTENNAHEADING heading standard deviation in degrees
 * @param ptch_std_dev  DUALANTENNAHEADING pitch standard deviation in degrees
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_heading_pack(uint8_t system_id, uint8_t component_id, mavlink_message_t* msg,
                               uint32_t sol_status, uint32_t pos_type, float length, float heading, float pitch, float hdg_std_dev, float ptch_std_dev)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_HEADING_LEN];
    _mav_put_uint32_t(buf, 0, sol_status);
    _mav_put_uint32_t(buf, 4, pos_type);
    _mav_put_float(buf, 8, length);
    _mav_put_float(buf, 12, heading);
    _mav_put_float(buf, 16, pitch);
    _mav_put_float(buf, 20, hdg_std_dev);
    _mav_put_float(buf, 24, ptch_std_dev);

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_HEADING_LEN);
#else
    mavlink_oem7_heading_t packet;
    packet.sol_status = sol_status;
    packet.pos_type = pos_type;
    packet.length = length;
    packet.heading = heading;
    packet.pitch = pitch;
    packet.hdg_std_dev = hdg_std_dev;
    packet.ptch_std_dev = ptch_std_dev;

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_HEADING_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_HEADING;
    return mavlink_finalize_message(msg, system_id, component_id, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN, MAVLINK_MSG_ID_OEM7_HEADING_CRC);
}

/**
 * @brief Pack a oem7_heading message
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param status MAVLink status structure
 * @param msg The MAVLink message to compress the data into
 *
 * @param sol_status  DUALANTENNAHEADING solution status
 * @param pos_type  DUALANTENNAHEADING position type
 * @param length  DUALANTENNAHEADING baseline length in meters
 * @param heading  DUALANTENNAHEADING heading in degree(0 ~ 359.999)
 * @param pitch  DUALANTENNAHEADING pitch (+-90 degrees)
 * @param hdg_std_dev  DUALANTENNAHEADING heading standard deviation in degrees
 * @param ptch_std_dev  DUALANTENNAHEADING pitch standard deviation in degrees
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_heading_pack_status(uint8_t system_id, uint8_t component_id, mavlink_status_t *_status, mavlink_message_t* msg,
                               uint32_t sol_status, uint32_t pos_type, float length, float heading, float pitch, float hdg_std_dev, float ptch_std_dev)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_HEADING_LEN];
    _mav_put_uint32_t(buf, 0, sol_status);
    _mav_put_uint32_t(buf, 4, pos_type);
    _mav_put_float(buf, 8, length);
    _mav_put_float(buf, 12, heading);
    _mav_put_float(buf, 16, pitch);
    _mav_put_float(buf, 20, hdg_std_dev);
    _mav_put_float(buf, 24, ptch_std_dev);

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_HEADING_LEN);
#else
    mavlink_oem7_heading_t packet;
    packet.sol_status = sol_status;
    packet.pos_type = pos_type;
    packet.length = length;
    packet.heading = heading;
    packet.pitch = pitch;
    packet.hdg_std_dev = hdg_std_dev;
    packet.ptch_std_dev = ptch_std_dev;

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_HEADING_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_HEADING;
#if MAVLINK_CRC_EXTRA
    return mavlink_finalize_message_buffer(msg, system_id, component_id, _status, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN, MAVLINK_MSG_ID_OEM7_HEADING_CRC);
#else
    return mavlink_finalize_message_buffer(msg, system_id, component_id, _status, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN);
#endif
}

/**
 * @brief Pack a oem7_heading message on a channel
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param chan The MAVLink channel this message will be sent over
 * @param msg The MAVLink message to compress the data into
 * @param sol_status  DUALANTENNAHEADING solution status
 * @param pos_type  DUALANTENNAHEADING position type
 * @param length  DUALANTENNAHEADING baseline length in meters
 * @param heading  DUALANTENNAHEADING heading in degree(0 ~ 359.999)
 * @param pitch  DUALANTENNAHEADING pitch (+-90 degrees)
 * @param hdg_std_dev  DUALANTENNAHEADING heading standard deviation in degrees
 * @param ptch_std_dev  DUALANTENNAHEADING pitch standard deviation in degrees
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_oem7_heading_pack_chan(uint8_t system_id, uint8_t component_id, uint8_t chan,
                               mavlink_message_t* msg,
                                   uint32_t sol_status,uint32_t pos_type,float length,float heading,float pitch,float hdg_std_dev,float ptch_std_dev)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_HEADING_LEN];
    _mav_put_uint32_t(buf, 0, sol_status);
    _mav_put_uint32_t(buf, 4, pos_type);
    _mav_put_float(buf, 8, length);
    _mav_put_float(buf, 12, heading);
    _mav_put_float(buf, 16, pitch);
    _mav_put_float(buf, 20, hdg_std_dev);
    _mav_put_float(buf, 24, ptch_std_dev);

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), buf, MAVLINK_MSG_ID_OEM7_HEADING_LEN);
#else
    mavlink_oem7_heading_t packet;
    packet.sol_status = sol_status;
    packet.pos_type = pos_type;
    packet.length = length;
    packet.heading = heading;
    packet.pitch = pitch;
    packet.hdg_std_dev = hdg_std_dev;
    packet.ptch_std_dev = ptch_std_dev;

        memcpy(_MAV_PAYLOAD_NON_CONST(msg), &packet, MAVLINK_MSG_ID_OEM7_HEADING_LEN);
#endif

    msg->msgid = MAVLINK_MSG_ID_OEM7_HEADING;
    return mavlink_finalize_message_chan(msg, system_id, component_id, chan, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN, MAVLINK_MSG_ID_OEM7_HEADING_CRC);
}

/**
 * @brief Encode a oem7_heading struct
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param msg The MAVLink message to compress the data into
 * @param oem7_heading C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_heading_encode(uint8_t system_id, uint8_t component_id, mavlink_message_t* msg, const mavlink_oem7_heading_t* oem7_heading)
{
    return mavlink_msg_oem7_heading_pack(system_id, component_id, msg, oem7_heading->sol_status, oem7_heading->pos_type, oem7_heading->length, oem7_heading->heading, oem7_heading->pitch, oem7_heading->hdg_std_dev, oem7_heading->ptch_std_dev);
}

/**
 * @brief Encode a oem7_heading struct on a channel
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param chan The MAVLink channel this message will be sent over
 * @param msg The MAVLink message to compress the data into
 * @param oem7_heading C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_heading_encode_chan(uint8_t system_id, uint8_t component_id, uint8_t chan, mavlink_message_t* msg, const mavlink_oem7_heading_t* oem7_heading)
{
    return mavlink_msg_oem7_heading_pack_chan(system_id, component_id, chan, msg, oem7_heading->sol_status, oem7_heading->pos_type, oem7_heading->length, oem7_heading->heading, oem7_heading->pitch, oem7_heading->hdg_std_dev, oem7_heading->ptch_std_dev);
}

/**
 * @brief Encode a oem7_heading struct with provided status structure
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param status MAVLink status structure
 * @param msg The MAVLink message to compress the data into
 * @param oem7_heading C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_oem7_heading_encode_status(uint8_t system_id, uint8_t component_id, mavlink_status_t* _status, mavlink_message_t* msg, const mavlink_oem7_heading_t* oem7_heading)
{
    return mavlink_msg_oem7_heading_pack_status(system_id, component_id, _status, msg,  oem7_heading->sol_status, oem7_heading->pos_type, oem7_heading->length, oem7_heading->heading, oem7_heading->pitch, oem7_heading->hdg_std_dev, oem7_heading->ptch_std_dev);
}

/**
 * @brief Send a oem7_heading message
 * @param chan MAVLink channel to send the message
 *
 * @param sol_status  DUALANTENNAHEADING solution status
 * @param pos_type  DUALANTENNAHEADING position type
 * @param length  DUALANTENNAHEADING baseline length in meters
 * @param heading  DUALANTENNAHEADING heading in degree(0 ~ 359.999)
 * @param pitch  DUALANTENNAHEADING pitch (+-90 degrees)
 * @param hdg_std_dev  DUALANTENNAHEADING heading standard deviation in degrees
 * @param ptch_std_dev  DUALANTENNAHEADING pitch standard deviation in degrees
 */
#ifdef MAVLINK_USE_CONVENIENCE_FUNCTIONS

static inline void mavlink_msg_oem7_heading_send(mavlink_channel_t chan, uint32_t sol_status, uint32_t pos_type, float length, float heading, float pitch, float hdg_std_dev, float ptch_std_dev)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char buf[MAVLINK_MSG_ID_OEM7_HEADING_LEN];
    _mav_put_uint32_t(buf, 0, sol_status);
    _mav_put_uint32_t(buf, 4, pos_type);
    _mav_put_float(buf, 8, length);
    _mav_put_float(buf, 12, heading);
    _mav_put_float(buf, 16, pitch);
    _mav_put_float(buf, 20, hdg_std_dev);
    _mav_put_float(buf, 24, ptch_std_dev);

    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_HEADING, buf, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN, MAVLINK_MSG_ID_OEM7_HEADING_CRC);
#else
    mavlink_oem7_heading_t packet;
    packet.sol_status = sol_status;
    packet.pos_type = pos_type;
    packet.length = length;
    packet.heading = heading;
    packet.pitch = pitch;
    packet.hdg_std_dev = hdg_std_dev;
    packet.ptch_std_dev = ptch_std_dev;

    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_HEADING, (const char *)&packet, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN, MAVLINK_MSG_ID_OEM7_HEADING_CRC);
#endif
}

/**
 * @brief Send a oem7_heading message
 * @param chan MAVLink channel to send the message
 * @param struct The MAVLink struct to serialize
 */
static inline void mavlink_msg_oem7_heading_send_struct(mavlink_channel_t chan, const mavlink_oem7_heading_t* oem7_heading)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    mavlink_msg_oem7_heading_send(chan, oem7_heading->sol_status, oem7_heading->pos_type, oem7_heading->length, oem7_heading->heading, oem7_heading->pitch, oem7_heading->hdg_std_dev, oem7_heading->ptch_std_dev);
#else
    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_HEADING, (const char *)oem7_heading, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN, MAVLINK_MSG_ID_OEM7_HEADING_CRC);
#endif
}

#if MAVLINK_MSG_ID_OEM7_HEADING_LEN <= MAVLINK_MAX_PAYLOAD_LEN
/*
  This variant of _send() can be used to save stack space by re-using
  memory from the receive buffer.  The caller provides a
  mavlink_message_t which is the size of a full mavlink message. This
  is usually the receive buffer for the channel, and allows a reply to an
  incoming message with minimum stack space usage.
 */
static inline void mavlink_msg_oem7_heading_send_buf(mavlink_message_t *msgbuf, mavlink_channel_t chan,  uint32_t sol_status, uint32_t pos_type, float length, float heading, float pitch, float hdg_std_dev, float ptch_std_dev)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    char *buf = (char *)msgbuf;
    _mav_put_uint32_t(buf, 0, sol_status);
    _mav_put_uint32_t(buf, 4, pos_type);
    _mav_put_float(buf, 8, length);
    _mav_put_float(buf, 12, heading);
    _mav_put_float(buf, 16, pitch);
    _mav_put_float(buf, 20, hdg_std_dev);
    _mav_put_float(buf, 24, ptch_std_dev);

    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_HEADING, buf, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN, MAVLINK_MSG_ID_OEM7_HEADING_CRC);
#else
    mavlink_oem7_heading_t *packet = (mavlink_oem7_heading_t *)msgbuf;
    packet->sol_status = sol_status;
    packet->pos_type = pos_type;
    packet->length = length;
    packet->heading = heading;
    packet->pitch = pitch;
    packet->hdg_std_dev = hdg_std_dev;
    packet->ptch_std_dev = ptch_std_dev;

    _mav_finalize_message_chan_send(chan, MAVLINK_MSG_ID_OEM7_HEADING, (const char *)packet, MAVLINK_MSG_ID_OEM7_HEADING_MIN_LEN, MAVLINK_MSG_ID_OEM7_HEADING_LEN, MAVLINK_MSG_ID_OEM7_HEADING_CRC);
#endif
}
#endif

#endif

// MESSAGE OEM7_HEADING UNPACKING


/**
 * @brief Get field sol_status from oem7_heading message
 *
 * @return  DUALANTENNAHEADING solution status
 */
static inline uint32_t mavlink_msg_oem7_heading_get_sol_status(const mavlink_message_t* msg)
{
    return _MAV_RETURN_uint32_t(msg,  0);
}

/**
 * @brief Get field pos_type from oem7_heading message
 *
 * @return  DUALANTENNAHEADING position type
 */
static inline uint32_t mavlink_msg_oem7_heading_get_pos_type(const mavlink_message_t* msg)
{
    return _MAV_RETURN_uint32_t(msg,  4);
}

/**
 * @brief Get field length from oem7_heading message
 *
 * @return  DUALANTENNAHEADING baseline length in meters
 */
static inline float mavlink_msg_oem7_heading_get_length(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  8);
}

/**
 * @brief Get field heading from oem7_heading message
 *
 * @return  DUALANTENNAHEADING heading in degree(0 ~ 359.999)
 */
static inline float mavlink_msg_oem7_heading_get_heading(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  12);
}

/**
 * @brief Get field pitch from oem7_heading message
 *
 * @return  DUALANTENNAHEADING pitch (+-90 degrees)
 */
static inline float mavlink_msg_oem7_heading_get_pitch(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  16);
}

/**
 * @brief Get field hdg_std_dev from oem7_heading message
 *
 * @return  DUALANTENNAHEADING heading standard deviation in degrees
 */
static inline float mavlink_msg_oem7_heading_get_hdg_std_dev(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  20);
}

/**
 * @brief Get field ptch_std_dev from oem7_heading message
 *
 * @return  DUALANTENNAHEADING pitch standard deviation in degrees
 */
static inline float mavlink_msg_oem7_heading_get_ptch_std_dev(const mavlink_message_t* msg)
{
    return _MAV_RETURN_float(msg,  24);
}

/**
 * @brief Decode a oem7_heading message into a struct
 *
 * @param msg The message to decode
 * @param oem7_heading C-struct to decode the message contents into
 */
static inline void mavlink_msg_oem7_heading_decode(const mavlink_message_t* msg, mavlink_oem7_heading_t* oem7_heading)
{
#if MAVLINK_NEED_BYTE_SWAP || !MAVLINK_ALIGNED_FIELDS
    oem7_heading->sol_status = mavlink_msg_oem7_heading_get_sol_status(msg);
    oem7_heading->pos_type = mavlink_msg_oem7_heading_get_pos_type(msg);
    oem7_heading->length = mavlink_msg_oem7_heading_get_length(msg);
    oem7_heading->heading = mavlink_msg_oem7_heading_get_heading(msg);
    oem7_heading->pitch = mavlink_msg_oem7_heading_get_pitch(msg);
    oem7_heading->hdg_std_dev = mavlink_msg_oem7_heading_get_hdg_std_dev(msg);
    oem7_heading->ptch_std_dev = mavlink_msg_oem7_heading_get_ptch_std_dev(msg);
#else
        uint8_t len = msg->len < MAVLINK_MSG_ID_OEM7_HEADING_LEN? msg->len : MAVLINK_MSG_ID_OEM7_HEADING_LEN;
        memset(oem7_heading, 0, MAVLINK_MSG_ID_OEM7_HEADING_LEN);
    memcpy(oem7_heading, _MAV_PAYLOAD(msg), len);
#endif
}
