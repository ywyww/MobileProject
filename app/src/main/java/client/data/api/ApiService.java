public interface ApiService {

    @GET("status")
    Call<StatusResponse> getStatus();

    @GET("sensor/history")
    Call<List<SensorHistory>> getHistory();

    @POST("relay/mode")
    Call<Void> setMode(@Body RelayModeRequest request);
}
