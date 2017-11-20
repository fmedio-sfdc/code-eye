package com.salesforce.javaparser;

import com.beust.jcommander.IParameterValidator;
import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import com.beust.jcommander.ParameterException;
import com.beust.jcommander.internal.Sets;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.salesforce.antlr.JavaBaseListener;
import com.salesforce.antlr.JavaLexer;
import com.salesforce.antlr.JavaParser;
import com.salesforce.antlr.JavaParser.VariableDeclaratorIdContext;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Type;
import java.text.DecimalFormat;
import java.util.*;


/**
 * Listens for Antlr parse events and collects statistics about
 * a given java file.
 *
 * The items below are code statistics, some of which are currently
 * collected by this class and others of which have not been implemented yet. It's
 * basically a to-do list. The completed items are marked with a * at
 * the beginning of the line. The unimplemented ideas have no *.
 *
 *   Average variable name length
    Number of segments in all camelcase words
    File/Method Name length
 *   Number of code blocks
 *   Code block depth counts for each depth
 *   Max code block depth
 *   Number of Inner classes
    Number of words that start with upper case char
    Number of words that start with a lower case char

 *   Number of local variables / method


 *   Number of methods
 *   Max method size - line count
 *   Number of Instance variables
    Number of Static initialization blocks

 # of lines / method
 # Comment lines / #code lines
 Tokens / line (e.g. >=  1 token;  a.b =  3 tokens)
    i.e. count identifiers as a single token
 Number of header comment characters
 Frequency of all non alphanumeric chars, including spaces and tabs
    # of blank lines

   See the javadoc for {@link com.salesforce.javaparser.StatsListener#main(String[])} for
   details on how to use this class as a command line tool for generating statistics for
   a java input class.


 */
public class StatsListener extends JavaBaseListener {

    private static final int MAX_NEST_LEVEL = 20;
    DecimalFormat decimalFormat = new DecimalFormat("#.00");

    private int fieldCount = 0;
    private int blockCount = 0;
    private int maxMethodLineCount = 0;
    private int methodCount = 0;
    private int variableCount = 0;
    private int identifierCount = 0;
    private int totalIdentifierLength = 0;

    private int blockNestCount = 0;
    private int maxBlockNestLevel;

    private int[] blockNestCounts;
    private int classNestCount = 0;
    private int maxClassNestLevel;

    private int[] classNestCounts;
    private final Map<String, String> stats = new TreeMap<>();

    /**
     * You can run the command line as
     * <code>
     * java -jar <path-to-jar>.jar [--fileDir /base/file/path --features comma,separated,feature,list fileName [fileName]*
     * </code>
     *
     * If any features you specify in the feature argument do not match a supporting java property
     * then you will get an IllegalArgumentException.
     *
     * @param argv filename is required, feature set is optional
     */
    public static void main(String[] argv) throws Exception {

        // Use StatsListener.java as the input for parsing
        Args args = new Args();
        JCommander.newBuilder()
                .addObject(args)
                .build()
                .parse(argv);

        Gson gson = new GsonBuilder()
                .setPrettyPrinting()
                .disableHtmlEscaping()
                .create();

        Scanner scanner = new Scanner(System.in).useDelimiter(System.getProperty("line.separator"));
        while (scanner.hasNext()) {
            Type stringStringMap = new TypeToken<Map<String, String>>(){}.getType();
            Map<String,String> input = gson.fromJson(scanner.next(), stringStringMap);
            assert input.containsKey("filename");

            String fileName = combinePath(args.fileDir, input.get("filename"));
            if (new File(fileName).exists()) {
                Map<String, String> dimensions = analyzeFile(CharStreams.fromFileName(fileName));
                input.putAll(dimensions);
                System.out.println(gson.toJson(input).toString());
            } else {
                System.err.println("Skipping file-not-found: " + fileName);
            }
        }
    }

    /**
     * Manages command line parameters using JCommander annotation library. See jcommander.org
     */
    public static class Args implements IParameterValidator {
        static final String MINUS_D = "-d";
        static final String FILE_DIR = "--fileDir";


        @Parameter(names = {FILE_DIR, MINUS_D}, validateWith = Args.class)
        public String fileDir;

        @Override
        public void validate(String name, String value) throws ParameterException {
            switch (name) {

                case FILE_DIR:
                case MINUS_D:
                    File f = new File(value);
                    if (!f.exists()) {
                        throw new ParameterException("Couldn't find specified base directory: " + value);
                    }
                    break;

            }
        }
    }

    private static Map<String, String> analyzeFile(CharStream stream) throws IOException {
        JavaLexer lexer = new JavaLexer(stream);
        CommonTokenStream tokenStream = new CommonTokenStream(lexer);
        JavaParser parser = new JavaParser(tokenStream);
        JavaParser.CompilationUnitContext tree = parser.compilationUnit();
        StatsListener listener = new StatsListener();
        ParseTreeWalker.DEFAULT.walk(listener, tree);

        Map<String, String> stats = listener.getStats();
        stats.put("tokenCount", String.valueOf(tokenStream.size()));
        return stats;
    }

    public Map<String, String> getStats() {
        return stats;
    }

    @Override
    public void enterMemberDeclaration(JavaParser.MemberDeclarationContext ctx) {
        if (ctx.fieldDeclaration() != null) {
            types(ctx.fieldDeclaration().typeType())
                    .forEach(s -> {
                        this.stats.put("lexer.types.uncategorized." + s, "1.0");
                        this.stats.put("lexer.types.field." + s, "1.0");
                    });
        }
    }

