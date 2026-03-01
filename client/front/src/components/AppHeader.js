// src/components/AppHeader.js
import React from "react";
import { Layout, Button, Tooltip } from "antd";
import { SunOutlined, MoonOutlined, SettingOutlined } from "@ant-design/icons";
import "./AppHeader.css";

const { Header } = Layout;

export default function AppHeader({ theme, toggleTheme, onOpenSettings, t }) {
  return (
    <Header className="app-header">
      {/* 标题国际化 */}
      <div className="title">{t.appTitle}</div>

      <div className="header-right">
        {/* 主题切换 */}
        <Tooltip title={t.switchTheme || "切换主题"}>
          <Button
            shape="circle"
            icon={theme === "light" ? <MoonOutlined /> : <SunOutlined />}
            onClick={toggleTheme}
          />
        </Tooltip>

        {/* 设置按钮 */}
        <Tooltip title={t.settings}>
          <Button
            shape="circle"
            icon={<SettingOutlined />}
            onClick={onOpenSettings}
          />
        </Tooltip>

        {/* 登出 */}
        <Button className="logout-btn" href="/login">
          {t.logout}
        </Button>
      </div>
    </Header>
  );
}
