Assignment 2 - Smart Home Monitoring System
Using Observer Pattern + Factory Pattern

=========================================
How to Compile
=========================================
在项目根目录下运行：

    javac *.java

确保所有 .java 文件在同一目录下（无 package 声明）。

=========================================
How to Run
=========================================
编译完成后运行主程序：

    java SmartHomeApp

程序将根据 SmartHomeApp.java 中的 roomType 变量加载不同房间的监控配置。

=========================================
How to Switch Between Dormitory and Laboratory
=========================================
打开 SmartHomeApp.java，找到如下代码：

    String roomType = "dormitory";   // 或 "laboratory"

修改为：

    String roomType = "laboratory";

即可切换为实验室监控配置（更严格的烟雾阈值）。

=========================================
Explanation: How Observer and Factory Patterns Interact
=========================================
本系统使用 Observer 模式让 MonitoringHub 与各个显示面板解耦。当数据上报时，Hub 不需要知道具体有哪些面板，只需通知所有已注册的观察者。

Factory 模式负责根据“房间类型”（宿舍或实验室）自动创建合适的面板组合，并在内部把这些面板注册到 MonitoringHub。这种方式使主程序不需要直接创建或注册面板，只需选择工厂即可。

工厂负责“创建与配置”，监控中心负责“广播通知”，面板负责“接收并响应”，三者独立又协作，形成灵活可扩展的架构。

=========================================
File List
=========================================
Subject.java
Observer.java
SensorEvent.java
MonitoringHub.java
RealtimePanel.java
AlarmPanel.java
RoomConfigFactory.java
DormRoomFactory.java
LabRoomFactory.java
FactoryConfig.java
SmartHomeApp.java
README.txt




                           +--------------------+
                           |    Subject<T>      |
                           +--------------------+
                           | + registerObserver()|
                           | + removeObserver()  |
                           | + notifyObservers() |
                           +----------^----------+
                                      |
                                      |
                       +--------------+----------------+
                       | MonitoringHub (Subject<T>)    |
                       +--------------------------------+
                       | - observers: List<Observer<T>> |
                       +--------------------------------+
                       | + reportData()                  |
                       | + registerObserver()            |
                       | + removeObserver()              |
                       | + notifyObservers()             |
                       +---------------+-----------------+
                                       |
                                       |
                            receives SensorEvent
                                       |
                                       v
                          +------------------------+
                          |     SensorEvent        |
                          +------------------------+
                          | - sensorType: String   |
                          | - roomName:  String    |
                          | - value: double        |
                          +------------------------+
                          | + getters              |
                          | + toString()           |
                          +------------------------+

                           Observers
       +-------------------------------------------------------+
       |                                                       |
       v                                                       v
+---------------------+                          +----------------------+
| RealtimePanel       |                          | AlarmPanel           |
+---------------------+                          +----------------------+
| + panelName         |                          | + panelName          |
+---------------------+                          | + smokeThreshold     |
| + update(event)     |                          +----------------------+
|  prints current     |                          | + update(event)      |
|  reading            |                          |  checks smoke value  |
+---------------------+                          +----------------------+

                         Factories
   +---------------------------------------------------------------+
   |                         RoomConfigFactory                     |
   +---------------------------------------------------------------+
   | + setupPanels(hub, roomName)                                  |
   +--------------^-------------------------------^-----------------+
                  |                               |
                  |                               |
     +--------------------------+     +----------------------------+
     |    DormRoomFactory       |     |    LabRoomFactory         |
     +--------------------------+     +----------------------------+
     | creates:                 |     | creates:                  |
     | - RealtimePanel          |     | - RealtimePanel           |
     | - AlarmPanel(th=50.0)    |     | - AlarmPanel(th=20.0)     |
     | and registers them       |     | and registers them        |
     +--------------------------+     +----------------------------+

                          Factory Selector
                     +--------------------------+
                     |     FactoryConfig        |
                     +--------------------------+
                     | + getFactory(roomType)   |
                     +-------------^------------+
                                   |
                           selected by
                                   |
                           +----------------+
                           | SmartHomeApp    |
                           +----------------+
                           | main():         |
                           | - create hub    |
                           | - choose factory|
                           | - factory.setup |
                           | - reportData()  |
                           +----------------+
