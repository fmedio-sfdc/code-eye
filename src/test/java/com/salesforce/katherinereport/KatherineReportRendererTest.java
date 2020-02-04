package com.salesforce.katherinereport;

import static org.junit.Assert.assertEquals;

import java.io.*;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.junit.Before;
import org.junit.Test;

import com.salesforce.katherinereport.KatherineReportRenderer.Entry;
import com.salesforce.katherinereport.KatherineReportRenderer.Release;

public class KatherineReportRendererTest {

    private Reader reader;

    @Test
    public void testParse() throws Exception {
        List<Entry> entries = new KatherineReportRenderer()
                .parse(reader)
                .collect(Collectors.toList());
        assertEquals(4, entries.size());
        assertEquals("15893574", entries.get(3).p4Changelist);
        assertEquals(.8d, entries.get(3).rfClass, 0.00001d);
    }

    @Test
    public void testScoreAll() throws IOException {
        Reader reader = new InputStreamReader(new ByteArrayInputStream(INPUT.getBytes()));
        Map<Release, DescriptiveStatistics> map = new KatherineReportRenderer().scoreAll(reader);
        assertEquals(2, map.size());
        List<Release> releases = map.keySet().stream().collect(Collectors.toList());
        assertEquals(.4d, map.get(releases.get(0)).getMax(), 0.00001d);
        assertEquals(.8d, map.get(releases.get(1)).getMax(), 0.00001d);
    }

    @Before
    public void setUp() throws Exception {
        reader = new InputStreamReader(new ByteArrayInputStream(INPUT.getBytes()));
    }

    private final static String INPUT = "Release Name,Release Date,Status,Work Record,Perforce Changelist,filename,logreg_proba,rfclass_proba\n" +
                                        "210.17.17,2018-02-01T23:30:00.000Z,Deployed Successfully,W-4608896,15889423,foo,0.2,\n" +
                                        "210.17.17,2018-02-01T23:30:00.000Z,Deployed Successfully,W-4608896,15891005,bar,0.4,\n" +
                                        "210.17.18,2018-02-01T23:30:00.000Z,Deployed Successfully,W-4608896,15892102,hello,0.6,\n" +
                                        "210.17.18,2018-02-01T23:30:00.000Z,Deployed Successfully,W-4608896,15893574,panda,0.8,";
}