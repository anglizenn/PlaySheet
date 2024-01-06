package com.example.fyp;

import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okio.BufferedSink;
import okio.Okio;

public class LoadingActivity extends AppCompatActivity {
    File file;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.loading);
        file = (File)getIntent().getExtras().get("file");
        connectServer();
    }
    public void connectServer(){
        String postUrl = "http://172.17.3.217:5000";

        RequestBody postBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", file.getName(),
                        RequestBody.create(MediaType.parse("application/pdf"), file))
                .build();

        TextView responseText = findViewById(R.id.loadingMessage);
        responseText.setText("Please wait...");

        postRequest(postUrl, postBody);
    }

    void postRequest(String postUrl, RequestBody postBody) {

        OkHttpClient client = new OkHttpClient();
        OkHttpClient.Builder builder = new OkHttpClient.Builder();
        builder.connectTimeout(10, TimeUnit.SECONDS);
        builder.readTimeout(60, TimeUnit.SECONDS);
        builder.writeTimeout(10, TimeUnit.SECONDS);
        client = builder.build();

        Request request = new Request.Builder()
                .url(postUrl)
                .post(postBody)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                call.cancel();

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Intent i = new Intent(LoadingActivity.this, MainActivity.class);
                        i.putExtra("message", 1);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        overridePendingTransition(0, 0);
                        finish();
                    }
                });
            }

            @Override
            public void onResponse(Call call, final Response response) throws IOException {
                if (!response.isSuccessful()){
                    Intent i = new Intent(LoadingActivity.this, MainActivity.class);
                    i.putExtra("message", 1);
                    i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                    startActivity(i);
                    overridePendingTransition(0, 0);
                    finish();
                }

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        String fileName=file.getName().substring(0, file.getName().length() - 3) + "mid";
                        File downloadedFile = new File(getApplicationContext().getCacheDir(), fileName);
                        try {
                            BufferedSink sink = Okio.buffer(Okio.sink(downloadedFile));
                            sink.writeAll(response.body().source());
                            sink.close();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        if (downloadedFile.length()!=0){
                            Intent i = new Intent(LoadingActivity.this, PlayActivity.class);
                            i.putExtra("song", fileName);
                            startActivity(i);
                            overridePendingTransition(0,0);
                        }

                    }
                });
            }
        });
    }
}
