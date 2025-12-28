@Dao
public interface SensorDao {

    @Query("SELECT * FROM SensorHistory ORDER BY timestamp DESC")
    List<SensorHistory> getAll();

    @Insert
    void insertAll(List<SensorHistory> list);

    @Query("SELECT * FROM SensorHistory ORDER BY timestamp DESC")
    List<SensorHistory> getAllSync();
}
