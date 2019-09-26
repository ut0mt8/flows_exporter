create table flow_out(
        id INT(4) UNSIGNED NOT NULL AUTO_INCREMENT,
        tag INT(4) UNSIGNED NOT NULL,
        as_src INT(4) UNSIGNED NOT NULL,
        as_dst INT(4) UNSIGNED NOT NULL,
        peer_ip_src CHAR(45) NOT NULL,
        peer_ip_dst CHAR(45) NOT NULL,
        as_path CHAR(40) NOT NULL,
        ip_src CHAR(45) NOT NULL,
        ip_dst CHAR(45) NOT NULL,
        port_src INT(2) UNSIGNED NOT NULL,
        port_dst INT(2) UNSIGNED NOT NULL,
        iface_in INT(4) UNSIGNED NOT NULL,
        iface_out INT(4) UNSIGNED NOT NULL,
        ip_proto CHAR(6) NOT NULL,
        tcp_flags INT(4) UNSIGNED NOT NULL,
        packets INT UNSIGNED NOT NULL,
        bytes BIGINT UNSIGNED NOT NULL,
        country_ip_src CHAR(2) NOT NULL,
        country_ip_dst CHAR(2) NOT NULL,
        stamp_inserted DATETIME NOT NULL,
        stamp_updated DATETIME,
        PRIMARY KEY (id,stamp_inserted),
        INDEX a (as_dst),
        INDEX b (as_src),
        INDEX c (ip_src),
        INDEX d (ip_dst),
        INDEX e (iface_in),
        INDEX f (iface_out)
) ENGINE=InnoDB AUTO_INCREMENT=1
PARTITION BY LIST (hour(stamp_inserted))(
PARTITION p00 VALUES IN (0),
PARTITION p01 VALUES IN (1),
PARTITION p02 VALUES IN (2),
PARTITION p03 VALUES IN (3),
PARTITION p04 VALUES IN (4),
PARTITION p05 VALUES IN (5),
PARTITION p06 VALUES IN (6),
PARTITION p07 VALUES IN (7),
PARTITION p08 VALUES IN (8),
PARTITION p09 VALUES IN (9),
PARTITION p10 VALUES IN (10),
PARTITION p11 VALUES IN (11),
PARTITION p12 VALUES IN (12),
PARTITION p13 VALUES IN (13),
PARTITION p14 VALUES IN (14),
PARTITION p15 VALUES IN (15),
PARTITION p16 VALUES IN (16),
PARTITION p17 VALUES IN (17),
PARTITION p18 VALUES IN (18),
PARTITION p19 VALUES IN (19),
PARTITION p20 VALUES IN (20),
PARTITION p21 VALUES IN (21),
PARTITION p22 VALUES IN (22),
PARTITION p23 VALUES IN (23));