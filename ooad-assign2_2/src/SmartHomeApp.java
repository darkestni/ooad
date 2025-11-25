public class SmartHomeApp {

    public static void main(String[] args) {
        // 1. 创建监控中心
        MonitoringHub hub = new MonitoringHub();

        // 2. 选择房间类型（你可以改成 "laboratory" 测试实验室配置）
        String roomType = "dormitory";  // 或 "laboratory"
        String roomName = "Dormitory A"; // 对应房间名称，例如 "Laboratory 1"

        // 3. 通过 FactoryConfig 获取对应房间类型的工厂
        RoomConfigFactory factory = FactoryConfig.getFactory(roomType);

        // 4. 使用工厂为这个房间创建并注册面板
        factory.setupPanels(hub, roomName);

        // 5. 模拟正常情况
        System.out.println("--- Normal Conditions ---");
        hub.reportData("temperature", roomName, 23.5);
        hub.reportData("smoke", roomName, 15.0);

        // 6. 模拟烟雾报警
        System.out.println("\n--- Smoke Alert ---");
        hub.reportData("smoke", roomName, 75.0);
    }
}
