public class ApiClient {

    private static final String BASE_URL = "http://192.168.0.100:8080/";

    public static ApiService getApi() {
        return new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(ApiService.class);
    }
}
