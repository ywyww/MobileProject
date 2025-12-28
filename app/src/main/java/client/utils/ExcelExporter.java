package com.example.sensorclient.utils;

import android.content.Context;
import android.os.Environment;

import com.example.sensorclient.data.model.SensorHistory;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileOutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class ExcelExporter {

    public static File export(Context context, List<SensorHistory> data) throws Exception {

        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Sensor History");

        Row header = sheet.createRow(0);
        header.createCell(0).setCellValue("Timestamp");
        header.createCell(1).setCellValue("Temperature (°C)");

        SimpleDateFormat sdf =
                new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());

        int rowIndex = 1;
        for (SensorHistory item : data) {
            Row row = sheet.createRow(rowIndex++);
            row.createCell(0).setCellValue(sdf.format(new Date(item.timestamp)));
            row.createCell(1).setCellValue(item.temperature);
        }

        sheet.autoSizeColumn(0);
        sheet.autoSizeColumn(1);

        File dir = context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS);
        if (dir != null && !dir.exists()) dir.mkdirs();

        File file = new File(dir, "sensor_history.xlsx");
        FileOutputStream fos = new FileOutputStream(file);
        workbook.write(fos);

        fos.close();
        workbook.close();

        return file;
    }
}
