public interface RoomConfigFactory {

    /**
     * 创建并注册本房间类型需要的所有面板
     * 重要：在这个方法里完成对 hub 的 registerObserver 调用
     *
     * @param hub      监控中心（Subject）
     * @param roomName 房间名称（用于显示）
     */
    void setupPanels(MonitoringHub hub, String roomName);
}
