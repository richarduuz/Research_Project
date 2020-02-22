package com.example.faceapp;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;


public class MainActivity extends AppCompatActivity {

    ImageView imageView1;
    ImageView imageView2;
    ImageView imageView3;
    Button button1;
    Button button2;
    Button button3;
    private static final int PICK_IMAGE1 = 100;
    private static final int PICK_IMAGE2 = 200;
    Uri imageUri;

    // server address and port
    String url = "http://34.87.203.105:7888/faceshifter";

    String bitString1;
    String bitString2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageView1 = (ImageView)findViewById(R.id.user_image1);
        button1 = (Button)findViewById(R.id.buttonLoadPicture1);
        button1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openGallery1();
            }
        });


        imageView2 = (ImageView)findViewById(R.id.user_image2);
        button2 = (Button)findViewById(R.id.buttonLoadPicture2);
        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openGallery2();
            }
        });

        button3 = findViewById(R.id.button_sendRequest);

        imageView3 = findViewById(R.id.result_image);

    }

    // open device gallery
    private void openGallery1() {
        Intent gallery = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI);
        startActivityForResult(gallery, PICK_IMAGE1);
    }
    private void openGallery2() {
        Intent gallery = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI);
        startActivityForResult(gallery, PICK_IMAGE2);
    }


    // load images of face and base, convert to bitmap base-64
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && requestCode == PICK_IMAGE1){
            // image data
            imageUri = data.getData();
            System.out.println(imageUri);
            imageView1.setImageURI(imageUri);

            Bitmap bitmap = ((BitmapDrawable)imageView1.getDrawable()).getBitmap();
            ByteArrayOutputStream baos = new ByteArrayOutputStream();// outputstream
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, baos);
            byte[] byteArray = baos.toByteArray();// to byte array
            bitString1 = Base64.encodeToString(byteArray, Base64.DEFAULT);

        } else if(resultCode == RESULT_OK && requestCode == PICK_IMAGE2){
            // image data
            imageUri = data.getData();
            System.out.println(imageUri);
            imageView2.setImageURI(imageUri);

            Bitmap bitmap = ((BitmapDrawable)imageView2.getDrawable()).getBitmap();
            ByteArrayOutputStream baos = new ByteArrayOutputStream();// outputstream
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, baos);
            byte[] byteArray = baos.toByteArray();// to byte array
            bitString2 = Base64.encodeToString(byteArray, Base64.DEFAULT);
        }
    }


    // make okphttp post request (send 2 images as bitmap in base-64
    public void sendRequest(View view){

        OkHttpClient client = new OkHttpClient();

        RequestBody requestBody = new FormBody.Builder()
                .add("source_image", bitString1)
                .add("target_image", bitString2)
                .build();

        Request request = new Request.Builder()
                .url(url)
                .post(requestBody)
                .build();

        Toast.makeText(getApplicationContext(), "Request Sent, Waiting for Result ... ", Toast.LENGTH_LONG).show();

        // async call in thread
        client.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(Call call, IOException e) {
                System.out.println("call failed");
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {

                System.out.println("called");

                if(response.isSuccessful()){

                    System.out.println("call success");

                    final String myResponse = response.body().string();

                    MainActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            System.out.println("response: " + myResponse);
//                            mTextViewResult.setText(myResponse);

                            // get base-64 message of bitmap from json
                            String result = null;
                            try {
                                JSONObject jsonObject = new JSONObject(myResponse);
                                result = jsonObject.getString("image");
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                            // decode and construct image from bitmap
                            byte[] decodedString = Base64.decode(result, Base64.DEFAULT);
                            Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);

                            imageView3.setImageBitmap(decodedByte);
                        }
                    });
                }
            }
        });

    }











}
