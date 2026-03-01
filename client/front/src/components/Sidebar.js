// src/components/Sidebar.js

import React from "react";
import { Upload, Button, List, Typography, Popconfirm, message } from "antd";
import {
  UploadOutlined,
  FilePdfOutlined,
  FileImageOutlined,
  FileWordOutlined,
  FileExcelOutlined,
  FilePptOutlined,
  DeleteOutlined,
} from "@ant-design/icons";

import "./Sidebar.css";

const { Text } = Typography;

// 🔥 支持的所有 MIME 类型
const allowedTypes = [
  // PDF
  "application/pdf",

  // Images
  "image/png",
  "image/jpg",
  "image/jpeg",
  "image/webp",
  "image/bmp",

  // Word
  "application/msword", // .doc
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document", // .docx

  // PowerPoint
  "application/vnd.ms-powerpoint", // .ppt
  "application/vnd.openxmlformats-officedocument.presentationml.presentation", // .pptx

  // Excel
  "application/vnd.ms-excel", // .xls
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", // .xlsx
];

export default function Sidebar({
  uploadedFiles = [],
  onUploadTextbook,
  onDeleteFile,
}) {
  const uploadProps = {
    beforeUpload: (file) => {
      if (!allowedTypes.includes(File.type)) {
        message.error("仅支持 PDF / 图片 / Word / PPT / Excel 文件");
        return false;
      }

      if (onUploadTextbook) onUploadTextbook(file);
      return false;
    },
  };
  // 图标选择器
  const getFileIcon = (name, type) => {
    const ext = name.split(".").pop().toLowerCase();

    if (["png", "jpg", "jpeg", "gif", "bmp", "webp"].includes(ext))
      return <FileImageOutlined className="file-icon" />;

    if (ext === "pdf")
      return <FilePdfOutlined className="file-icon red" />;

    if (ext === "doc" || ext === "docx")
      return <FileWordOutlined className="file-icon blue" />;

    if (ext === "ppt" || ext === "pptx")
      return <FilePptOutlined className="file-icon orange" />;

    if (ext === "xls" || ext === "xlsx")
      return <FileExcelOutlined className="file-icon green" />;

    // 默认 PDF 图标
    return <FilePdfOutlined className="file-icon" />;
  };

  return (
    <div className="sidebar-container">
      <h2 className="sidebar-title">📚 我的教材</h2>

      {/* 上传按钮 */}
      <Upload {...uploadProps} showUploadList={false}>
        <Button className="upload-btn" icon={<UploadOutlined />}>
          上传文件
        </Button>
      </Upload>

      {/* 文件列表 */}
      <List
        className="file-list"
        dataSource={uploadedFiles}
        locale={{ emptyText: "暂无上传文件" }}
        renderItem={(item) => (
          <List.Item
            className="file-item"
            actions={[
              <Popconfirm
                title="确认删除此文件吗？"
                onConfirm={() => onDeleteFile && onDeleteFile(item)}
                okText="删除"
                cancelText="取消"
              >
                <DeleteOutlined className="delete-btn" />
              </Popconfirm>,
            ]}
          >
            <List.Item.Meta
              avatar={getFileIcon(item.name)}
              title={<Text className="file-name">{item.name}</Text>}
            />
          </List.Item>
        )}
      />
    </div>
  );
}
