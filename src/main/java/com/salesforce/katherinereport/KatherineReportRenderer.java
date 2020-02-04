package com.salesforce.katherinereport;

import java.awt.*;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.io.Reader;
import java.util.Map;
import java.util.Objects;
import java.util.TreeMap;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.io.FileUtils;
import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;

public class KatherineReportRenderer {

    // Release Name,Release Date,Status,Work Record,Perforce Changelist,filename,logreg_proba,rfclass_proba

    public static class Entry {
        String name;
        String date;
        String status;
        String workRecord;
        String p4Changelist;
        String filename;
        double logreg;
        double rfClass;

        public Entry(String name, String date, String status, String workRecord, String p4Changelist, String filename, double logreg, double rfClass) {
            this.name = name;
            this.date = date;
            this.status = status;
            this.workRecord = workRecord;
            this.p4Changelist = p4Changelist;
            this.filename = filename;
            this.logreg = logreg;
            this.rfClass = rfClass;
        }

        Release getRelease() {
            return new Release(name, date, status);
        }
    }

    public static class Release implements Comparable<Release> {
        String name;
        String date;
        String status;

        public Release(String name, String date, String status) {
            this.name = name;
            this.date = date;
            this.status = status;
        }

        @Override
        public int compareTo(Release o) {
            return name.compareTo(o.name);
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Release release = (Release) o;
            return Objects.equals(name, release.name);
        }

        @Override
        public int hashCode() {

            return Objects.hash(name);
        }
    }


    public static void main(String[] args) throws Exception {
        Reader reader = new FileReader(args[0]);
        File output = new File("/Users/fabrice.medio/Downloads/katherine.html");
        FileUtils.deleteQuietly(output);
        new KatherineReportRenderer().decorate(reader, new PrintStream(output));
    }

    public void decorate(Reader reader, PrintStream printStream) throws Exception {
        printStream.println("<!DOCTYPE html>\n" +
                            "<html>\n" +
                            "<head>\n" +
                            "<meta charset=\"UTF-8\">\n" +
                            "<title>Release heatmap</title>\n" +
                            "</head>\n" +
                            "\n" +
                            "<body>\n");

        Map<Release, DescriptiveStatistics> map = scoreAll(reader);
        printStream.println("<table>");
        printStream.println("<tr><td>Release Name</td><td>Release date</td><td>Status</td><td>Predicted Issues</td></tr>");

        map.keySet().forEach(release -> {
            printStream.println("<tr><td>" + release.name + "</td><td>" + release.date + "</td>");
            DescriptiveStatistics ds = map.get(release);
            printStream.println("<td>" + release.status + "</td><td bgcolor=\"" + getHtmlColor(ds) + "\">" + ds + "</td>");
        });

        printStream.println("</table></body>\n" +
                            "\n" +
                            "</html>");

    }

    public static String getHtmlColor(DescriptiveStatistics ds) {
        double angle = 120d - (ds.getMax() * 120d);
        return HSLColor.toHtmlColor(new HSLColor(Color.red).adjustHue((float) angle));
    }

    public Map<Release, DescriptiveStatistics> scoreAll(Reader reader) throws IOException {
        Map<Release, DescriptiveStatistics> scores = new TreeMap<>();
        return parse(reader)
                .reduce(scores,
                        (in, entry) -> {
                            Release release = entry.getRelease();
                            DescriptiveStatistics ds = in.getOrDefault(release, new DescriptiveStatistics());
                            ds.addValue(entry.rfClass);
                            in.put(release, ds);
                            return in;
                        }, (left, right) -> {
                            throw new RuntimeException();
                        });

    }

    public Stream<Entry> parse(Reader reader) throws IOException {
        CSVParser parsed = CSVFormat.RFC4180.withFirstRecordAsHeader().parse(reader);
        return StreamSupport.stream(parsed.spliterator(), false)
                .map(record -> {
                    return new Entry(
                            record.get(1),
                            record.get(2),
                            record.get(3),
                            record.get(4),
                            record.get(5),
                            record.get(6),
                            tryParse(record.get(7)),
                            tryParse(record.get(8))
                    );
                });
    }

    private double tryParse(String a) {
        try {
            return Double.parseDouble(a);
        } catch (NumberFormatException e) {
            return 0;
        }
    }
}
