public class LabRoomFactory implements RoomConfigFactory {

    @Override
    public void setupPanels(MonitoringHub hub, String roomName) {
        // 1. 创建实时显示面板
        RealtimePanel realtimePanel = new RealtimePanel("Lab Display");
        hub.registerObserver(realtimePanel);  // 注册观察者

        // 2. 创建报警面板（阈值更低，更敏感）
        AlarmPanel alarmPanel = new AlarmPanel("Lab Alarm", 20.0);
        hub.registerObserver(alarmPanel);     // 注册观察者
    }
}
