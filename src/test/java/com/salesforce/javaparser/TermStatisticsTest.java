package com.salesforce.javaparser;

import static org.junit.Assert.assertEquals;

import java.io.StringBufferInputStream;
import java.util.Iterator;

import org.apache.lucene.index.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.junit.Test;

import com.google.gson.JsonObject;

public class TermStatisticsTest {
    @Test
    public void testIndexAndRescore() throws Exception {
        TermStatistics termStatistics = new TermStatistics();
        Iterator<JsonObject> iterator = new FrameParser(new StringBufferInputStream(FrameParserTest.INPUT));
        Directory directory = new RAMDirectory();
        termStatistics.index(iterator, directory, x -> {});
        IndexReader indexReader = DirectoryReader.open(directory);
        assertEquals(2, indexReader.docFreq(new Term(TermStatistics.FIELD_NAME, "lexer.types.field.ConnectUri")));
        assertEquals(1, indexReader.docFreq(new Term(TermStatistics.FIELD_NAME, "lexer.types.field.Panda")));

        iterator = new FrameParser(new StringBufferInputStream(FrameParserTest.INPUT));

        JsonObject rescored = termStatistics.rescore(indexReader, iterator.next());
        assertEquals(1.0d, rescored.get("lexer.types.field.ConnectUri").getAsDouble(), 0.00001d);

        rescored = termStatistics.rescore(indexReader, iterator.next());
        assertEquals(0.6495d, rescored.get("lexer.types.field.ConnectUri").getAsDouble(), 0.001d);
        assertEquals(0.2469d, rescored.get("lexer.types.field.Panda").getAsDouble(), 0.001d);
    }
}