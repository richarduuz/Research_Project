package com.example.wifitester;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.text.format.Formatter;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.util.List;

import ru.alexbykov.nopermission.PermissionHelper;

public class MainActivity extends AppCompatActivity {

    TextView txtWifiInfo;
    Button btnInfo;

    private PermissionHelper permissionHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txtWifiInfo = (TextView) findViewById(R.id.xml_wifi_info);
        btnInfo = (Button) findViewById(R.id.xml_button1);

    }

    public String getWifiInformation(View view) {

        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        ConnectivityManager mConnectivityManager = (ConnectivityManager) this.getApplicationContext().getSystemService(Context.CONNECTIVITY_SERVICE);

        WifiInfo wifiInfo = wifiManager.getConnectionInfo();

//        System.out.println(wifiInfo.toString());

        int ip = wifiInfo.getIpAddress();
        String formatIP = Formatter.formatIpAddress(ip);
        String bssid = wifiInfo.getBSSID();
//        System.out.println(bssid);
        String ssid = wifiInfo.getSSID();


        String wifiStr = "IP address: " + formatIP +
                "\n" + "BSSID(router MAC): " + bssid +
                "\n" + "SSID: " + ssid;

        txtWifiInfo.setText(wifiStr);

        return formatIP;
    }

    public void getWifiList(View view) {
        final WifiManager wifiManager = (WifiManager)
                getApplicationContext().getSystemService(Context.WIFI_SERVICE);

        BroadcastReceiver wifiScanReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context c, Intent intent) {
                boolean success = intent.getBooleanExtra(
                        WifiManager.EXTRA_RESULTS_UPDATED, false);
                if (success) {
                    List<ScanResult> results = wifiManager.getScanResults();

//                    System.out.println(results);
//                    System.out.println(results.get(0).BSSID);

                    String wifiListSSID = "";

                    for (int i = 0; i < results.size(); i++) {
                        if(results.get(i).SSID.equals("UniWireless")){
                            wifiListSSID += results.get(i).SSID + ", " + results.get(i).BSSID + ", " + results.get(i).level + "\n";

                        }
                    }

                    List<ScanResult> wifiList = wifiManager.getScanResults();
                    for (ScanResult scanResult : wifiList) {
                        int level = WifiManager.calculateSignalLevel(scanResult.level, 5);
                        System.out.println("Level is " + level + " out of 5");
                    }

                    txtWifiInfo.setText(wifiListSSID);

//                    System.out.println("success to scan");
//                    scanSuccess();
                } else {
                    // scan failure handling

                    System.out.println("fail to scan");
//                    scanFailure();
                }
            }
        };

        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
        getApplicationContext().registerReceiver(wifiScanReceiver, intentFilter);

        boolean success = wifiManager.startScan();
        if (!success) {
            // scan failure handling
            scanFailure();
        }
    }

    private void scanSuccess() {

        System.out.println("success to scan");
    }

    private void scanFailure() {
        System.out.println("fail to scan");
    }

}