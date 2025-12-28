@Database(entities = {SensorHistory.class}, version = 1)
public abstract class AppDatabase extends RoomDatabase {

    private static AppDatabase instance;

    public static synchronized AppDatabase get(Context context) {
        if (instance == null) {
            instance = Room.databaseBuilder(
                    context.getApplicationContext(),
                    AppDatabase.class,
                    "sensor.db"
            ).build();
        }
        return instance;
    }

    public abstract SensorDao sensorDao();
}
