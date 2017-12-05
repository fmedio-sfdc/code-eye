package com.salesforce.javaparser;

import com.google.gson.JsonObject;
import org.junit.Test;

import java.io.FileInputStream;
import java.io.StringBufferInputStream;
import java.util.Iterator;

import static org.junit.Assert.*;

public class FrameParserTest {

    @Test
    public void testParse() throws Exception {
        Iterator<JsonObject> frameParser = new FrameParser(new StringBufferInputStream(INPUT));
        assertTrue(frameParser.hasNext());
        assertEquals(2d, frameParser.next().get("lexer.types.field.ConnectUri").getAsDouble(), 0.00001d);
        assertTrue(frameParser.hasNext());
        assertEquals(3d, frameParser.next().get("lexer.types.field.ConnectUri").getAsDouble(), 0.00003d);
        assertFalse(frameParser.hasNext());
    }

    public static final String INPUT =
                    "{\n" +
                    "    \"p4.action\": \"edit\",\n" +
                    "    \"lexer.types.field.ConnectUri\": \"2.0\",\n" +
                    "    \"future.enhancement\": { \"hello\": \"world\" }\n" +
                    "}\n" +
                    "{\n" +
                    "   \"p4.action\": \"edit\",\n" +
                    "    \"lexer.types.field.ConnectUri\": \"3.0\",\n" +
                    "    \"lexer.types.field.Panda\": \"1.0\"\n" +
                    "}\n";
}
