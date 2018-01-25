package com.salesforce.javaparser;

import com.beust.jcommander.internal.Lists;
import com.salesforce.antlr.JavaLexer;
import com.salesforce.antlr.JavaParser;
import com.salesforce.antlr.JavaParser.CompilationUnitContext;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTreeWalker;
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.util.Map;

import static org.junit.Assert.assertEquals;


public class StatsListenerTest {

    private StatsListener listener;
    private int tokenCount;

    private void parse(String source) {
        CompilationUnitContext tree = getTree(source);
        ParseTreeWalker.DEFAULT.walk(listener, tree);
    }

    @Before
    public void setup() {
        listener = new StatsListener();
    }

    static String SOURCE =
            "    class Foo<T> {\n" +
                    "\n" +
                    "        static {\n" +
                    "            Panda p;\n" +
                    "            StaticBlockVariable sbv;\n" +
                    "        }\n" +
                    "\n" +
                    "        static final StaticField someStaticField = new StaticField();\n" +
                    "        GenericField<T> field;\n" +
                    "\n" +
                    "        Foo(ConstructorParameter cp, T tee) {\n" +
                    "\n" +
                    "        }\n" +
                    "\n" +
                    "        ReturnType someMethod(MethodParameter mp, T tee) throws SomeException,PandaException {\n" +
                    "            Panda p;\n" +
                    "            MethodVariable mv;\n" +
                    "            T genericMethodVariable;\n" +
                    "        }\n" +
                    "\n" +
                    "        void someOtherMethdod() throws AnotherException, SomeOtherException {}\n" +
                    "\n" +
                    "        void noExceptionsMethod() {}\n" +
                    "    }";

    @Test
    public void testMethodBlockCount() {
        parse("class Foo { public void m1() {} }");
        assertEquals(1, listener.getBlockCount());
    }

    @Test
    public void testInnerBlockCount() {
        parse("class Foo { public void m1() {{}} }");
        assertEquals(2, listener.getBlockCount());
    }

    @Test
    public void testFieldCount() {
        parse("class Foo { int a; }");
        assertEquals(1, listener.getFieldCount());
    }

    @Test
    public void testFieldsCount() {
        parse("class Foo { int a; m() {int a;} int b; }");
        assertEquals(2, listener.getFieldCount());
    }

    @Test
    public void testMaxMethodLineCount() {
        parse("class Foo { public void m1() {\n\n} public void m2() {\n\n\n} }");
        assertEquals(3, listener.getMaxMethodLineCount());
    }

    @Test
    public void testTypeTokens() {
//        String source = "class Foo<T> { static { Panda p; StaticBlockVariable sbv; } GenericField<T> field; Foo(ConstructorParameter cp, T tee) {} m(MethodParameter mp, T tee) {Panda p; MethodVariable mv; T genericMethodVariable;}}";
        parse(SOURCE);
        Map<String, String> stats = listener.getStats();
        Lists.newArrayList(
                "lexer.types.field.GenericField<T>",
                "lexer.types.field.GenericField",
                "lexer.types.field.StaticField",
                "lexer.types.method_signature.parameter.ConstructorParameter",
                "lexer.types.method_signature.parameter.MethodParameter",
                "lexer.types.method_signature.return_type.ReturnType",
                "lexer.types.method_signature.exception.SomeException",
                "lexer.types.method_signature.exception.SomeOtherException",
                "lexer.types.method_signature.exception.AnotherException",
                "lexer.types.method_signature.exception.PandaException",
                "lexer.types.local_variable.MethodVariable",
                "lexer.types.local_variable.StaticBlockVariable",
                "lexer.types.local_variable.T"
        )
                .forEach(s -> {
                    assertEquals("No value for " + s, "1.0", stats.get(s));
                });

        Lists.newArrayList(
                "lexer.types.local_variable.Panda",
                "lexer.types.method_signature.parameter.T"
        )
                .forEach(s -> {
                    assertEquals("No value for " + s, "2.0", stats.get(s));
                });
    }

    @Test
    public void testFieldIdLength() {
        parse("class Foo { int aa; }");
        assertEquals(2, listener.getAvgIdentifierLength(), 0.00001);
    }

