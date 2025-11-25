public class TestObserver {

    public static void main(String[] args) {
        MonitoringHub hub = new MonitoringHub();

        // 创建两个面板
        RealtimePanel realtimePanel = new RealtimePanel("Test Display");
        AlarmPanel alarmPanel = new AlarmPanel("Test Alarm", 50.0);

        // 注册到 hub
        hub.registerObserver(realtimePanel);
        hub.registerObserver(alarmPanel);

        String roomName = "Test Room";

        System.out.println("--- Normal ---");
        hub.reportData("temperature", roomName, 22.0);
        hub.reportData("smoke", roomName, 30.0);  // 不触发报警

        System.out.println("\n--- Smoke Alert ---");
        hub.reportData("smoke", roomName, 80.0);  // 触发报警
    }
}
