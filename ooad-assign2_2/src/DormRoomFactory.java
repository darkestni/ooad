public class DormRoomFactory implements RoomConfigFactory {

    @Override
    public void setupPanels(MonitoringHub hub, String roomName) {
        // 1. 创建实时显示面板
        RealtimePanel realtimePanel = new RealtimePanel("Dorm Display");
        hub.registerObserver(realtimePanel);  // 注册观察者

        // 2. 创建报警面板（阈值较高，避免误报）
        AlarmPanel alarmPanel = new AlarmPanel("Dorm Alarm", 50.0);
        hub.registerObserver(alarmPanel);     // 注册观察者
    }
}