    private Collection<String> types(JavaParser.TypeTypeContext context) {
        Set<String> result = Sets.newHashSet();
        result.add(context.getText());
        JavaParser.ClassOrInterfaceTypeContext classContext = context.classOrInterfaceType();
        if (classContext != null) {
            classContext.Identifier().stream()
                    .map(i -> i.getSymbol().getText())
                    .forEach(s -> result.add(s));
        }

        return result;
    }

    @Override
    public void enterFormalParameterList(JavaParser.FormalParameterListContext ctx) {
        ctx.formalParameter().forEach(fp -> {
            types(fp.typeType()).forEach(s -> {
                this.stats.put("lexer.types.uncategorized." + s, "1.0");
                this.stats.put("lexer.types.formal_parameter." + s, "1.0");
            });
        });
    }

    private static String combinePath(String fileDir, String fileName) {
        if (fileName.startsWith("//")) {
            fileName = fileName.substring(2);
        }
        if (fileName.indexOf("#") > 0) {
            fileName = fileName.replace("#","");
        }
        File fileInDirectory;
        if (fileDir != null) {
            File baseDirectory = new File(fileDir);
            fileInDirectory = new File(baseDirectory, fileName);
        } else {
            fileInDirectory = new File(fileName);
        }
        return fileInDirectory.getPath();
    }

    @Override
    public void enterLocalVariableDeclaration(JavaParser.LocalVariableDeclarationContext ctx) {
        types(ctx.typeType()).forEach(s -> {
            this.stats.put("lexer.types.uncategorized." + s, "1.0");
            this.stats.put("lexer.types.local_variable." + s, "1.0");
        });
    }

    /**
     * Count variable names, method names and parameter names. Ignore constants and enum constants.
     */
    private void addIdentifier(int length) {
        identifierCount++;
        totalIdentifierLength += length;
    }

    @Override public void enterBlock(JavaParser.BlockContext ctx) {
        // ignore nesting levels that are too absurd
        if (blockNestCount < blockNestCounts.length) {
            blockNestCounts[blockNestCount]++;
        }
        blockNestCount++;
        if (maxBlockNestLevel < blockNestCount) {
            maxBlockNestLevel = blockNestCount;
        }
    }

    @Override public void exitBlock(JavaParser.BlockContext ctx) {
        blockCount++;
        blockNestCount--;
    }

    @Override public void enterClassDeclaration(JavaParser.ClassDeclarationContext ctx) {
        // ignore nesting levels that are too absurd
        if (classNestCount < classNestCounts.length) {
            classNestCounts[classNestCount]++;
        }
        classNestCount++;
        if (maxClassNestLevel < classNestCount) {
            maxClassNestLevel = classNestCount;
        }
    }

    @Override public void exitClassDeclaration(JavaParser.ClassDeclarationContext ctx) {
        classNestCount--;
    }

    @Override public void enterCompilationUnit(JavaParser.CompilationUnitContext ctx) {
        blockNestCounts = new int[MAX_NEST_LEVEL];
        maxBlockNestLevel = 0;

        classNestCounts = new int[MAX_NEST_LEVEL];
        maxClassNestLevel = 0;
    }

    @Override
    public void exitCompilationUnit(JavaParser.CompilationUnitContext ctx) {
        stats.put("blockCount", String.valueOf(blockCount));
        stats.put("fieldCount", String.valueOf(fieldCount));
        stats.put("methodCount", String.valueOf(methodCount));
        this.maxMethodLineCount = ctx.maxMethodLineCount;
        stats.put("maxMethodLineCount", String.valueOf(maxMethodLineCount));
        stats.put("variableCount", String.valueOf((variableCount - fieldCount)));
        stats.put("varsPerMethodCount", decimalFormat.format(getVarsPerMethodCount()));
        stats.put("avgIdentifierLength", decimalFormat.format(getAvgIdentifierLength()));
        stats.put("maxBlockNestLevel", String.valueOf(getMaxBlockNestLevel()));
    }

    @Override
    public void exitFieldDeclaration(JavaParser.FieldDeclarationContext ctx) {
        fieldCount++;
    }

    @Override
    public void enterMethodDeclaration(JavaParser.MethodDeclarationContext ctx) {
        super.enterMethodDeclaration(ctx);
    }

    @Override
    public void exitMethodDeclaration(JavaParser.MethodDeclarationContext ctx) {
        methodCount++;
        addIdentifier(ctx.Identifier().getText().length());
    }

    @Override
    public void exitVariableDeclaratorId(VariableDeclaratorIdContext ctx) {
        variableCount++;
        addIdentifier(ctx.getText().length());
    }

    double getAvgIdentifierLength() {
        return identifierCount > 0 ? ((double) totalIdentifierLength) / identifierCount : 0;
    }

    public int getBlockCount() {
        return blockCount;
    }

    public int getFieldCount() {
        return fieldCount;
    }

    public int getMethodCount() {
        return methodCount;
    }

    int getBlockNestLevelCount(int level) {
        return blockNestCounts[level];
    }

    int getClassNestLevelCount(int level) {
        return classNestCounts[level];
    }

    // Used by introspection
    @SuppressWarnings("WeakerAccess")
    public double getVarsPerMethodCount() {
        return methodCount > 0 ? ((double) (variableCount - fieldCount)) / methodCount : 0;
    }

    // Used by introspection
    @SuppressWarnings("WeakerAccess")
    public int getVariableCount() {
        return variableCount - fieldCount;
    }

    public int getMaxBlockNestLevel() {
        return maxBlockNestLevel;
    }

    // Used by introspection
    @SuppressWarnings("WeakerAccess")
    public int getMaxMethodLineCount() {
        return maxMethodLineCount;
    }
}
