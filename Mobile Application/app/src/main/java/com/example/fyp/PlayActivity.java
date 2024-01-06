package com.example.fyp;

import android.content.Intent;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.SeekBar;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.FileInputStream;

public class PlayActivity extends AppCompatActivity {
    MediaPlayer mediaPlayer=new MediaPlayer();
    private int endTime=0, startTime=0, difference=0;
    private boolean setHandler=false;
    ImageButton playBtn;
    ImageButton pauseBtn;
    ImageButton rewindBtn;

    Runnable UpdateSongTime;
    private TextView startText, endText;
    private SeekBar seekBar;
    private Handler handler;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        getSupportActionBar().hide();
        super.onCreate(savedInstanceState);
        setContentView(R.layout.play);
        handler=new Handler();
        playBtn = (ImageButton) findViewById(R.id.playButton);
        pauseBtn = (ImageButton) findViewById(R.id.pauseButton);
        rewindBtn = (ImageButton) findViewById(R.id.rewindButton);
        Button againBtn = (Button) findViewById(R.id.againButton);
        seekBar=(SeekBar) findViewById(R.id.seekBar);
        startText = (TextView) findViewById(R.id.startTime);
        endText = (TextView) findViewById(R.id.endTime);

        mediaPlayer.reset();
        Intent intent  =getIntent();
        String fileName=intent.getStringExtra("song");
        TextView fileDisplay = (TextView) findViewById(R.id.playFileName);
        fileDisplay.setText(fileName.substring(0, fileName.length() - 4));

        try {
            FileInputStream fileInputStream = new FileInputStream(getApplicationContext().getCacheDir() + "/" + fileName);
            mediaPlayer.setDataSource(fileInputStream.getFD());
            mediaPlayer.prepareAsync();
        } catch (Exception e) {
            e.printStackTrace();
        }
        mediaPlayer.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
            public void onPrepared(MediaPlayer player) {
                mediaPlayer.seekTo(0);
                endTime=mediaPlayer.getDuration();
                seekBar.setMax(endTime);
                endText.setText(convertTime(endTime));
                playBtn.setEnabled(true);
                playBtn.setImageResource(R.drawable.play_button_foreground);
                pauseBtn.setEnabled(true);
                pauseBtn.setImageResource(R.drawable.pause_button_foreground);
                rewindBtn.setEnabled(true);
                rewindBtn.setImageResource(R.drawable.rewind_button_foreground);
                updateSeekBar();
                setHandler=true;
            }
        });

        playBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!setHandler){
                    updateSeekBar();
                    setHandler=true;
                }
                if (!mediaPlayer.isPlaying()){
                    mediaPlayer.start();
                    playBtn.setEnabled(false);
                    playBtn.setImageResource(R.drawable.select_play_foreground);
                    pauseBtn.setEnabled(true);
                    pauseBtn.setImageResource(R.drawable.pause_button_foreground);
                    rewindBtn.setEnabled(true);
                    rewindBtn.setImageResource(R.drawable.rewind_button_foreground);
                }
            }
        });
        pauseBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mediaPlayer.isPlaying()){
                    mediaPlayer.pause();
                    playBtn.setEnabled(true);
                    playBtn.setImageResource(R.drawable.play_button_foreground);
                    pauseBtn.setEnabled(false);
                    pauseBtn.setImageResource(R.drawable.select_pause_foreground);
                }
            }
        });

        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                if (fromUser) {
                    mediaPlayer.seekTo(progress);
                    difference=0;
                    startTime=mediaPlayer.getCurrentPosition();
                    startText.setText(convertTime(startTime));
                    if (!rewindBtn.isEnabled()){
                        pauseBtn.setEnabled(false);
                        pauseBtn.setImageResource(R.drawable.select_pause_foreground);
                        rewindBtn.setEnabled(true);
                        rewindBtn.setImageResource(R.drawable.rewind_button_foreground);
                    }
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                mediaPlayer.pause();
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                if (!playBtn.isEnabled()) {
                    mediaPlayer.start();
                }
            }
        });

        rewindBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mediaPlayer.pause();
                mediaPlayer.seekTo(0);
                startTime = 0;
                seekBar.setProgress(startTime);
                startText.setText(convertTime(startTime));
                playBtn.setEnabled(true);
                playBtn.setImageResource(R.drawable.play_button_foreground);
                pauseBtn.setEnabled(true);
                pauseBtn.setImageResource(R.drawable.pause_button_foreground);
                rewindBtn.setEnabled(false);
                rewindBtn.setImageResource(R.drawable.select_rewind_foreground);
                handler.removeCallbacks(UpdateSongTime);
                difference=0;
                setHandler=false;
            }
        });
        againBtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                mediaPlayer.stop();
                handler.removeCallbacks(UpdateSongTime);
                startActivity(new Intent(PlayActivity.this, MainActivity.class));
                finish();
            }
        });
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        if(intent!=null){
            setIntent(intent);
        }
    }

    private String convertTime(int time){
        int minutes = (int) (time/60000);
        int seconds = (int) ((time/1000)%60);
        StringBuffer buffer=new StringBuffer();
        buffer
                .append(String.format("%02d", minutes))
                .append(":")
                .append(String.format("%02d", seconds));

        return buffer.toString();
    }

    private void updateSeekBar(){
        int pos=mediaPlayer.getCurrentPosition();
        if (pos+difference<seekBar.getProgress()){
            difference = java.lang.Math.abs(seekBar.getProgress()-pos);
        }
        if (seekBar.getProgress()>=mediaPlayer.getDuration()){
            difference=0;
            playBtn.setEnabled(true);
            playBtn.setImageResource(R.drawable.play_button_foreground);
            pauseBtn.setEnabled(false);
            pauseBtn.setImageResource(R.drawable.select_pause_foreground);
            rewindBtn.setEnabled(true);
            rewindBtn.setImageResource(R.drawable.rewind_button_foreground);
            handler.removeCallbacks(UpdateSongTime);
            setHandler=false;
            startTime = mediaPlayer.getDuration();
            seekBar.setProgress(startTime);
            startText.setText(convertTime(startTime));
            return;
        }
        startTime = pos+difference;
        seekBar.setProgress(startTime);
        startText.setText(convertTime(startTime));


        UpdateSongTime = new Runnable() {
            @Override
            public void run() {
                updateSeekBar();

            }
        };
        handler.postDelayed(UpdateSongTime,100);
    }


}
