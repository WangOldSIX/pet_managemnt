-- ============================================
-- 宠物管理系统数据库初始化脚本
-- 数据库课程设计 - MySQL 8.0
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS pet_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE pet_management;

-- ============================================
-- 1. 用户表 (users)
-- 说明：存储系统用户信息，包含管理员、宠物主人、员工三种角色
-- ============================================
CREATE TABLE `users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID，主键，自增',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名，唯一，用于登录',
  `password` VARCHAR(255) NOT NULL COMMENT '密码，bcrypt加密存储',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱地址，用于通知',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号，用于联系',
  `real_name` VARCHAR(50) DEFAULT NULL COMMENT '真实姓名',
  `role` ENUM('admin', 'owner', 'staff') NOT NULL DEFAULT 'owner' COMMENT '角色：admin-管理员，owner-宠物主人，staff-员工',
  `avatar` VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用：1-启用，0-禁用',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除：1-已删除，0-未删除（软删除）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  KEY `idx_email` (`email`),
  KEY `idx_phone` (`phone`),
  KEY `idx_role` (`role`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 2. 宠物档案表 (pets)
-- 说明：存储宠物的基本信息，与用户表是一对多关系
-- ============================================
CREATE TABLE `pets` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '宠物ID，主键，自增',
  `owner_id` BIGINT UNSIGNED NOT NULL COMMENT '主人ID，外键关联users表',
  `name` VARCHAR(50) NOT NULL COMMENT '宠物名称',
  `species` VARCHAR(50) NOT NULL COMMENT '物种：猫、狗、其他',
  `breed` VARCHAR(50) DEFAULT NULL COMMENT '品种',
  `gender` ENUM('male', 'female') NOT NULL COMMENT '性别：male-公，female-母',
  `birth_date` DATE DEFAULT NULL COMMENT '出生日期',
  `weight` DECIMAL(5,2) DEFAULT NULL COMMENT '体重，单位kg',
  `color` VARCHAR(50) DEFAULT NULL COMMENT '毛色',
  `health_status` TEXT COMMENT '健康状况描述',
  `special_notes` TEXT COMMENT '特殊备注（如过敏史、习惯等）',
  `avatar` VARCHAR(255) DEFAULT NULL COMMENT '宠物照片URL',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除：1-已删除，0-未删除（软删除）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_owner_id` (`owner_id`),
  KEY `idx_species` (`species`),
  KEY `idx_gender` (`gender`),
  CONSTRAINT `fk_pets_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='宠物档案表';

-- ============================================
-- 3. 宠物服务表 (services)
-- 说明：存储系统提供的各项服务信息
-- ============================================
CREATE TABLE `services` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '服务ID，主键，自增',
  `name` VARCHAR(100) NOT NULL COMMENT '服务名称',
  `description` TEXT COMMENT '服务详细描述',
  `category` VARCHAR(50) NOT NULL COMMENT '服务类别：美容、医疗、寄养、训练等',
  `price` DECIMAL(10,2) NOT NULL COMMENT '服务价格，单位元',
  `duration` INT DEFAULT NULL COMMENT '服务时长，单位分钟',
  `image` VARCHAR(255) DEFAULT NULL COMMENT '服务图片URL',
  `is_available` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否上架：1-上架，0-下架',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除：1-已删除，0-未删除（软删除）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category`),
  KEY `idx_available` (`is_available`),
  KEY `idx_price` (`price`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='宠物服务表';

-- ============================================
-- 4. 订单表 (orders)
-- 说明：存储宠物服务的订单信息
-- ============================================
CREATE TABLE `orders` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单ID，主键，自增',
  `order_no` VARCHAR(50) NOT NULL COMMENT '订单号，唯一',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID，外键关联users表',
  `pet_id` BIGINT UNSIGNED NOT NULL COMMENT '宠物ID，外键关联pets表',
  `service_id` BIGINT UNSIGNED NOT NULL COMMENT '服务ID，外键关联services表',
  `staff_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '服务员工ID，外键关联users表',
  `appointment_time` DATETIME DEFAULT NULL COMMENT '预约时间',
  `status` ENUM('pending', 'confirmed', 'in_progress', 'completed', 'cancelled') NOT NULL DEFAULT 'pending' COMMENT '订单状态：pending-待确认，confirmed-已确认，in_progress-进行中，completed-已完成，cancelled-已取消',
  `total_amount` DECIMAL(10,2) NOT NULL COMMENT '订单总额',
  `notes` TEXT COMMENT '订单备注',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除：1-已删除，0-未删除（软删除）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_pet_id` (`pet_id`),
  KEY `idx_service_id` (`service_id`),
  KEY `idx_staff_id` (`staff_id`),
  KEY `idx_status` (`status`),
  KEY `idx_appointment_time` (`appointment_time`),
  CONSTRAINT `fk_orders_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_orders_pet` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_orders_service` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_orders_staff` FOREIGN KEY (`staff_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- ============================================
-- 5. 寄养表 (boardings)
-- 说明：存储宠物寄养的详细信息（扩展表）
-- ============================================
CREATE TABLE `boardings` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '寄养ID，主键，自增',
  `order_id` BIGINT UNSIGNED NOT NULL COMMENT '订单ID，外键关联orders表',
  `pet_id` BIGINT UNSIGNED NOT NULL COMMENT '宠物ID，外键关联pets表',
  `staff_id` BIGINT UNSIGNED NOT NULL COMMENT '饲养员ID，外键关联users表',
  `start_date` DATETIME NOT NULL COMMENT '寄养开始时间',
  `end_date` DATETIME NOT NULL COMMENT '寄养结束时间',
  `status` ENUM('scheduled', 'in_progress', 'completed', 'cancelled') NOT NULL DEFAULT 'scheduled' COMMENT '寄养状态：scheduled-已预约，in_progress-进行中，completed-已完成，cancelled-已取消',
  `daily_notes` TEXT COMMENT '每日记录',
  `food_type` VARCHAR(100) DEFAULT NULL COMMENT '食物类型',
  `feeding_schedule` VARCHAR(100) DEFAULT NULL COMMENT '喂食计划',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除：1-已删除，0-未删除（软删除）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_pet_id` (`pet_id`),
  KEY `idx_staff_id` (`staff_id`),
  KEY `idx_dates` (`start_date`, `end_date`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_boardings_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_boardings_pet` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_boardings_staff` FOREIGN KEY (`staff_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='寄养表';

-- ============================================
-- 6. 健康记录表 (health_records)
-- 说明：存储宠物健康检查和治疗记录（扩展表）
-- ============================================
CREATE TABLE `health_records` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '健康记录ID，主键，自增',
  `pet_id` BIGINT UNSIGNED NOT NULL COMMENT '宠物ID，外键关联pets表',
  `vet_id` BIGINT UNSIGNED NOT NULL COMMENT '兽医ID，外键关联users表',
  `check_date` DATETIME NOT NULL COMMENT '检查日期',
  `type` ENUM('checkup', 'treatment', 'vaccination', 'surgery') NOT NULL COMMENT '记录类型：checkup-检查，treatment-治疗，vaccination-疫苗，surgery-手术',
  `description` TEXT COMMENT '详细描述',
  `diagnosis` TEXT COMMENT '诊断结果',
  `prescription` TEXT COMMENT '处方信息',
  `notes` TEXT COMMENT '备注',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除：1-已删除，0-未删除（软删除）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_pet_id` (`pet_id`),
  KEY `idx_vet_id` (`vet_id`),
  KEY `idx_check_date` (`check_date`),
  KEY `idx_type` (`type`),
  CONSTRAINT `fk_health_pet` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_health_vet` FOREIGN KEY (`vet_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='健康记录表';

-- ============================================
-- 插入初始数据
-- ============================================

-- 插入管理员用户（密码：admin123，已bcrypt加密）
INSERT INTO `users` (`username`, `password`, `email`, `real_name`, `role`, `is_active`) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYqWqxVbJ.', 'admin@pet.com', '系统管理员', 'admin', 1),
('owner001', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYqWqxVbJ.', 'owner001@pet.com', '张三', 'owner', 1),
('staff001', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYqWqxVbJ.', 'staff001@pet.com', '李四', 'staff', 1);

-- 插入测试宠物数据
INSERT INTO `pets` (`owner_id`, `name`, `species`, `breed`, `gender`, `birth_date`, `weight`, `color`, `health_status`) VALUES
(2, '小白', '猫', '英短', 'female', '2023-01-15', 4.5, '白色', '健康'),
(2, '大黄', '狗', '金毛', 'male', '2022-06-20', 25.0, '金色', '健康，已完成疫苗'),
(2, '小黑', '猫', '美短', 'male', '2023-03-10', 5.2, '黑色', '健康');

-- 插入测试服务数据
INSERT INTO `services` (`name`, `description`, `category`, `price`, `duration`, `is_available`) VALUES
('宠物美容', '基础洗护、修剪指甲、清理耳朵、梳理毛发', '美容', 88.00, 60, 1),
('宠物洗澡', '深度清洁、吹干', '美容', 48.00, 45, 1),
('宠物寄养（天）', '专业寄养服务，包含喂食、遛狗、陪伴', '寄养', 128.00, NULL, 1),
('宠物训练', '基础服从性训练、行为矫正', '训练', 200.00, 90, 1),
('疫苗接种', '狂犬病疫苗、多联疫苗', '医疗', 98.00, 30, 1),
('驱虫服务', '体内外驱虫', '医疗', 68.00, 20, 1),
('体检套餐', '全面健康体检', '医疗', 288.00, 60, 1);

-- 插入测试订单数据
INSERT INTO `orders` (`order_no`, `user_id`, `pet_id`, `service_id`, `staff_id`, `appointment_time`, `status`, `total_amount`, `notes`) VALUES
('ORD2025010110001', 2, 1, 1, 3, '2025-02-05 14:00:00', 'confirmed', 88.00, '首次美容，需要特别注意'),
('ORD2025010210002', 2, 2, 3, 3, '2025-02-10 09:00:00', 'pending', 128.00, '寄养3天'),
('ORD2025010310003', 2, 3, 5, 3, '2025-02-08 10:00:00', 'completed', 98.00, '年度疫苗接种');

COMMIT;
