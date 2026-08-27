-- 新的用户体系数据库设计
-- Generated: 2026-08-26

CREATE DATABASE IF NOT EXISTS `anxingban`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE `anxingban`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users (子女用户表)
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nickname` varchar(80) NOT NULL COMMENT '昵称',
  `phone` varchar(30) NOT NULL COMMENT '手机号',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希',
  `last_login_at` datetime DEFAULT NULL COMMENT '最后登录时间',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  KEY `idx_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='子女用户表';

-- ----------------------------
-- Table structure for elders (老人表)
-- ----------------------------
DROP TABLE IF EXISTS `elders`;
CREATE TABLE `elders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL COMMENT '姓名',
  `phone` varchar(30) NOT NULL COMMENT '手机号',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希',
  `health_info` text NOT NULL COMMENT '健康信息JSON',
  `interests` text NOT NULL COMMENT '兴趣爱好',
  `wechat_webhook_url` varchar(300) DEFAULT '' COMMENT '企业微信Webhook URL',
  `last_login_at` datetime DEFAULT NULL COMMENT '最后登录时间',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  KEY `idx_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='老人用户表';

-- ----------------------------
-- Table structure for profiles (档案关联表)
-- ----------------------------
DROP TABLE IF EXISTS `profiles`;
CREATE TABLE `profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `elder_id` int NOT NULL COMMENT '老人ID',
  `user_id` int NOT NULL COMMENT '子女用户ID',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_elder_id` (`elder_id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_profiles_elder` FOREIGN KEY (`elder_id`) REFERENCES `elders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_profiles_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='老人-子女关联表';

-- ----------------------------
-- Table structure for trips (行程表)
-- ----------------------------
DROP TABLE IF EXISTS `trips`;
CREATE TABLE `trips` (
  `id` int NOT NULL AUTO_INCREMENT,
  `profile_id` int NOT NULL COMMENT '档案ID',
  `destination` varchar(120) NOT NULL COMMENT '目的地',
  `travel_date` date NOT NULL COMMENT '出行日期',
  `pass_token` varchar(120) NOT NULL COMMENT '通行码令牌',
  `pass_qr_svg` text NOT NULL COMMENT '二维码SVG',
  `status` varchar(20) NOT NULL COMMENT '状态',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pass_token` (`pass_token`),
  KEY `profile_id` (`profile_id`),
  CONSTRAINT `trips_ibfk_1` FOREIGN KEY (`profile_id`) REFERENCES `profiles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='行程表';

-- ----------------------------
-- Table structure for tasks (亲子任务表)
-- ----------------------------
DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `profile_id` int NOT NULL COMMENT '档案ID',
  `trip_id` int NOT NULL COMMENT '行程ID',
  `title` varchar(150) NOT NULL COMMENT '任务标题',
  `description` text NOT NULL COMMENT '任务描述',
  `status` varchar(20) NOT NULL COMMENT '状态',
  `completed_note` text COMMENT '完成备注',
  `photo_url` varchar(400) DEFAULT NULL COMMENT '照片URL',
  `feedback_text` text COMMENT '反馈文本',
  `hearts` int NOT NULL COMMENT '爱心数',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  PRIMARY KEY (`id`),
  KEY `profile_id` (`profile_id`),
  KEY `trip_id` (`trip_id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`profile_id`) REFERENCES `profiles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`trip_id`) REFERENCES `trips` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='亲子任务表';

-- ----------------------------
-- Table structure for sos_records (紧急求助记录表)
-- ----------------------------
DROP TABLE IF EXISTS `sos_records`;
CREATE TABLE `sos_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `profile_id` int NOT NULL COMMENT '档案ID',
  `trip_id` int DEFAULT NULL COMMENT '行程ID',
  `latitude` float DEFAULT NULL COMMENT '纬度',
  `longitude` float DEFAULT NULL COMMENT '经度',
  `network_status` varchar(30) NOT NULL COMMENT '网络状态',
  `health_snapshot` text NOT NULL COMMENT '健康信息快照',
  `sms_status` varchar(30) NOT NULL COMMENT '短信状态',
  `wechat_status` varchar(30) NOT NULL COMMENT '微信状态',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `profile_id` (`profile_id`),
  KEY `trip_id` (`trip_id`),
  CONSTRAINT `sos_records_ibfk_1` FOREIGN KEY (`profile_id`) REFERENCES `profiles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sos_records_ibfk_2` FOREIGN KEY (`trip_id`) REFERENCES `trips` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='SOS紧急求助记录表';

-- ----------------------------
-- Table structure for memory_cards (回忆卡片表)
-- ----------------------------
DROP TABLE IF EXISTS `memory_cards`;
CREATE TABLE `memory_cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int NOT NULL COMMENT '行程ID',
  `title` varchar(120) NOT NULL COMMENT '标题',
  `summary` text NOT NULL COMMENT '摘要',
  `image_url` varchar(400) DEFAULT NULL COMMENT '图片URL',
  `card_json` text NOT NULL COMMENT '卡片JSON数据',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `trip_id` (`trip_id`),
  CONSTRAINT `memory_cards_ibfk_1` FOREIGN KEY (`trip_id`) REFERENCES `trips` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='回忆卡片表';

SET FOREIGN_KEY_CHECKS = 1;
