public class FactoryConfig {

    public static RoomConfigFactory getFactory(String roomType) {
        if (roomType == null) {
            // 默认用宿舍配置
            return new DormRoomFactory();
        }

        if (roomType.equalsIgnoreCase("dormitory")) {
            return new DormRoomFactory();
        } else if (roomType.equalsIgnoreCase("laboratory")) {
            return new LabRoomFactory();
        } else {
            // 未知类型也默认宿舍
            return new DormRoomFactory();
        }
    }
}