    @Test
    public void testClassNestLevel() {
        parse("class Foo { static class a {} class b { class c {} } }");
        assertEquals(1, listener.getClassNestLevelCount(0));
        assertEquals(2, listener.getClassNestLevelCount(1));
        assertEquals(1, listener.getClassNestLevelCount(2));
    }

    @Test
    public void testMethodCount() {
        parse("class Foo { public void m1() {} \r\n public void m2() {} }");
        assertEquals(2, listener.getMethodCount());
    }

    @Test
    public void testTokenCount() {
        parse("class Foo {}");
        // token count includes EOF token
        assertEquals(5, tokenCount);
    }

    @Test
    public void testNestCount() {
        parse("class Foo { public void m1() {} }");
        assertEquals(0, listener.getBlockNestLevelCount(1));

        parse("class Foo { public void m1() {{}} }");
        assertEquals(1, listener.getBlockNestLevelCount(1));

        parse("class Foo { public void m1() {{}{}} }");
        assertEquals(2, listener.getBlockNestLevelCount(1));

        parse("class Foo { public void m1() {{{}{}}} }");
        assertEquals(1, listener.getBlockNestLevelCount(1));
        assertEquals(2, listener.getBlockNestLevelCount(2));
    }

    @Test
    public void testMaxNestLevel() {
        parse("class Foo { public void m1() {} }");
        assertEquals(1, listener.getMaxBlockNestLevel());

        parse("class Foo { public void m1() {{}} }");
        assertEquals(2, listener.getMaxBlockNestLevel());

        parse("class Foo { public void m1() {{}{{}}} }");
        assertEquals(3, listener.getMaxBlockNestLevel());
    }

    @Test
    public void testVariableCount() {
        parse("class Foo { m() {int a;} }");
        assertEquals(1, listener.getVariableCount());
    }

    @Test
    public void testVariablePerMethodCount() {
        parse("class Foo { int i; void m() {int a; int b;} void m1() {int c;} }");
        assertEquals(1.5, listener.getVarsPerMethodCount(), 0.001);
    }

    @Test
    public void testAvgVariableCount() {
        parse("class Foo { int a; m() {int a; int b;} m2() {int a;} }");
        assertEquals(3, listener.getVariableCount());
    }

    @Test
    public void testMethodIdLength() {
        parse("class Foo { int aa() {} }");
        assertEquals(2, listener.getAvgIdentifierLength(), 0.00001);
    }

    @Test
    public void testVariableIdLength() {
        parse("class Foo { int m(int a) {int aa = 1;} }");
        assertEquals((double) (1+1+2)/3, listener.getAvgIdentifierLength(), 0.00001);
    }

    @Test
    public void testAvgIdLength() {
        parse("class Foo { int a = 1; void aa(int aaa) {int aaaa = 1;} }");
        assertEquals((double) (1+2+3+4)/4, listener.getAvgIdentifierLength(), 0.00001);
    }

    private CompilationUnitContext getTree(String twoMethods) {
        CharStream input = CharStreams.fromString(twoMethods);
        JavaLexer lexer = new JavaLexer(input);
        CommonTokenStream tokenStream = new CommonTokenStream(lexer);
        JavaParser parser = new JavaParser(tokenStream);
        CompilationUnitContext compilationUnitContext = parser.compilationUnit();
        tokenCount = tokenStream.size();
        return compilationUnitContext;
    }

    @SuppressWarnings("unused")
    static class Foo {
        String notAFeature() {return "";}
        public String getStr() {
            return "";
        }

        public Integer getFoo() {
            return 1;
        }
        public void setFoo(Integer foo) {}

        public void setBar(Integer bar) {}
    }


    // This test can be used to debug parsing problems
    @SuppressWarnings("unused")
//    @Test
    public void testParsingProblem() throws IOException {

        CharStream stream = CharStreams.fromFileName("/Users/stager/Documents/dev/ml-patches/SandOmExportXiFileInfo.java1-2");
        JavaLexer lexer = new JavaLexer(stream);
        CommonTokenStream tokenStream = new CommonTokenStream(lexer);
        tokenStream.fill();

//        System.out.printf("input: `%s`\n", input);

        for (Token token : tokenStream.getTokens()) {
            System.out.printf("  %-20s %s\n", JavaLexer.VOCABULARY.getSymbolicName(token.getType()), token.getText());
        }

        System.out.println();
    }

}